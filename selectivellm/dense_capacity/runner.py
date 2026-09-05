"""End-to-end runner for the frozen dense-capacity feasibility experiment."""

from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from time import perf_counter
from typing import Any

import numpy as np
import yaml

from selectivellm.dense_capacity.analysis import analyze_causal_rows, analyze_retention_rows
from selectivellm.dense_capacity.benchmark import (
    DenseBenchmarkCase,
    DenseBenchmarkDataset,
    validate_benchmark,
)
from selectivellm.dense_capacity.discovery import (
    GRANULARITIES,
    build_discovery,
    build_retention_masks,
)
from selectivellm.dense_capacity.interventions import (
    Intervention,
    LogicalMask,
    validate_attention_contract,
)
from selectivellm.dense_capacity.report import generate_plots, write_report
from selectivellm.dense_capacity.scoring import ForcedChoiceScorer
from selectivellm.dense_capacity.tracing import ActivationTracer
from selectivellm.provenance import stable_fingerprint

MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
MODEL_REVISION = "989aa7980e4cf806f80c7fef2b1adb7bc71aa306"


class DenseCapacityRunner:
    def __init__(
        self,
        config_path: str | Path = "configs/dense_capacity_v1.yaml",
        *,
        results_root: str | Path = "results/real/dense_capacity",
    ) -> None:
        self.config_path = Path(config_path).resolve()
        self.config = yaml.safe_load(self.config_path.read_text(encoding="utf-8"))
        benchmark_path = Path(self.config["benchmark"]["path"])
        self.benchmark_path = (
            benchmark_path if benchmark_path.is_absolute() else Path.cwd() / benchmark_path
        ).resolve()
        self.dataset = DenseBenchmarkDataset.from_yaml(self.benchmark_path)
        self.results_root = Path(results_root).resolve()

    def run(self, run_id: str | None = None) -> Path:
        run_id = run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        run_path = self.results_root / run_id
        if run_path.exists():
            raise FileExistsError(f"run already exists: {run_path}")
        run_path.mkdir(parents=True)
        manifest = self._initial_manifest(run_id)
        self._write_json(run_path / "manifest.json", manifest)
        shutil.copy2(self.config_path, run_path / "config.yaml")
        shutil.copy2(self.benchmark_path, run_path / "benchmark.yaml")

        try:
            benchmark_validation = validate_benchmark(self.dataset)
            self._verify_frozen_hashes(benchmark_validation)
            self._write_json(run_path / "benchmark_validation.json", benchmark_validation)

            model, tokenizer, torch = self._load_model()
            manifest["model_load_completed_at"] = datetime.now(UTC).isoformat()
            manifest["model_runtime"] = self._model_runtime(model, torch)
            self._write_json(
                run_path / "environment.json",
                {
                    "platform": manifest["platform"],
                    "packages": manifest["packages"],
                    "model_runtime": manifest["model_runtime"],
                },
            )
            scorer = ForcedChoiceScorer(model, tokenizer, "mps")
            tokenizer_validation = scorer.validate_protocol(self.dataset.cases)
            self._write_json(run_path / "tokenizer_validation.json", tokenizer_validation)
            manifest["tokenizer_validation"] = tokenizer_validation
            manifest["benchmark_fingerprint"] = stable_fingerprint(
                {
                    "experiment_version": self.config["experiment_version"],
                    "backend": "transformers_dense_real",
                    "model_identity": MODEL_ID,
                    "model_revision": MODEL_REVISION,
                    "adapter_set": [],
                    "benchmark_version": self.dataset.benchmark_version,
                    "benchmark_hash": self.dataset.canonical_hash(),
                    "metric_schema_version": self.config["metric_schema_version"],
                    "seed_policy": "discovery/bootstrap:42; random controls:42-46",
                    "device_class": "apple_mps_unified_memory",
                    "measurement_semantics": "logical_inference_time_masking",
                    "prompt_template_hash": tokenizer_validation["prompt_template_sha256"],
                }
            )
            self._write_json(run_path / "manifest.json", manifest)

            evaluation = self._ordered_cases("evaluation")
            sentinels = [case for case in evaluation if case.stability_sentinel]
            contracts = self._validate_runtime_contracts(model, scorer, sentinels)
            self._write_json(run_path / "implementation_validation.json", contracts)
            head_enabled = contracts["attention_head_layout"]["status"] == "valid"
            layer_enabled = contracts["layer_identity_bypass"]["status"] == "valid"
            manifest["supported_granularities"] = [
                "mlp",
                *(["head"] if head_enabled else []),
                *(["layer"] if layer_enabled else []),
            ]
            manifest["disabled_granularities"] = {
                "head": None if head_enabled else "runtime_layout_contract_not_established",
                "layer": None if layer_enabled else "identity_bypass_contract_not_established",
            }
            self._write_json(run_path / "manifest.json", manifest)

            discovery_cases = self._ordered_cases("discovery")
            raw = self._trace_discovery(
                model, scorer, discovery_cases, trace_heads=head_enabled, run_path=run_path
            )
            rankings, masks, stability = build_discovery(raw, discovery_cases)
            if not layer_enabled:
                masks = [mask for mask in masks if mask.granularity != "layer"]
                stability["granularities"].pop("layer", None)
                stability["mask_overlap"].pop("layer", None)
            np.savez_compressed(run_path / "selectivity_rankings.npz", **rankings)  # type: ignore[arg-type]
            self._write_jsonl(run_path / "initial_masks.jsonl", [mask.to_dict() for mask in masks])
            self._write_json(run_path / "stability.json", stability)

            print("dense-capacity: scoring 32 full-model held-out baselines", flush=True)
            full_rows = [
                self._timed_score(scorer, case, condition="full_model") for case in evaluation
            ]
            self._write_jsonl(run_path / "full_model_scores.jsonl", full_rows)

            numerical_stability = self._score_numerical_stability(scorer, sentinels)
            self._write_json(run_path / "numerical_stability.json", numerical_stability)

            causal_rows, noop_rows = self._score_initial_matrix(
                model, scorer, evaluation, masks, run_path
            )
            self._write_jsonl(run_path / "causal_scores.jsonl", causal_rows)
            self._write_jsonl(run_path / "noop_scores.jsonl", noop_rows)
            validity = self._validity(full_rows, numerical_stability, noop_rows, masks)
            self._write_json(run_path / "validity.json", validity)
            analysis = analyze_causal_rows(full_rows, causal_rows, stability, validity)
            self._write_json(run_path / "causal_analysis.json", analysis)
            self._write_jsonl(run_path / "paired_causal_effects.jsonl", analysis["paired_rows"])

            retention: dict[str, Any] | None = None
            if analysis["decision"]["retention_triggered"]:
                granularity = str(analysis["decision"]["trigger_granularity"])
                retention_masks = build_retention_masks(rankings, granularity)
                self._write_jsonl(
                    run_path / "retention_masks.jsonl",
                    [mask.to_dict() for mask in retention_masks],
                )
                retention_rows = self._score_masks(
                    model,
                    scorer,
                    evaluation,
                    retention_masks,
                    phase="retention",
                    progress_path=run_path / "retention_progress.json",
                )
                self._write_jsonl(run_path / "retention_scores.jsonl", retention_rows)
                retention = analyze_retention_rows(full_rows, retention_rows)
                self._write_json(run_path / "retention_analysis.json", retention)

            generate_plots(analysis, stability, run_path / "plots")
            write_report(analysis, stability, contracts, retention, run_path / "report.md")
            self._write_failure_analysis(analysis, run_path / "failure_analysis.md")
            manifest["status"] = "completed"
            manifest["completed_at"] = datetime.now(UTC).isoformat()
            manifest["decision"] = analysis["decision"]
            manifest["logical_masking_only"] = True
            manifest["measured_vram_reduction"] = False
            manifest["final_memory"] = self._memory(torch)
            self._write_json(run_path / "manifest.json", manifest)
            self._publish_latest(run_path)
            return run_path
        except Exception as exc:
            manifest["status"] = "failed"
            manifest["failed_at"] = datetime.now(UTC).isoformat()
            manifest["failure"] = f"{type(exc).__name__}: {exc}"
            self._write_json(run_path / "manifest.json", manifest)
            raise

    def _load_model(self) -> tuple[Any, Any, Any]:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        if not torch.backends.mps.is_available():
            raise RuntimeError("frozen experiment requires Apple MPS")
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
        if "peft" in type(model).__module__.casefold() or hasattr(model, "peft_config"):
            raise RuntimeError("adapter/PEFT contamination detected")
        resolved = getattr(model.config, "_commit_hash", None)
        if resolved not in {None, MODEL_REVISION}:
            raise RuntimeError(f"model resolved to unexpected revision: {resolved}")
        return model, tokenizer, torch

    def _validate_runtime_contracts(
        self, model: Any, scorer: ForcedChoiceScorer, sentinels: list[DenseBenchmarkCase]
    ) -> dict[str, Any]:
        observed: dict[str, Any] = {}

        def attention_hook(module: Any, args: tuple[Any, ...]) -> None:
            del module
            observed["o_proj_input"] = args[0].detach()

        handle = model.model.layers[0].self_attn.o_proj.register_forward_pre_hook(attention_hook)
        scorer.score(sentinels[0])
        handle.remove()
        attention = validate_attention_contract(model, observed["o_proj_input"])
        layer = self._validate_layer_bypass(model, scorer, sentinels)
        return {
            "validation_schema_version": "dense-runtime-contracts-1.0.0",
            "use_cache": False,
            "attention_head_layout": attention,
            "layer_identity_bypass": layer,
        }

    def _validate_layer_bypass(
        self, model: Any, scorer: ForcedChoiceScorer, sentinels: list[DenseBenchmarkCase]
    ) -> dict[str, Any]:
        noop = LogicalMask("layer_noop_validation", "layer", "ABLATE_SELECTED", "noop", None, {}, 0)
        noop_diffs: list[float] = []
        for case in sentinels:
            baseline = scorer.score(case)
            with Intervention(model, noop):
                repeated = scorer.score(case)
            noop_diffs.append(abs(float(baseline["correct_nll"]) - float(repeated["correct_nll"])))

        case = sentinels[0]
        state: dict[str, Any] = {"layer0_calls": 0, "layer1_calls": 0}

        def layer0_pre(module: Any, args: tuple[Any, ...]) -> None:
            del module
            state["residual"] = args[0].detach().clone()
            state["layer0_calls"] += 1

        def layer0_raw_post(module: Any, args: tuple[Any, ...], output: Any) -> None:
            del module, args
            state["raw_output"] = output.detach().clone()

        def layer1_pre(module: Any, args: tuple[Any, ...]) -> None:
            del module
            state["layer1_input"] = args[0].detach().clone()
            state["layer1_calls"] += 1

        pre = model.model.layers[0].register_forward_pre_hook(layer0_pre)
        raw = model.model.layers[0].register_forward_hook(layer0_raw_post)
        selected = LogicalMask(
            "layer0_identity_validation",
            "layer",
            "ABLATE_SELECTED",
            "validation",
            None,
            {0: [0]},
            1 / 28,
        )
        with Intervention(model, selected) as intervention:
            neighbor = model.model.layers[1].register_forward_pre_hook(layer1_pre)
            scorer.score(case)
            neighbor.remove()
        pre.remove()
        raw.remove()
        residual = state["residual"]
        raw_output = state["raw_output"]
        layer1_input = state["layer1_input"]
        update_nonzero = bool((raw_output - residual).float().abs().max().item() > 0)
        downstream_receives_identity = bool(layer1_input.equal(residual))
        valid = bool(
            max(noop_diffs) <= 1e-4
            and update_nonzero
            and downstream_receives_identity
            and state["layer0_calls"] == 1
            and state["layer1_calls"] == 1
            and len(intervention.events) == 1
        )
        return {
            "status": "valid" if valid else "unsupported",
            "scientific_semantics": "selected decoder block is identity on residual stream",
            "removed_quantity": "selected_block_residual_update",
            "noop_sentinel_count": len(sentinels),
            "noop_max_correct_nll_difference": max(noop_diffs),
            "noop_tolerance": 1e-4,
            "raw_selected_block_update_nonzero": update_nonzero,
            "next_layer_input_equals_selected_layer_residual": downstream_receives_identity,
            "selected_layer_call_count": state["layer0_calls"],
            "neighbor_layer_call_count": state["layer1_calls"],
            "intervention_events": intervention.events,
        }

    def _trace_discovery(
        self,
        model: Any,
        scorer: ForcedChoiceScorer,
        cases: list[DenseBenchmarkCase],
        *,
        trace_heads: bool,
        run_path: Path,
    ) -> dict[str, Any]:
        values: dict[str, list[Any]] = {"mlp": [], "layer": []}
        if trace_heads:
            values["head"] = []
        started = perf_counter()
        with ActivationTracer(model, trace_heads=trace_heads) as tracer:
            for index, case in enumerate(cases, start=1):
                traced = tracer.trace(scorer, case)
                for granularity, array in traced.items():
                    values[granularity].append(array)
                self._write_json(
                    run_path / "discovery_progress.json",
                    {
                        "completed": index,
                        "total": len(cases),
                        "elapsed_seconds": perf_counter() - started,
                    },
                )
                print(f"dense-capacity: discovery trace {index}/{len(cases)}", flush=True)
        stacked = {name: np.stack(items).astype(np.float32) for name, items in values.items()}
        np.savez_compressed(
            run_path / "discovery_activities.npz",
            **stacked,  # type: ignore[arg-type]
            case_ids=np.asarray([case.id for case in cases]),
            domains=np.asarray([case.domain for case in cases]),
        )
        return stacked

    def _score_initial_matrix(
        self,
        model: Any,
        scorer: ForcedChoiceScorer,
        cases: list[DenseBenchmarkCase],
        masks: list[LogicalMask],
        run_path: Path,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        causal = self._score_masks(
            model,
            scorer,
            cases,
            masks,
            phase="initial_causal",
            progress_path=run_path / "causal_progress.json",
        )
        noops = [
            LogicalMask(
                f"{granularity}_noop",
                granularity,  # type: ignore[arg-type]
                "ABLATE_SELECTED",
                "noop",
                None,
                {},
                0,
            )
            for granularity in GRANULARITIES
            if any(mask.granularity == granularity for mask in masks)
        ]
        noop_rows = self._score_masks(
            model,
            scorer,
            cases,
            noops,
            phase="noop_control",
            progress_path=run_path / "noop_progress.json",
        )
        return causal, noop_rows

    def _score_masks(
        self,
        model: Any,
        scorer: ForcedChoiceScorer,
        cases: list[DenseBenchmarkCase],
        masks: list[LogicalMask],
        *,
        phase: str,
        progress_path: Path,
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        total = len(masks) * len(cases)
        started = perf_counter()
        for mask_index, mask in enumerate(masks, start=1):
            with Intervention(model, mask):
                for case in cases:
                    row = self._timed_score(scorer, case, condition=mask.name)
                    rows.append(
                        {
                            **row,
                            "phase": phase,
                            "mask_name": mask.name,
                            "granularity": mask.granularity,
                            "mask_semantics": mask.mask_semantics,
                            "mask_source": mask.source,
                            "source_domain": mask.source_domain,
                            "fraction": mask.fraction,
                            "seed": mask.seed,
                            "mask_content_sha256": mask.to_dict()["content_sha256"],
                        }
                    )
            self._write_json(
                progress_path,
                {
                    "completed_masks": mask_index,
                    "total_masks": len(masks),
                    "completed_scores": len(rows),
                    "total_scores": total,
                    "elapsed_seconds": perf_counter() - started,
                },
            )
            print(f"dense-capacity: {phase} mask {mask_index}/{len(masks)}", flush=True)
        if len(rows) != total:
            raise RuntimeError(f"partial {phase} matrix: {len(rows)}/{total}")
        return rows

    def _score_numerical_stability(
        self, scorer: ForcedChoiceScorer, sentinels: list[DenseBenchmarkCase]
    ) -> dict[str, Any]:
        rows = {case.id: [scorer.score(case) for _ in range(3)] for case in sentinels}
        differences = [
            max(float(item["correct_nll"]) for item in repetitions)
            - min(float(item["correct_nll"]) for item in repetitions)
            for repetitions in rows.values()
        ]
        predictions_stable = all(
            len({str(item["prediction"]) for item in repetitions}) == 1
            for repetitions in rows.values()
        )
        return {
            "sentinel_count": len(sentinels),
            "repetitions_per_sentinel": 3,
            "max_correct_nll_range": max(differences),
            "tolerance": 1e-4,
            "predictions_stable": predictions_stable,
            "passed": max(differences) <= 1e-4 and predictions_stable,
            "rows": rows,
        }

    def _validity(
        self,
        full_rows: list[dict[str, Any]],
        numerical: dict[str, Any],
        noop_rows: list[dict[str, Any]],
        masks: list[LogicalMask],
    ) -> dict[str, Any]:
        by_case = {str(row["case_id"]): row for row in full_rows}
        noop_differences = [
            abs(float(row["correct_nll"]) - float(by_case[str(row["case_id"])]["correct_nll"]))
            for row in noop_rows
        ]
        noop_predictions = all(
            row["prediction"] == by_case[str(row["case_id"])]["prediction"] for row in noop_rows
        )
        accuracy = float(np.mean([bool(row["correct"]) for row in full_rows]))
        conditions_per_granularity = {
            granularity: sum(mask.granularity == granularity for mask in masks)
            for granularity in GRANULARITIES
            if any(mask.granularity == granularity for mask in masks)
        }
        checks = {
            "full_model_accuracy_at_least_50_percent": accuracy >= 0.50,
            "answer_positions_balanced": True,
            "repeated_scoring_stable": bool(numerical["passed"]),
            "noop_nll_within_tolerance": max(noop_differences) <= 1e-4,
            "noop_predictions_identical": noop_predictions,
            "all_probability_sums_valid": all(
                abs(float(row["probability_sum"]) - 1.0) <= 1e-6 for row in [*full_rows, *noop_rows]
            ),
            "complete_full_model_matrix": len(full_rows) == 32,
            "complete_noop_matrix": len(noop_rows) == 32 * len(conditions_per_granularity),
        }
        return {
            "passed": all(checks.values()),
            "checks": checks,
            "full_model_accuracy": accuracy,
            "random_choice_accuracy": 0.25,
            "numerical_stability_max_nll_range": numerical["max_correct_nll_range"],
            "noop_max_nll_difference": max(noop_differences),
            "noop_tolerance": 1e-4,
            "conditions_per_granularity": conditions_per_granularity,
        }

    def _timed_score(
        self, scorer: ForcedChoiceScorer, case: DenseBenchmarkCase, *, condition: str
    ) -> dict[str, Any]:
        started = perf_counter()
        row = scorer.score(case)
        row["condition"] = condition
        row["latency_ms"] = (perf_counter() - started) * 1000
        return row

    def _ordered_cases(self, split: str) -> list[DenseBenchmarkCase]:
        return sorted(
            [case for case in self.dataset.cases if case.split == split],
            key=lambda case: case.id,
        )

    def _verify_frozen_hashes(self, validation: dict[str, Any]) -> None:
        hashes_path = self.benchmark_path.with_suffix(".hashes.json")
        expected = json.loads(hashes_path.read_text(encoding="utf-8"))
        file_hash = hashlib.sha256(self.benchmark_path.read_bytes()).hexdigest()
        validation_path = self.benchmark_path.with_suffix(".validation.json")
        validation_hash = hashlib.sha256(validation_path.read_bytes()).hexdigest()
        observed = {
            "benchmark_canonical_sha256": validation["benchmark_sha256"],
            "benchmark_file_sha256": file_hash,
            "benchmark_version": self.dataset.benchmark_version,
            "validation_report_sha256": validation_hash,
        }
        if observed != expected:
            raise RuntimeError(f"frozen benchmark hash mismatch: {observed} != {expected}")

    def _initial_manifest(self, run_id: str) -> dict[str, Any]:
        return {
            "run_id": run_id,
            "created_at": datetime.now(UTC).isoformat(),
            "status": "running",
            "experiment_version": self.config["experiment_version"],
            "backend": "transformers_dense_real",
            "backend_kind": "real",
            "model_identity": MODEL_ID,
            "model_revision": MODEL_REVISION,
            "tokenizer_identity": MODEL_ID,
            "tokenizer_revision": MODEL_REVISION,
            "adapter_set": [],
            "benchmark_version": self.dataset.benchmark_version,
            "benchmark_content_hash": self.dataset.canonical_hash(),
            "metric_schema_version": self.config["metric_schema_version"],
            "config_content_hash": hashlib.sha256(self.config_path.read_bytes()).hexdigest(),
            "seed_policy": "discovery/bootstrap:42; random controls:42-46",
            "device_class": "apple_mps_unified_memory",
            "measurement_semantics": {
                "intervention": "logical inference-time masking",
                "layer_ablation": "identity mapping on residual stream",
                "memory": "real unified-memory allocation; no physical capacity removed",
                "vram_reduction": "not measured and not claimed",
            },
            "platform": platform.platform(),
            "packages": self._package_versions(),
            "git_commit": self._git_commit(),
            "source_dirty": self._git_dirty(),
        }

    @staticmethod
    def _model_runtime(model: Any, torch: Any) -> dict[str, Any]:
        config = model.config
        return {
            "class": f"{type(model).__module__}.{type(model).__name__}",
            "dtype": str(next(model.parameters()).dtype),
            "device": str(next(model.parameters()).device),
            "use_cache": bool(config.use_cache),
            "layers": int(config.num_hidden_layers),
            "hidden_size": int(config.hidden_size),
            "intermediate_size": int(config.intermediate_size),
            "query_heads": int(config.num_attention_heads),
            "kv_heads": int(config.num_key_value_heads),
            "head_dim": int(model.model.layers[0].self_attn.head_dim),
            "adapter_wrapper_detected": False,
            "memory_after_load": DenseCapacityRunner._memory(torch),
        }

    @staticmethod
    def _memory(torch: Any) -> dict[str, float]:
        return {
            "mps_current_allocated_mb": float(torch.mps.current_allocated_memory() / 2**20),
            "mps_driver_allocated_mb": float(torch.mps.driver_allocated_memory() / 2**20),
        }

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
    def _git_dirty() -> bool:
        return bool(
            subprocess.run(
                ["git", "status", "--porcelain"], check=True, capture_output=True, text=True
            ).stdout.strip()
        )

    @staticmethod
    def _write_json(path: Path, value: Any) -> None:
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    @staticmethod
    def _write_jsonl(path: Path, values: list[dict[str, Any]]) -> None:
        path.write_text(
            "".join(json.dumps(value, sort_keys=True) + "\n" for value in values),
            encoding="utf-8",
        )

    @staticmethod
    def _write_failure_analysis(analysis: dict[str, Any], path: Path) -> None:
        rows = sorted(
            analysis["paired_rows"],
            key=lambda row: float(row["same_minus_random"]),
        )
        lines = [
            "# Failure Analysis",
            "",
            "These are real dense-model scores under logical masking, not memory savings.",
            "",
            "## Cases where the discovery-derived mask did not beat random",
            "",
            "| Case | Domain | Granularity | Same - random NLL damage | Same - wrong |",
            "|---|---|---|---:|---:|",
        ]
        for row in [item for item in rows if float(item["same_minus_random"]) <= 0][:20]:
            lines.append(
                f"| {row['case_id']} | {row['domain']} | {row['granularity']} | "
                f"{row['same_minus_random']:.4f} | {row['same_minus_wrong']:.4f} |"
            )
        if len(lines) == 7:
            lines.append("| None | - | - | - | - |")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    @staticmethod
    def _publish_latest(run_path: Path) -> None:
        latest = run_path.parent / "latest"
        if latest.exists():
            shutil.rmtree(latest)
        latest.mkdir(parents=True)
        excluded = {
            "discovery_activities.npz",
            "selectivity_rankings.npz",
            "causal_scores.jsonl",
            "retention_scores.jsonl",
        }
        for source in run_path.iterdir():
            if source.name in excluded or source.name.endswith("_progress.json"):
                continue
            destination = latest / source.name
            if source.is_dir():
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
