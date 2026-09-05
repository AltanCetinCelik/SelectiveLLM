"""Fail-closed runner for preregistered causal-importance discovery."""

from __future__ import annotations

import hashlib
import json
import math
import platform
import shutil
import subprocess
from collections import Counter
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from time import perf_counter
from typing import Any

import numpy as np
import yaml

from selectivellm.causal_importance.analysis import (
    analyze_causal_matrix,
    analyze_signed_diagnostics,
)
from selectivellm.causal_importance.discovery import build_discovery
from selectivellm.causal_importance.gradient import (
    GradientCompatibleScorer,
    GradientMeasurement,
    aggregate_blocks,
)
from selectivellm.causal_importance.mappings import BlockMapping
from selectivellm.causal_importance.masks import (
    BlockIntervention,
    BlockMask,
    expanded_channels,
    validate_block_mask,
)
from selectivellm.causal_importance.report import generate_plots, write_report
from selectivellm.dense_capacity.benchmark import (
    DenseBenchmarkCase,
    DenseBenchmarkDataset,
    validate_benchmark,
)
from selectivellm.dense_capacity.scoring import ForcedChoiceScorer
from selectivellm.provenance import stable_fingerprint

MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
MODEL_REVISION = "989aa7980e4cf806f80c7fef2b1adb7bc71aa306"


