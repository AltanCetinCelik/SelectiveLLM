"""Execute the frozen 108-generation expert-quality diagnostic."""

from __future__ import annotations

import csv
import json
import platform
import shutil
import subprocess
from dataclasses import asdict
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

import yaml

from selectivellm.analyzers import DeterministicEmbeddingAnalyzer
from selectivellm.backends.transformers import TransformersPeftBackend
from selectivellm.config import SelectiveLLMConfig
from selectivellm.provenance import stable_fingerprint
from selectivellm.real_validation.assets import ASSETS, verify_compatibility
from selectivellm.real_validation.evaluation import RealBenchmarkDataset, score_response
from selectivellm.real_validation.expert_quality import (
    BOOTSTRAP_RESAMPLES,
    BOOTSTRAP_SEED,
    CONDITIONS,
    EXPERT_TO_CONDITION,
    aggregate_diagnostic,
    generate_heatmap,
    write_matrix,
    write_report,
)
from selectivellm.registry import CapacityRegistry
from selectivellm.routing.hybrid import HybridRouter
from selectivellm.runtime.device import inspect_hardware
from selectivellm.schemas import METRIC_SCHEMA_VERSION

EXPERIMENT_VERSION = "expert-quality-diagnostic-1.0.0"
TECHNICAL_REPETITIONS = 3


