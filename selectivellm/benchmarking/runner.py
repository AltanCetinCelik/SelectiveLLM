"""Hero benchmark runner with baselines, ablations, provenance, and failure output."""

from __future__ import annotations

import json
import platform
import shutil
import subprocess
from collections import defaultdict
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import as_file, files
from pathlib import Path
from typing import Any

import yaml

from selectivellm.benchmarking.dataset import load_dataset
from selectivellm.benchmarking.evaluation import output_quality, routing_scores
from selectivellm.benchmarking.report import generate_plots, write_report, write_summary_csv
from selectivellm.config import SelectiveLLMConfig
from selectivellm.engine import SelectiveLLM
from selectivellm.metrics import aggregate
from selectivellm.provenance import benchmark_fingerprint, stable_fingerprint
from selectivellm.registry import CapacityRegistry
from selectivellm.routing import create_router
from selectivellm.runtime.device import inspect_hardware
from selectivellm.schemas import METRIC_SCHEMA_VERSION, RunManifest

DEFAULT_METHODS = [
    "base_only",
    "random",
    "keyword",
    "oracle",
    "embedding",
    "semantic_top1",
    "semantic",
    "semantic_threshold_high",
    "semantic_cache",
    "semantic_cache_small",
    "all_resident",
]


class BenchmarkRunner:
    def __init__(
        self,
        config: SelectiveLLMConfig,
        *,
        dataset_path: str | Path | None = None,
        results_root: str | Path = "results",
    ) -> None:
        self.config = config
        if dataset_path is None:
            if config.benchmark_path:
                dataset_path = config.benchmark_path
            else:
                resource = files("selectivellm.resources").joinpath("hero_v1.yaml")
                with as_file(resource) as path:
                    dataset_path = Path(path)
        self.dataset = load_dataset(dataset_path)
        self.results_root = Path(results_root).resolve()

    def run(
        self,
        *,
        methods: list[str] | None = None,
        repetitions: int = 1,
        report: bool = True,
        run_id: str | None = None,
    ) -> Path:
        if repetitions < 1:
            raise ValueError("repetitions must be at least one")
        active_methods = methods or DEFAULT_METHODS
        run_id = run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        run_path = self.results_root / run_id
        if run_path.exists():
            raise FileExistsError(f"run already exists: {run_path}")
        run_path.mkdir(parents=True)

        hardware = inspect_hardware(self.config.backend.device)
        registry = self._load_registry()
        seed_policy = (
            f"fixed-base-seed:{self.config.seed}; deterministic-case-derived random baseline"
        )
        compatibility = {
            "backend": self._backend_name(),
            "backend_kind": "control" if self.config.backend.type == "deterministic" else "real",
            "model_identity": self.config.backend.model_path or "selectivellm-control-v1",
            "adapter_set": sorted(component.id for component in registry.routable_components()),
            "benchmark_version": self.dataset.benchmark_version,
            "benchmark_content_hash": stable_fingerprint(self.dataset.model_dump(mode="json")),
            "registry_version": registry.version,
            "registry_content_hash": stable_fingerprint(registry.document.model_dump(mode="json")),
            "routing_config_version": self.config.router.version,
            "routing_config_hash": stable_fingerprint(self.config.router.model_dump(mode="json")),
            "metric_schema_version": METRIC_SCHEMA_VERSION,
            "seed_policy": seed_policy,
            "device_class": hardware.device_class,
            "measurement_semantics": "declared_capacity_plus_observed_process_and_accelerator",
        }
        fingerprint = benchmark_fingerprint(**compatibility)
        manifest = RunManifest(
            run_id=run_id,
            status="running",
            benchmark_fingerprint=fingerprint,
            configuration_fingerprint=stable_fingerprint(
                {**compatibility, "methods": active_methods, "repetitions": repetitions}
            ),
            git_commit=self._git_commit(),
            source_dirty=self._git_dirty(),
            **compatibility,
        )
        self._write_json(run_path / "manifest.json", manifest.model_dump(mode="json"))
        config_payload = self.config.model_dump(mode="json")
        config_payload["experiment"] = {
            "methods": active_methods,
            "repetitions": repetitions,
            "benchmark_version": self.dataset.benchmark_version,
        }
        (run_path / "config.yaml").write_text(
            yaml.safe_dump(config_payload, sort_keys=False), encoding="utf-8"
        )
        environment = {
            **hardware.to_dict(),
            "platform": platform.platform(),
            "packages": self._package_versions(),
            "git_commit": manifest.git_commit,
            "source_dirty": manifest.source_dirty,
        }
        self._write_json(run_path / "environment.json", environment)

        rows: list[dict[str, Any]] = []
        decisions: list[dict[str, Any]] = []
        for method in active_methods:
            engine = self._engine_for(method)
            for repetition in range(repetitions):
                for case in self.dataset.cases:
                    allow_over_budget = method in {"oracle", "all_resident"}
                    result = engine.generate(
                        case.prompt,
                        expected_experts=case.expected_experts if method == "oracle" else None,
                        allow_over_budget=allow_over_budget,
                    )
                    selected_experts = [item for item in result.plan.selected if item != "base"]
                    routing = routing_scores(case.expected_experts, selected_experts)
                    quality, quality_semantics = output_quality(
                        case,
                        result.text,
                        selected_experts,
                        backend_kind=result.backend_kind,
                    )
                    requests = result.metrics.cache_hits + result.metrics.cache_misses
                    row = {
                        "run_id": run_id,
                        "benchmark_fingerprint": fingerprint,
                        "backend": result.backend,
                        "backend_kind": result.backend_kind,
                        "model_identity": result.model_identity,
                        "backend_metadata": result.backend_metadata,
                        "benchmark_version": self.dataset.benchmark_version,
                        "registry_version": registry.version,
                        "metric_schema_version": METRIC_SCHEMA_VERSION,
                        "method": method,
                        "repetition": repetition,
                        "case_id": case.id,
                        "prompt": case.prompt,
                        "tags": case.tags,
                        "expected_experts": case.expected_experts,
                        "selected_experts": selected_experts,
                        "candidate_scores": {
                            item.component_id: item.score for item in result.routing.candidates
                        },
                        "rejected_experts": result.plan.rejected,
                        "routing_confidence": result.routing.confidence,
                        "routing_precision": routing["precision"],
                        "routing_recall": routing["recall"],
                        "routing_f1": routing["f1"],
                        "top1_accuracy": routing["top1_accuracy"],
                        "topk_recall": routing["topk_recall"],
                        "false_activations": routing["false_activations"],
                        "quality": quality,
                        "quality_semantics": quality_semantics,
                        "routing_ms": result.metrics.routing_ms,
                        "planning_ms": result.metrics.planning_ms,
                        "loading_ms": result.metrics.loading_ms,
                        "inference_ms": result.metrics.inference_ms,
                        "first_token_ms": result.metrics.first_token_ms,
                        "end_to_end_ms": result.metrics.end_to_end_ms,
                        "tokens_per_second": result.metrics.tokens_per_second,
                        "cache_hits": result.metrics.cache_hits,
                        "cache_misses": result.metrics.cache_misses,
                        "cache_hit_rate": result.metrics.cache_hits / requests if requests else 0.0,
                        "expert_swaps": result.metrics.expert_swaps,
                        "declared_resident_capacity_mb": result.memory.declared_resident_capacity_mb,
                        "declared_peak_capacity_mb": result.memory.declared_peak_capacity_mb,
                        "declared_base_capacity_mb": result.memory.declared_base_capacity_mb,
                        "declared_expert_capacity_mb": result.memory.declared_expert_capacity_mb,
                        "host_rss_mb": result.memory.host_rss_mb,
                        "accelerator_peak_allocated_mb": result.memory.accelerator_peak_allocated_mb,
                        "accelerator_measurement_available": result.memory.accelerator_measurement_available,
                        "measurement_semantics": result.memory.measurement_semantics,
                        "output": result.text,
                    }
                    rows.append(row)
                    decisions.append(
                        {
                            "method": method,
                            "repetition": repetition,
                            "case_id": case.id,
                            "profile": result.profile.model_dump(mode="json"),
                            "routing": result.routing.model_dump(mode="json"),
                            "plan": result.plan.model_dump(mode="json"),
                            "runtime_events": [
                                event.model_dump(mode="json") for event in result.runtime_events
                            ],
                        }
                    )
            engine.runtime.clear()

        self._add_relative_metrics(rows)
        self._write_jsonl(run_path / "raw_results.jsonl", rows)
        self._write_jsonl(run_path / "routing_decisions.jsonl", decisions)
        summary = self._summarize(rows, manifest)
        self._write_json(run_path / "summary.json", summary)
        write_summary_csv(summary, run_path / "summary.csv")
        self._write_failures(rows, run_path / "routing_failures.md")
        if report:
            generate_plots(summary, rows, run_path / "plots")
            write_report(
                summary, manifest.model_dump(mode="json"), environment, run_path / "report.md"
            )
        manifest.status = "completed"
        self._write_json(run_path / "manifest.json", manifest.model_dump(mode="json"))
        self._publish_latest(run_path)
        return run_path

    def _engine_for(self, method: str) -> SelectiveLLM:
        config = self.config.model_copy(deep=True)
        mapping = {
            "base_only": "base_only",
            "random": "random",
            "keyword": "keyword",
            "oracle": "oracle",
            "embedding": "embedding",
            "semantic_top1": "hybrid",
            "semantic": "hybrid",
            "semantic_threshold_high": "hybrid",
            "semantic_cache": "hybrid",
            "semantic_cache_small": "hybrid",
            "all_resident": "all_resident",
        }
        if method not in mapping:
            raise ValueError(f"unsupported benchmark method: {method}")
        config.router.type = mapping[method]
        if method == "semantic_top1":
            config.router.top_k = 1
        if method == "semantic_threshold_high":
            config.router.threshold = 0.4
        if method == "semantic_cache_small":
            config.runtime.memory_budget_mb = 680
        config.runtime.cache_enabled = method in {
            "semantic_cache",
            "semantic_cache_small",
            "all_resident",
        }
        router = create_router(config.router, seed=config.seed, dimension=config.analyzer.dimension)
        return SelectiveLLM.from_config(config=config, router=router)

    def _load_registry(self) -> CapacityRegistry:
        if self.config.registry_path:
            return CapacityRegistry.from_yaml(self.config.registry_path)
        resource = files("selectivellm.resources").joinpath("registry.yaml")
        with as_file(resource) as path:
            return CapacityRegistry.from_yaml(path)

    def _summarize(self, rows: list[dict[str, Any]], manifest: RunManifest) -> dict[str, Any]:
        metrics = [
            "quality",
            "routing_precision",
            "routing_recall",
            "routing_f1",
            "top1_accuracy",
            "topk_recall",
            "false_activations",
            "routing_ms",
            "planning_ms",
            "loading_ms",
            "inference_ms",
            "first_token_ms",
            "end_to_end_ms",
            "tokens_per_second",
            "cache_hit_rate",
            "expert_swaps",
            "declared_resident_capacity_mb",
            "declared_peak_capacity_mb",
            "declared_memory_reduction",
            "accelerator_memory_reduction",
            "quality_retention",
            "host_rss_mb",
        ]
        grouped: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            grouped[row["method"]].append(row)
        methods: dict[str, Any] = {}
        for method, observations in grouped.items():
            methods[method] = {}
            for metric in metrics:
                values = [row[metric] for row in observations if row.get(metric) is not None]
                methods[method][metric] = aggregate(values).model_dump(mode="json")
        return {
            "run_id": manifest.run_id,
            "backend": manifest.backend,
            "backend_kind": manifest.backend_kind,
            "benchmark_version": manifest.benchmark_version,
            "benchmark_fingerprint": manifest.benchmark_fingerprint,
            "quality_semantics": sorted({row["quality_semantics"] for row in rows}),
            "comparison_validity": "all rows share one benchmark fingerprint",
            "methods": methods,
        }

    @staticmethod
    def _add_relative_metrics(rows: list[dict[str, Any]]) -> None:
        oracle_quality = {
            (row["repetition"], row["case_id"]): row["quality"]
            for row in rows
            if row["method"] == "oracle"
        }
        all_resident_declared = {
            (row["repetition"], row["case_id"]): row["declared_peak_capacity_mb"]
            for row in rows
            if row["method"] == "all_resident"
        }
        all_resident_accelerator = {
            (row["repetition"], row["case_id"]): row["accelerator_peak_allocated_mb"]
            for row in rows
            if row["method"] == "all_resident" and row["accelerator_peak_allocated_mb"] is not None
        }
        for row in rows:
            key = (row["repetition"], row["case_id"])
            oracle = oracle_quality.get(key)
            declared = all_resident_declared.get(key)
            accelerator = all_resident_accelerator.get(key)
            row["quality_retention"] = (
                row["quality"] / oracle if oracle is not None and oracle > 0 else None
            )
            row["declared_memory_reduction"] = (
                1 - row["declared_peak_capacity_mb"] / declared
                if declared is not None and declared > 0
                else None
            )
            row["accelerator_memory_reduction"] = (
                1 - row["accelerator_peak_allocated_mb"] / accelerator
                if accelerator is not None
                and accelerator > 0
                and row["accelerator_peak_allocated_mb"] is not None
                else None
            )

    def _write_failures(self, rows: list[dict[str, Any]], path: Path) -> None:
        base_quality = {
            (row["repetition"], row["case_id"]): row["quality"]
            for row in rows
            if row["method"] == "base_only"
        }
        lines = [
            "# Routing Failure Analysis",
            "",
            "Failures are retained by policy. Scores below are backend-specific and must be read with the run manifest.",
            "",
        ]
        failures = 0
        for row in rows:
            if row["method"] in {"base_only", "oracle", "all_resident"}:
                continue
            reasons: list[str] = []
            if row["expected_experts"] and row["routing_recall"] < 1:
                reasons.append("missing required expert")
            if row["false_activations"] > 0:
                reasons.append("unnecessary expert activation")
            rejected_relevant = sorted(set(row["expected_experts"]) & set(row["rejected_experts"]))
            if rejected_relevant:
                reasons.append("relevant expert rejected by memory budget")
            if row["routing_confidence"] < 0.3:
                reasons.append("low confidence")
            baseline = base_quality.get((row["repetition"], row["case_id"]))
            if row["routing_recall"] == 1 and baseline is not None and row["quality"] <= baseline:
                reasons.append("correct routing did not improve output quality")
            if not reasons:
                continue
            failures += 1
            lines.extend(
                [
                    f"## {row['method']} / {row['case_id']} / repetition {row['repetition']}",
                    "",
                    f"**Prompt:** {row['prompt']}",
                    "",
                    f"**Expected:** `{row['expected_experts']}`",
                    f"**Selected:** `{row['selected_experts']}`",
                    f"**Confidence:** `{row['routing_confidence']:.3f}`",
                    f"**Scores:** `{row['candidate_scores']}`",
                    f"**Quality:** `{row['quality']:.3f}` (`{row['quality_semantics']}`)",
                    f"**Possible reason:** {', '.join(reasons)}",
                    "",
                ]
            )
        if failures == 0:
            lines.append("No configured failure condition was observed in this run.\n")
        path.write_text("\n".join(lines), encoding="utf-8")

    def _publish_latest(self, run_path: Path) -> None:
        latest = self.results_root / "latest"
        if latest.exists():
            shutil.rmtree(latest)
        shutil.copytree(run_path, latest)

    def _backend_name(self) -> str:
        return (
            "deterministic-control"
            if self.config.backend.type == "deterministic"
            else "transformers-peft"
        )

    @staticmethod
    def _write_json(path: Path, payload: Any) -> None:
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    @staticmethod
    def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
        path.write_text(
            "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
            encoding="utf-8",
        )

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

    @staticmethod
    def _package_versions() -> dict[str, str | None]:
        packages = [
            "selectivellm",
            "pydantic",
            "numpy",
            "matplotlib",
            "psutil",
            "torch",
            "transformers",
            "peft",
        ]
        versions: dict[str, str | None] = {}
        for package in packages:
            try:
                versions[package] = version(package)
            except PackageNotFoundError:
                versions[package] = None
        return versions