class CausalImportanceRunner:
    def __init__(
        self,
        config_path: str | Path = "configs/causal_importance_v1.yaml",
        *,
        results_root: str | Path = "results/real/causal_importance",
    ) -> None:
        self.config_path = Path(config_path).resolve()
        self.config = yaml.safe_load(self.config_path.read_text(encoding="utf-8"))
        self.benchmark_path = self._resolve(self.config["benchmark"]["path"])
        self.dataset = DenseBenchmarkDataset.from_yaml(self.benchmark_path)
        self.mapping_paths = {
            int(size): self._resolve(path) for size, path in self.config["mappings"].items()
        }
        self.mappings = {
            size: BlockMapping.from_json(path) for size, path in self.mapping_paths.items()
        }
        if set(self.mappings) != {64, 128}:
            raise ValueError("the experiment requires canonical 64- and 128-channel mappings")
        self.results_root = Path(results_root).resolve()

    def preflight(self, output_path: str | Path | None = None) -> Path:
        output = Path(output_path) if output_path else self.results_root / "preflight.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        model, tokenizer, _ = self._load_model()
        scorer = GradientCompatibleScorer(model, tokenizer, "mps")
        tokenizer_validation = scorer.validate_protocol(self.dataset.cases)
        case = self._ordered_cases("discovery")[0]
        validation = self._gradient_preflight(scorer, case)
        self._write_json(
            output,
            {
                "status": "valid" if validation["passed"] else "invalid",
                "created_at": datetime.now(UTC).isoformat(),
                "case_id": case.id,
                "tokenizer_validation": tokenizer_validation,
                "gradient_validation": validation,
                "mapping_hashes": {
                    str(size): mapping.mapping_hash for size, mapping in self.mappings.items()
                },
                "scientific_values_inspected": False,
            },
        )
        if not validation["passed"]:
            raise RuntimeError("gradient preflight failed")
        return output.resolve()

    def run(self, run_id: str | None = None) -> Path:
        source_status = self._git_status()
        source_dirty = bool(source_status)
        run_id = run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        run_path = self.results_root / run_id
        if run_path.exists():
            raise FileExistsError(f"run already exists: {run_path}")
        run_path.mkdir(parents=True)
        manifest = self._initial_manifest(run_id, source_dirty, source_status)
        self._write_json(run_path / "manifest.json", manifest)
        shutil.copy2(self.config_path, run_path / "config.yaml")
        shutil.copy2(self.benchmark_path, run_path / "benchmark.yaml")
        for size, mapping_path in self.mapping_paths.items():
            shutil.copy2(mapping_path, run_path / f"mapping_block{size}.json")

        try:
            immutable = self._verify_immutable_inputs()
            self._write_json(run_path / "immutable_input_validation.json", immutable)
            model, tokenizer, torch = self._load_model()
            scorer = GradientCompatibleScorer(model, tokenizer, "mps")
            tokenizer_validation = scorer.validate_protocol(self.dataset.cases)
            self._write_json(run_path / "tokenizer_validation.json", tokenizer_validation)
            manifest["tokenizer_validation"] = tokenizer_validation
            manifest["model_runtime"] = self._model_runtime(model, torch)
            manifest["benchmark_fingerprint"] = self._fingerprint(tokenizer_validation)
            self._write_json(run_path / "environment.json", manifest["model_runtime"])
            self._write_json(run_path / "manifest.json", manifest)

            discovery_cases = self._ordered_cases("discovery")
            preflight = self._gradient_preflight(scorer, discovery_cases[0])
            self._write_json(run_path / "gradient_preflight.json", preflight)
            if not preflight["passed"]:
                raise RuntimeError("canonical gradient preflight failed")

            channel_summaries, discovery_meta = self._measure_cases(
                scorer,
                discovery_cases,
                phase="discovery",
                progress_path=run_path / "discovery_progress.json",
            )
            np.savez_compressed(
                run_path / "discovery_channel_summaries.npz",
                **channel_summaries,
                case_ids=np.asarray([case.id for case in discovery_cases]),
                domains=np.asarray([case.domain for case in discovery_cases]),
            )
            self._write_jsonl(run_path / "discovery_gradient_metadata.jsonl", discovery_meta)
            discovery = build_discovery(
                channel_summaries,
                discovery_cases,
                [self.mappings[64], self.mappings[128]],
            )
            masks, stability = self._write_discovery_artifacts(discovery, run_path)

            evaluation_cases = self._ordered_cases("evaluation")
            print("causal-importance: scoring 32 full-model baselines", flush=True)
            full_rows = [self._timed_score(scorer, case, "full_model") for case in evaluation_cases]
            self._write_jsonl(run_path / "full_model_scores.jsonl", full_rows)
            numerical = self._numerical_stability(
                scorer, [case for case in evaluation_cases if case.stability_sentinel]
            )
            self._write_json(run_path / "numerical_stability.json", numerical)

            masked_rows = self._score_masks(
                model,
                scorer,
                evaluation_cases,
                masks,
                full_rows,
                run_path / "causal_progress.json",
            )
            self._write_jsonl(run_path / "causal_scores.jsonl", masked_rows)

            signed_channel, signed_meta = self._measure_cases(
                scorer,
                evaluation_cases,
                phase="heldout_signed_diagnostic",
                progress_path=run_path / "signed_progress.json",
            )
            np.savez_compressed(
                run_path / "heldout_signed_channel_summaries.npz",
                gradient_signed_sum=signed_channel["gradient_signed_sum"],
                gradient_signed_mean=signed_channel["gradient_signed_mean"],
                case_ids=np.asarray([case.id for case in evaluation_cases]),
                domains=np.asarray([case.domain for case in evaluation_cases]),
            )
            self._write_jsonl(run_path / "heldout_gradient_metadata.jsonl", signed_meta)
            signed_rows = self._build_signed_rows(signed_channel, evaluation_cases, masks)
            self._write_jsonl(run_path / "signed_diagnostics.jsonl", signed_rows)

            validity = self._validity(
                preflight,
                numerical,
                full_rows,
                masked_rows,
                signed_rows,
                masks,
            )
            self._write_json(run_path / "validity.json", validity)
            analysis = analyze_causal_matrix(full_rows, masked_rows, stability, validity)
            signed_analysis = analyze_signed_diagnostics(signed_rows, masked_rows)
            self._write_json(run_path / "causal_analysis.json", analysis)
            self._write_jsonl(run_path / "paired_causal_effects.jsonl", analysis["paired_rows"])
            self._write_json(run_path / "signed_analysis.json", signed_analysis)

            generate_plots(analysis, stability, run_path / "plots")
            write_report(analysis, stability, signed_analysis, manifest, run_path / "report.md")
            self._write_failure_analysis(analysis, run_path / "failure_analysis.md")
            manifest["status"] = "completed"
            manifest["completed"] = True
            manifest["completed_at"] = datetime.now(UTC).isoformat()
            manifest["primary_decision"] = analysis["primary_decision"]
            manifest["final_memory"] = self._memory(torch)
            manifest["publishable"] = not source_dirty
            manifest["artifact_sha256"] = self._artifact_hashes(run_path)
            self._write_json(run_path / "manifest.json", manifest)
            if not source_dirty:
                self._publish_latest(run_path)
            return run_path
        except Exception as exc:
            manifest["status"] = "failed"
            manifest["completed"] = False
            manifest["publishable"] = False
            manifest["failed_at"] = datetime.now(UTC).isoformat()
            manifest["failure"] = f"{type(exc).__name__}: {exc}"
            manifest["artifact_sha256"] = self._artifact_hashes(run_path)
            self._write_json(run_path / "manifest.json", manifest)
            raise

    def _measure_cases(
        self,
        scorer: ForcedChoiceScorer,
        cases: list[DenseBenchmarkCase],
        *,
        phase: str,
        progress_path: Path,
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        values: dict[str, list[Any]] = {
            "activation": [],
            "gradient_absolute": [],
            "gradient_signed_sum": [],
            "gradient_signed_mean": [],
        }
        metadata: list[dict[str, Any]] = []
        started = perf_counter()
        with GradientMeasurement(scorer) as measurement:
            for index, case in enumerate(cases, start=1):
                result = measurement.measure(case)
                for name, array in result["summaries"].items():
                    values[name].append(array)
                metadata.append({key: value for key, value in result.items() if key != "summaries"})
                self._write_json(
                    progress_path,
                    {
                        "phase": phase,
                        "completed": index,
                        "total": len(cases),
                        "elapsed_seconds": perf_counter() - started,
                    },
                )
                print(f"causal-importance: {phase} {index}/{len(cases)}", flush=True)
        stacked = {name: np.stack(arrays).astype(np.float32) for name, arrays in values.items()}
        return stacked, metadata

    def _write_discovery_artifacts(
        self, discovery: dict[str, Any], run_path: Path
    ) -> tuple[list[BlockMask], dict[str, Any]]:
        self._write_json(run_path / "split_assignments.json", discovery["split_assignments"])
        masks: list[BlockMask] = []
        stability: dict[str, Any] = {}
        for size in (64, 128):
            item = discovery["block_sizes"][str(size)]
            np.savez_compressed(
                run_path / f"raw_blocks_{size}.npz",
                **item["raw_blocks"],
            )
            np.savez_compressed(
                run_path / f"normalized_blocks_{size}.npz",
                **item["normalized"],
            )
            np.savez_compressed(
                run_path / f"rankings_{size}.npz",
                **item["rankings"],
            )
            masks.extend(item["masks"])
            stability[str(size)] = item["stability"]
        self._write_jsonl(run_path / "masks.jsonl", [mask.to_dict() for mask in masks])
        self._write_json(run_path / "stability.json", stability)
        if len(masks) != 36:
            raise RuntimeError("the experiment requires exactly 36 masks")
        return masks, stability

    def _score_masks(
        self,
        model: Any,
        scorer: ForcedChoiceScorer,
        cases: list[DenseBenchmarkCase],
        masks: list[BlockMask],
        full_rows: list[dict[str, Any]],
        progress_path: Path,
    ) -> list[dict[str, Any]]:
        full = {str(row["case_id"]): row for row in full_rows}
        rows: list[dict[str, Any]] = []
        started = perf_counter()
        for mask_index, mask in enumerate(masks, start=1):
            mapping = self.mappings[mask.block_size]
            with BlockIntervention(model, mask, mapping):
                for case in cases:
                    row = self._timed_score(scorer, case, mask.name)
                    baseline = full[case.id]
                    rows.append(
                        {
                            **row,
                            "block_size": mask.block_size,
                            "discovery_method": mask.discovery_method,
                            "mask_source": mask.source,
                            "source_domain": mask.source_domain,
                            "mask_name": mask.name,
                            "mask_sha256": mask.to_dict()["mask_sha256"],
                            "mapping_sha256": mask.mapping_sha256,
                            "quota_pattern_sha256": mask.quota_pattern_sha256,
                            "mask_semantics": mask.mask_semantics,
                            "seed": mask.seed,
                            "full_correct_nll": float(baseline["correct_nll"]),
                            "causal_damage": float(row["correct_nll"])
                            - float(baseline["correct_nll"]),
                        }
                    )
            self._write_json(
                progress_path,
                {
                    "completed_masks": mask_index,
                    "total_masks": len(masks),
                    "completed_scores": len(rows),
                    "total_scores": len(masks) * len(cases),
                    "elapsed_seconds": perf_counter() - started,
                },
            )
            print(f"causal-importance: causal mask {mask_index}/{len(masks)}", flush=True)
        if len(rows) != 1152:
            raise RuntimeError(f"incomplete causal matrix: {len(rows)}/1152")
        return rows

    def _build_signed_rows(
        self,
        channels: dict[str, Any],
        cases: list[DenseBenchmarkCase],
        masks: list[BlockMask],
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        active_masks = [mask for mask in masks if mask.source != "noop"]
        for case_index, case in enumerate(cases):
            signed_sum = channels["gradient_signed_sum"][case_index]
            signed_mean = channels["gradient_signed_mean"][case_index]
            for mask in active_masks:
                mapping = self.mappings[mask.block_size]
                taylor = 0.0
                normalized = 0.0
                for layer in range(28):
                    selected = expanded_channels(mask, mapping, layer)
                    taylor += float(signed_sum[layer, selected].sum(dtype=np.float64))
                    normalized += float(signed_mean[layer, selected].sum(dtype=np.float64))
                if not math.isfinite(taylor) or not math.isfinite(normalized):
                    raise FloatingPointError(
                        f"nonfinite signed diagnostic for {case.id}/{mask.name}"
                    )
                rows.append(
                    {
                        "case_id": case.id,
                        "domain": case.domain,
                        "mask_name": mask.name,
                        "block_size": mask.block_size,
                        "discovery_method": mask.discovery_method,
                        "mask_source": mask.source,
                        "source_domain": mask.source_domain,
                        "predicted_taylor_damage": taylor,
                        "normalized_signed_attribution": normalized,
                        "classification_input": False,
                    }
                )
        if len(rows) != 1088:
            raise RuntimeError(f"incomplete signed diagnostic matrix: {len(rows)}/1088")
        return rows

    def _gradient_preflight(
        self, scorer: ForcedChoiceScorer, case: DenseBenchmarkCase
    ) -> dict[str, Any]:
        ordinary = scorer.score(case)
        with GradientMeasurement(scorer) as measurement:
            gradient = measurement.measure(case)
        logit_differences = {
            label: abs(
                float(ordinary["option_logits"][label]) - float(gradient["option_logits"][label])
            )
            for label in ordinary["option_logits"]
        }
        block_shapes = {
            str(size): {
                name: list(aggregate_blocks(array, size).shape)
                for name, array in gradient["summaries"].items()
            }
            for size in (64, 128)
        }
        nll_difference = abs(float(ordinary["correct_nll"]) - float(gradient["correct_nll"]))
        passed = bool(
            max(logit_differences.values()) <= 1e-4
            and nll_difference <= 1e-4
            and ordinary["prediction"] == gradient["prediction"]
            and len(gradient["shape_records"]) == 28
            and all(item["finite"] for item in gradient["shape_records"])
        )
        return {
            "passed": passed,
            "case_id": case.id,
            "max_option_logit_difference": max(logit_differences.values()),
            "correct_nll_difference": nll_difference,
            "tolerance": 1e-4,
            "prediction_identical": ordinary["prediction"] == gradient["prediction"],
            "captured_layer_count": len(gradient["shape_records"]),
            "activation_gradient_shapes_identical": all(
                item["activation_shape"] == item["gradient_shape"]
                for item in gradient["shape_records"]
            ),
            "channel_dimension": gradient["shape_records"][0]["activation_shape"][-1],
            "all_finite": all(item["finite"] for item in gradient["shape_records"]),
            "block_aggregate_shapes": block_shapes,
            "scientific_values_inspected": False,
        }

    def _validity(
        self,
        preflight: dict[str, Any],
        numerical: dict[str, Any],
        full_rows: list[dict[str, Any]],
        masked_rows: list[dict[str, Any]],
        signed_rows: list[dict[str, Any]],
        masks: list[BlockMask],
    ) -> dict[str, Any]:
        full = {str(row["case_id"]): row for row in full_rows}
        answer_counts = Counter(str(row["correct_label"]) for row in full_rows)
        causal_cells = {(row["mask_name"], row["case_id"]) for row in masked_rows}
        expected_causal = {(mask.name, case_id) for mask in masks for case_id in full}
        active_masks = [mask for mask in masks if mask.source != "noop"]
        signed_cells = {(row["mask_name"], row["case_id"]) for row in signed_rows}
        expected_signed = {(mask.name, case_id) for mask in active_masks for case_id in full}
        noops = [row for row in masked_rows if row["mask_source"] == "noop"]
        for mask in masks:
            validate_block_mask(mask, self.mappings[mask.block_size])
        finite_rows = all(
            math.isfinite(float(row[field]))
            for row in [*full_rows, *masked_rows]
            for field in ("correct_nll", "probability_sum")
        ) and all(
            math.isfinite(float(row[field]))
            for row in signed_rows
            for field in ("predicted_taylor_damage", "normalized_signed_attribution")
        )
        checks = {
            "gradient_preflight_passed": bool(preflight["passed"]),
            "full_model_accuracy_at_least_50_percent": float(
                np.mean([bool(row["correct"]) for row in full_rows])
            )
            >= 0.50,
            "answer_positions_balanced": answer_counts == Counter({label: 8 for label in "ABCD"}),
            "repeated_scoring_stable": bool(numerical["passed"]),
            "mapping_and_mask_structure_valid": True,
            "all_values_finite": finite_rows,
            "all_probability_sums_valid": all(
                abs(float(row["probability_sum"]) - 1.0) <= 1e-6
                for row in [*full_rows, *masked_rows]
            ),
            "complete_full_matrix": len(full_rows) == 32 and len(full) == 32,
            "complete_causal_matrix": len(masked_rows) == 1152 and causal_cells == expected_causal,
            "complete_signed_matrix": len(signed_rows) == 1088 and signed_cells == expected_signed,
            "noop_equivalent": len(noops) == 64
            and max(abs(float(row["causal_damage"])) for row in noops) <= 1e-4
            and all(row["prediction"] == full[row["case_id"]]["prediction"] for row in noops),
            "signed_diagnostics_excluded_from_masks": all(
                "signed" not in json.dumps(mask.to_dict()).casefold()
                and "taylor" not in json.dumps(mask.to_dict()).casefold()
                for mask in masks
            ),
        }
        return {
            "passed": all(checks.values()),
            "checks": checks,
            "full_model_accuracy": float(np.mean([bool(row["correct"]) for row in full_rows])),
            "correct_answer_position_counts": dict(sorted(answer_counts.items())),
            "causal_rows": len(masked_rows),
            "signed_rows": len(signed_rows),
            "noop_rows": len(noops),
            "noop_max_nll_difference": max(abs(float(row["causal_damage"])) for row in noops),
        }

    def _numerical_stability(
        self, scorer: ForcedChoiceScorer, cases: list[DenseBenchmarkCase]
    ) -> dict[str, Any]:
        rows = {case.id: [scorer.score(case) for _ in range(3)] for case in cases}
        ranges = [
            max(float(row["correct_nll"]) for row in repetitions)
            - min(float(row["correct_nll"]) for row in repetitions)
            for repetitions in rows.values()
        ]
        predictions_stable = all(
            len({row["prediction"] for row in repetitions}) == 1 for repetitions in rows.values()
        )
        return {
            "sentinel_count": len(cases),
            "repetitions": 3,
            "max_correct_nll_range": max(ranges),
            "predictions_stable": predictions_stable,
            "passed": max(ranges) <= 1e-4 and predictions_stable,
            "rows": rows,
        }

    def _verify_immutable_inputs(self) -> dict[str, Any]:
        benchmark_validation = validate_benchmark(self.dataset)
        expected_benchmark = "f4cf067de00d490a036488520768c82a5e0ea7bd0a126946b887fc5fd679d5e0"
        if benchmark_validation["benchmark_sha256"] != expected_benchmark:
            raise RuntimeError("immutable benchmark hash changed")
        published_root = Path("results/real/dense_capacity/latest").resolve()
        audit = json.loads(
            (published_root / "posthoc_reporting_audit.json").read_text(encoding="utf-8")
        )
        manifest = json.loads((published_root / "manifest.json").read_text(encoding="utf-8"))
        prior_root = published_root.parent / manifest["run_id"]
        observed: dict[str, str] = {}
        for name, expected_hash in audit["input_file_sha256"].items():
            observed[name] = hashlib.sha256((prior_root / name).read_bytes()).hexdigest()
            if observed[name] != expected_hash:
                raise RuntimeError(f"immutable prior evidence changed: {name}")
        return {
            "status": "valid",
            "benchmark_validation": benchmark_validation,
            "prior_classification": "C",
            "prior_evidence_hashes": observed,
            "mapping_hashes": {
                str(size): mapping.mapping_hash for size, mapping in self.mappings.items()
            },
            "quota_pattern_hashes": {
                str(size): mapping.quota_pattern_hash for size, mapping in self.mappings.items()
            },
        }

    def _load_model(self) -> tuple[Any, Any, Any]:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        if not torch.backends.mps.is_available():
            raise RuntimeError("the frozen experiment requires Apple MPS")
        torch.manual_seed(42)
        np.random.seed(42)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
        loaded: Any = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            revision=MODEL_REVISION,
            dtype=torch.float16,
            low_cpu_mem_usage=True,
        )
        model: Any = loaded.to("mps")
        model.eval()
        model.config.use_cache = False
        for parameter in model.parameters():
            parameter.requires_grad_(False)
        if "peft" in type(model).__module__.casefold() or hasattr(model, "peft_config"):
            raise RuntimeError("adapter/PEFT contamination detected")
        resolved = getattr(model.config, "_commit_hash", None)
        if resolved not in {None, MODEL_REVISION}:
            raise RuntimeError(f"model resolved to unexpected revision: {resolved}")
        return model, tokenizer, torch

    def _fingerprint(self, tokenizer_validation: dict[str, Any]) -> str:
        return stable_fingerprint(
            {
                "experiment_version": self.config["experiment_version"],
                "backend": "transformers_dense_real",
                "model": MODEL_ID,
                "revision": MODEL_REVISION,
                "benchmark_hash": self.dataset.canonical_hash(),
                "prompt_hash": tokenizer_validation["prompt_template_sha256"],
                "mapping_hashes": {
                    str(size): mapping.mapping_hash for size, mapping in self.mappings.items()
                },
                "quota_hashes": {
                    str(size): mapping.quota_pattern_hash for size, mapping in self.mappings.items()
                },
                "discovery_schema": self.config["discovery_schema_version"],
                "metric_schema": self.config["metric_schema_version"],
                "seed_policy": "split/bootstrap:42; random controls:42-46",
                "device": "apple_mps_unified_memory",
                "measurement": "logical_contiguous_mlp_block_ablation",
                "scoring_execution": self.config["scoring_execution"],
            }
        )

    def _initial_manifest(
        self, run_id: str, source_dirty: bool, source_status: str
    ) -> dict[str, Any]:
        return {
            "run_id": run_id,
            "created_at": datetime.now(UTC).isoformat(),
            "status": "running",
            "experiment_version": self.config["experiment_version"],
            "discovery_schema_version": self.config["discovery_schema_version"],
            "mapping_schema_version": self.config["mapping_schema_version"],
            "metric_schema_version": self.config["metric_schema_version"],
            "backend": "transformers_dense_real",
            "backend_kind": "real",
            "model_identity": MODEL_ID,
            "model_revision": MODEL_REVISION,
            "adapter_set": [],
            "benchmark_version": self.dataset.benchmark_version,
            "benchmark_hash": self.dataset.canonical_hash(),
            "block_sizes": {"64": "primary", "128": "corroborative"},
            "mapping_hashes": {
                str(size): mapping.mapping_hash for size, mapping in self.mappings.items()
            },
            "quota_pattern_hashes": {
                str(size): mapping.quota_pattern_hash for size, mapping in self.mappings.items()
            },
            "git_commit": self._git_commit(),
            "source_dirty": source_dirty,
            "dirty": source_dirty,
            "git_status_porcelain": source_status,
            "canonical_latest_eligible": not source_dirty,
            "platform": platform.platform(),
            "packages": self._package_versions(),
            "logical_masking_only": True,
            "measured_vram_reduction": False,
            "measurement_semantics": {
                "causal": "logical zeroing at MLP down_proj input",
                "predicted_taylor_damage": "token-summed signed first-order estimate",
                "normalized_signed_attribution": "token-mean signed attribution",
                "scoring_execution": (
                    "frozen parameters; detached input embeddings; gradient-enabled forward; "
                    "no backward outside discovery and held-out signed diagnostics"
                ),
                "memory": "real unified-memory allocation; no parameters unloaded",
            },
        }

    @staticmethod
    def _model_runtime(model: Any, torch: Any) -> dict[str, Any]:
        return {
            "class": f"{type(model).__module__}.{type(model).__name__}",
            "dtype": str(next(model.parameters()).dtype),
            "device": str(next(model.parameters()).device),
            "layers": int(model.config.num_hidden_layers),
            "intermediate_size": int(model.config.intermediate_size),
            "use_cache": bool(model.config.use_cache),
            "adapter_wrapper_detected": False,
            "parameters_frozen": not any(
                parameter.requires_grad for parameter in model.parameters()
            ),
            "attention_implementation": str(
                getattr(model.config, "_attn_implementation", "unknown")
            ),
            "memory_after_load": CausalImportanceRunner._memory(torch),
        }

    @staticmethod
    def _memory(torch: Any) -> dict[str, float]:
        return {
            "mps_current_allocated_mb": float(torch.mps.current_allocated_memory() / 2**20),
            "mps_driver_allocated_mb": float(torch.mps.driver_allocated_memory() / 2**20),
        }

    @staticmethod
    def _timed_score(
        scorer: ForcedChoiceScorer, case: DenseBenchmarkCase, condition: str
    ) -> dict[str, Any]:
        started = perf_counter()
        row = scorer.score(case)
        return {**row, "condition": condition, "latency_ms": (perf_counter() - started) * 1000}

    def _ordered_cases(self, split: str) -> list[DenseBenchmarkCase]:
        return sorted(
            [case for case in self.dataset.cases if case.split == split],
            key=lambda case: case.id,
        )

    def _resolve(self, path: str) -> Path:
        candidate = Path(path)
        return (candidate if candidate.is_absolute() else Path.cwd() / candidate).resolve()

    @staticmethod
    def _package_versions() -> dict[str, str]:
        output: dict[str, str] = {}
        for package in ("torch", "transformers", "numpy", "safetensors", "accelerate"):
            try:
                output[package] = version(package)
            except PackageNotFoundError:
                output[package] = "not-installed"
        return output

    @staticmethod
    def _git_commit() -> str:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True
        ).stdout.strip()

    @staticmethod
    def _git_status() -> str:
        return subprocess.run(
            ["git", "status", "--porcelain"], check=True, capture_output=True, text=True
        ).stdout.strip()

    @staticmethod
    def _write_json(path: Path, value: Any) -> None:
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    @staticmethod
    def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
        path.write_text(
            "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
            encoding="utf-8",
        )

    @staticmethod
    def _artifact_hashes(run_path: Path) -> dict[str, str]:
        return {
            str(path.relative_to(run_path)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(run_path.rglob("*"))
            if path.is_file() and path.name != "manifest.json"
        }

    @staticmethod
    def _write_failure_analysis(analysis: dict[str, Any], path: Path) -> None:
        rows = sorted(
            [row for row in analysis["paired_rows"] if row["discovery_method"] == "gradient"],
            key=lambda row: float(row["gradient_same_minus_activation_same"]),
        )
        lines = [
            "# Failure Analysis",
            "",
            "Real dense-model NLL under logical contiguous-block masking; no memory claim.",
            "",
            "| Case | Domain | Blocks | Gradient - activation | Same - random | Same - wrong |",
            "|---|---|---:|---:|---:|---:|",
        ]
        for row in rows[:32]:
            lines.append(
                f"| {row['case_id']} | {row['domain']} | {row['block_size']} | "
                f"{row['gradient_same_minus_activation_same']:.4f} | "
                f"{row['same_minus_random']:.4f} | {row['same_minus_wrong']:.4f} |"
            )
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    @staticmethod
    def _publish_latest(run_path: Path) -> None:
        latest = run_path.parent / "latest"
        if latest.exists():
            shutil.rmtree(latest)
        latest.mkdir(parents=True)
        excluded = {
            "discovery_channel_summaries.npz",
            "heldout_signed_channel_summaries.npz",
            "raw_blocks_64.npz",
            "raw_blocks_128.npz",
            "normalized_blocks_64.npz",
            "normalized_blocks_128.npz",
        }
        for source in run_path.iterdir():
            if source.name in excluded or source.name.endswith("_progress.json"):
                continue
            destination = latest / source.name
            if source.is_dir():
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