class ExpertQualityDiagnosticRunner:
    def __init__(
        self,
        config_path: str | Path = "configs/expert_quality_v012.yaml",
        *,
        results_root: str | Path = "results/real/expert_quality",
    ) -> None:
        self.config_path = Path(config_path).resolve()
        self.config = SelectiveLLMConfig.from_yaml(self.config_path)
        if self.config.backend.type not in {"transformers", "transformers_peft"}:
            raise ValueError("expert-quality diagnostic requires Transformers/PEFT")
        if self.config.backend.max_new_tokens != 384:
            raise ValueError("expert-quality diagnostic requires max_new_tokens=384")
        self.registry = CapacityRegistry.from_yaml(self.config.registry_path or "")
        self.dataset = RealBenchmarkDataset.from_yaml(self.config.benchmark_path or "")
        if len(self.dataset.cases) != 9:
            raise ValueError("expert-quality diagnostic requires exactly nine cases")
        self.results_root = Path(results_root).resolve()

    def run(self, *, run_id: str | None = None) -> Path:
        run_id = run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        run_path = self.results_root / run_id
        if run_path.exists():
            raise FileExistsError(f"run already exists: {run_path}")
        run_path.mkdir(parents=True)

        manifest: dict[str, Any] = {
            "run_id": run_id,
            "created_at": datetime.now(UTC).isoformat(),
            "status": "running",
            "experiment_version": EXPERIMENT_VERSION,
            "backend": "transformers-peft",
            "backend_kind": "real",
            "generation_matrix": {
                "conditions": list(CONDITIONS),
                "cases": len(self.dataset.cases),
                "technical_repetitions": TECHNICAL_REPETITIONS,
                "expected_generations": 108,
                "max_new_tokens": 384,
                "decoding": "greedy",
            },
            "statistical_protocol": {
                "primary_unit": "benchmark_case",
                "cell_aggregate": "arithmetic_mean_over_three_technical_repetitions",
                "bootstrap_unit": "benchmark_case",
                "bootstrap_seed": BOOTSTRAP_SEED,
                "bootstrap_resamples": BOOTSTRAP_RESAMPLES,
                "bootstrap_interval": "percentile_95",
                "tie_absolute_tolerance": 1e-12,
            },
            "decision_gate": {
                "mean_routing_opportunity_threshold": 0.10,
                "strict_improvement_case_threshold": 3,
                "primary_tie_inclusive_win_rate_threshold": 0.60,
            },
            "model_identity": ASSETS[0].repo_id,
            "model_revision": ASSETS[0].revision,
            "adapters": [asdict(asset) for asset in ASSETS[1:]],
            "benchmark_version": self.dataset.benchmark_version,
            "evaluation_schema_version": self.dataset.evaluation_schema_version,
            "metric_schema_version": METRIC_SCHEMA_VERSION,
            "registry_version": self.registry.version,
            "router_version": self.config.router.version,
            "seed": self.config.seed,
            "seed_policy": "fixed:42; greedy decoding; three technical repetitions",
            "git_commit": self._git_commit(),
            "source_dirty": self._git_dirty(),
        }
        self._write_json(run_path / "manifest.json", manifest)

        backend: TransformersPeftBackend | None = None
        rows: list[dict[str, Any]] = []
        try:
            compatibility = verify_compatibility(run_path / "compatibility_report.json")
            hardware = inspect_hardware(self.config.backend.device)
            packages = self._package_versions()
            fingerprint_payload = {
                "experiment_version": EXPERIMENT_VERSION,
                "assets": [asdict(asset) for asset in ASSETS],
                "peft_config_hashes": [
                    adapter["config_sha256"] for adapter in compatibility["adapters"]
                ],
                "benchmark_version": self.dataset.benchmark_version,
                "benchmark_hash": stable_fingerprint(self.dataset.model_dump(mode="json")),
                "evaluation_schema_version": self.dataset.evaluation_schema_version,
                "metric_schema_version": METRIC_SCHEMA_VERSION,
                "registry_version": self.registry.version,
                "registry_hash": stable_fingerprint(self.registry.document.model_dump(mode="json")),
                "router": self.config.router.model_dump(mode="json"),
                "generation_matrix": manifest["generation_matrix"],
                "statistical_protocol": manifest["statistical_protocol"],
                "decision_gate": manifest["decision_gate"],
                "device": hardware.to_dict(),
                "packages": packages,
                "platform": platform.platform(),
            }
            manifest.update(
                {
                    "device": hardware.to_dict(),
                    "packages": packages,
                    "benchmark_content_hash": fingerprint_payload["benchmark_hash"],
                    "registry_content_hash": fingerprint_payload["registry_hash"],
                    "benchmark_fingerprint": stable_fingerprint(fingerprint_payload),
                    "fingerprint_payload": fingerprint_payload,
                    "measurement_semantics": {
                        "quality": "fixed deterministic rubric over real model generations",
                        "expert_capacity": "one real PEFT LoRA active for specialist conditions",
                        "memory": "not a memory benchmark; no memory conclusion is drawn",
                    },
                }
            )
            self._write_json(run_path / "manifest.json", manifest)
            self._snapshot_inputs(run_path, hardware.to_dict(), packages)

            semantic_routes = self._semantic_routes()
            self._write_jsonl(run_path / "semantic_routes.jsonl", semantic_routes)

            backend = TransformersPeftBackend(self.config.backend)
            base = self.registry.base_components()[0]
            backend.load_component(base)
            backend.synchronize()
            experts = {component.id: component for component in self.registry.routable_components()}
            condition_experts = {
                condition: expert for expert, condition in EXPERT_TO_CONDITION.items()
            }

            active_expert: str | None = None
            completed = 0
            for condition in CONDITIONS:
                if active_expert is not None:
                    backend.activate_adapters([])
                    backend.unload_component(experts[active_expert])
                    active_expert = None
                expert_id = condition_experts.get(condition)
                if expert_id is not None:
                    backend.load_component(experts[expert_id])
                    backend.activate_adapters([expert_id])
                    active_expert = expert_id
                else:
                    backend.activate_adapters([])

                for case in self.dataset.cases:
                    primary = case.expected_experts[0] if case.expected_experts else None
                    wrong_experts = [
                        expert
                        for expert in EXPERT_TO_CONDITION
                        if expert not in case.expected_experts
                    ]
                    for repetition in range(1, TECHNICAL_REPETITIONS + 1):
                        output = backend.generate(
                            case.prompt,
                            [experts[expert_id]] if expert_id is not None else [],
                        )
                        quality, evaluation = score_response(case, output.text)
                        truncated = output.token_count == self.config.backend.max_new_tokens
                        row = {
                            "run_backend": "transformers-peft",
                            "backend_kind": "real",
                            "condition": condition,
                            "active_expert": expert_id,
                            "resident_adapters": output.metadata["resident_adapters"],
                            "active_adapters": output.metadata["active_adapters"],
                            "case_id": case.id,
                            "prompt": case.prompt,
                            "expected_experts": list(case.expected_experts),
                            "correct_labeled_expert": primary,
                            "wrong_experts": wrong_experts,
                            "repetition": repetition,
                            "response": output.text,
                            "quality": quality,
                            "evaluation_details": evaluation,
                            "token_count": output.token_count,
                            "max_new_tokens": self.config.backend.max_new_tokens,
                            "truncated": truncated,
                            "eos_completed": not truncated,
                            "first_token_ms": output.first_token_ms,
                            "generation_ms": output.generation_ms,
                        }
                        rows.append(row)
                        completed += 1
                        self._write_jsonl(run_path / "raw_generations.partial.jsonl", rows)
                        print(f"completed {completed}/108", flush=True)

            if active_expert is not None:
                backend.activate_adapters([])
                backend.unload_component(experts[active_expert])

            cells, case_analysis, summary = aggregate_diagnostic(
                rows, self.dataset.cases, semantic_routes
            )
            if not summary["completion"]["complete"]:
                raise RuntimeError("diagnostic completion invariant failed")
            summary["run_id"] = run_id
            summary["benchmark_fingerprint"] = manifest["benchmark_fingerprint"]

            self._write_jsonl(run_path / "raw_generations.jsonl", rows)
            self._write_jsonl(run_path / "cell_aggregates.jsonl", cells)
            self._write_jsonl(run_path / "case_analysis.jsonl", case_analysis)
            mismatches = [
                item
                for item in case_analysis
                if item["correct_labeled_expert"] is not None
                and not bool(item["primary_tie_inclusive_win"])
            ]
            self._write_jsonl(run_path / "label_mismatches.jsonl", mismatches)
            self._write_json(run_path / "summary.json", summary)
            self._write_summary_csv(summary, run_path / "summary.csv")
            write_matrix(case_analysis, run_path / "expert_specialization_matrix.csv")
            generate_heatmap(case_analysis, run_path / "expert_specialization_heatmap.png")
            write_report(summary, case_analysis, manifest, run_path / "report.md")
            manifest.update(
                {
                    "status": "completed",
                    "completed_at": datetime.now(UTC).isoformat(),
                    "observed_generations": len(rows),
                    "observed_cells": len(cells),
                    "decision_gate_classification": summary["decision_gate"]["classification"],
                }
            )
            self._write_json(run_path / "manifest.json", manifest)
            (run_path / "raw_generations.partial.jsonl").unlink(missing_ok=True)
            self._publish_latest(run_path)
            return run_path
        except Exception as exc:
            manifest["status"] = "failed"
            manifest["failure"] = f"{type(exc).__name__}: {exc}"
            manifest["observed_generations"] = len(rows)
            self._write_json(run_path / "manifest.json", manifest)
            raise
        finally:
            if backend is not None:
                backend.cleanup_allocator()

    def _semantic_routes(self) -> list[dict[str, Any]]:
        analyzer = DeterministicEmbeddingAnalyzer(self.config.analyzer.dimension)
        router = HybridRouter(
            dimension=self.config.analyzer.dimension,
            top_k=self.config.router.top_k,
            threshold=self.config.router.threshold,
            embedding_weight=self.config.router.embedding_weight,
            keyword_weight=self.config.router.keyword_weight,
        )
        routes: list[dict[str, Any]] = []
        for case in self.dataset.cases:
            profile = analyzer.analyze(case.prompt)
            decision = router.route(profile, self.registry)
            routes.append(
                {
                    "case_id": case.id,
                    "expected_experts": list(case.expected_experts),
                    "selected_experts": list(decision.selected),
                    "first_selected_expert": (decision.selected[0] if decision.selected else None),
                    "confidence": decision.confidence,
                    "candidate_scores": {
                        candidate.component_id: candidate.score for candidate in decision.candidates
                    },
                    "profile": profile.model_dump(mode="json"),
                    "routing": decision.model_dump(mode="json"),
                }
            )
        return routes

    def _snapshot_inputs(
        self, run_path: Path, hardware: dict[str, Any], packages: dict[str, str | None]
    ) -> None:
        shutil.copy2(self.config_path, run_path / "config.source.yaml")
        shutil.copy2(self.config.registry_path or "", run_path / "registry.yaml")
        shutil.copy2(self.config.benchmark_path or "", run_path / "benchmark.yaml")
        saved_config = yaml.safe_load(self.config_path.read_text(encoding="utf-8"))
        saved_config["registry_path"] = "./registry.yaml"
        saved_config["benchmark_path"] = "./benchmark.yaml"
        (run_path / "config.yaml").write_text(
            yaml.safe_dump(saved_config, sort_keys=False), encoding="utf-8"
        )
        self._write_json(
            run_path / "environment.json",
            {**hardware, "platform": platform.platform(), "packages": packages},
        )

    def _publish_latest(self, run_path: Path) -> None:
        latest = self.results_root / "latest"
        if latest.exists():
            shutil.rmtree(latest)
        shutil.copytree(run_path, latest)

    @staticmethod
    def _write_summary_csv(summary: dict[str, Any], path: Path) -> None:
        rows: list[dict[str, Any]] = []
        for section in ("conditions", "policies", "policy_delta_base", "metrics"):
            for name, stats in summary[section].items():
                rows.append({"section": section, "name": name, **stats})
        columns = sorted({key for row in rows for key in row})
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)

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
    def _package_versions() -> dict[str, str | None]:
        output: dict[str, str | None] = {}
        for package in (
            "selectivellm",
            "torch",
            "transformers",
            "peft",
            "accelerate",
            "huggingface-hub",
            "safetensors",
            "numpy",
        ):
            try:
                output[package] = version(package)
            except PackageNotFoundError:
                output[package] = None
        return output

    @staticmethod
    def _git_commit() -> str | None:
        try:
            return subprocess.check_output(
                ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
            ).strip()
        except (OSError, subprocess.CalledProcessError):
            return None

    @staticmethod
    def _git_dirty() -> bool:
        try:
            output = subprocess.check_output(
                ["git", "status", "--porcelain"], text=True, stderr=subprocess.DEVNULL
            )
            return bool(output.strip())
        except (OSError, subprocess.CalledProcessError):
            return True
