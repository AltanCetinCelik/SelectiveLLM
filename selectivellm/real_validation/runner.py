"""End-to-end v0.1.1 real-model benchmark runner."""

from __future__ import annotations

import json
import platform
import shutil
import subprocess
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from time import perf_counter
from typing import Any

from selectivellm.analyzers import DeterministicEmbeddingAnalyzer
from selectivellm.backends.transformers import TransformersPeftBackend
from selectivellm.benchmarking.evaluation import routing_scores
from selectivellm.config import SelectiveLLMConfig
from selectivellm.provenance import stable_fingerprint
from selectivellm.real_validation.assets import ASSETS, verify_compatibility
from selectivellm.real_validation.evaluation import (
    RealBenchmarkCase,
    RealBenchmarkDataset,
    score_response,
)
from selectivellm.real_validation.report import (
    generate_plots,
    summarize,
    write_report,
    write_summary_csv,
)
from selectivellm.real_validation.runtime import AdapterResidencyManager, memory_checkpoint
from selectivellm.registry import CapacityRegistry
from selectivellm.routing.baselines import BaseOnlyRouter, KeywordRouter, OracleRouter, RandomRouter
from selectivellm.routing.hybrid import HybridRouter
from selectivellm.runtime.device import inspect_hardware
from selectivellm.schemas import CapacityComponent


@dataclass(frozen=True)
class Policy:
    name: str
    router: str
    locality: str
    cache_size: int
    all_resident: bool = False


POLICIES = (
    Policy("base_only", "base", "low", 0),
    Policy("random", "random", "low", 0),
    Policy("keyword", "keyword", "low", 0),
    Policy("oracle", "oracle", "low", 0),
    Policy("semantic_cache0_low", "semantic", "low", 0),
    Policy("semantic_cache1_low", "semantic", "low", 1),
    Policy("semantic_cache3_low", "semantic", "low", 3),
    Policy("all_resident", "semantic", "low", 3, all_resident=True),
    Policy("semantic_cache0_high", "semantic", "high", 0),
    Policy("semantic_cache1_high", "semantic", "high", 1),
    Policy("semantic_cache3_high", "semantic", "high", 3),
)


class RealBenchmarkRunner:
    def __init__(
        self,
        config_path: str | Path = "configs/real_v011.yaml",
        *,
        results_root: str | Path = "results/real",
    ) -> None:
        self.config_path = Path(config_path).resolve()
        self.config = SelectiveLLMConfig.from_yaml(self.config_path)
        if self.config.backend.type not in {"transformers", "transformers_peft"}:
            raise ValueError("real validation requires the Transformers/PEFT backend")
        self.registry = CapacityRegistry.from_yaml(self.config.registry_path or "")
        self.dataset = RealBenchmarkDataset.from_yaml(self.config.benchmark_path or "")
        self.results_root = Path(results_root).resolve()
        self.analyzer = DeterministicEmbeddingAnalyzer(self.config.analyzer.dimension)

    def run(self, *, warm_repetitions: int = 3, run_id: str | None = None) -> Path:
        if warm_repetitions < 1:
            raise ValueError("warm_repetitions must be at least one")
        run_id = run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        run_path = self.results_root / run_id
        if run_path.exists():
            raise FileExistsError(f"run already exists: {run_path}")
        run_path.mkdir(parents=True)

        telemetry: list[dict[str, Any]] = [memory_checkpoint("process_start", None)]
        compatibility = verify_compatibility(run_path / "compatibility_report.json")
        hardware = inspect_hardware(self.config.backend.device)
        packages = self._package_versions()
        fingerprint_payload = {
            "assets": [asdict(asset) for asset in ASSETS],
            "peft_config_hashes": [
                adapter["config_sha256"] for adapter in compatibility["adapters"]
            ],
            "benchmark_version": self.dataset.benchmark_version,
            "benchmark_hash": stable_fingerprint(self.dataset.model_dump(mode="json")),
            "evaluation_schema_version": self.dataset.evaluation_schema_version,
            "router": self.config.router.model_dump(mode="json"),
            "runtime": {
                "policies": [asdict(policy) for policy in POLICIES],
                "warm_repetitions": warm_repetitions,
                "max_active_experts": 2,
            },
            "packages": packages,
            "device": hardware.to_dict(),
            "platform": platform.platform(),
        }
        manifest: dict[str, Any] = {
            "run_id": run_id,
            "created_at": datetime.now(UTC).isoformat(),
            "status": "running",
            "backend": "transformers-peft",
            "backend_kind": "real",
            "model_identity": ASSETS[0].repo_id,
            "model_revision": ASSETS[0].revision,
            "tokenizer_identity": ASSETS[0].repo_id,
            "tokenizer_revision": ASSETS[0].revision,
            "adapters": [asdict(asset) for asset in ASSETS[1:]],
            "benchmark_version": self.dataset.benchmark_version,
            "evaluation_schema_version": self.dataset.evaluation_schema_version,
            "registry_version": self.registry.version,
            "seed": self.config.seed,
            "seed_policy": "fixed:42; greedy decoding; deterministic prompt-derived random routing",
            "device": hardware.to_dict(),
            "packages": packages,
            "measurement_semantics": {
                "host_rss_mb": "process RSS on unified memory",
                "mps_current_allocated_mb": "live tensor allocation excluding allocator cache",
                "mps_driver_allocated_mb": "Metal driver allocation including cache/framework",
                "generation_peak": "5 ms sampled peak; not a CUDA peak counter",
            },
            "benchmark_fingerprint": stable_fingerprint(fingerprint_payload),
            "fingerprint_payload": fingerprint_payload,
            "git_commit": self._git_commit(),
            "source_dirty": self._git_dirty(),
        }
        self._write_json(run_path / "manifest.json", manifest)
        shutil.copy2(self.config_path, run_path / "config.yaml")
        self._write_json(
            run_path / "environment.json",
            {**hardware.to_dict(), "platform": platform.platform(), "packages": packages},
        )

        backend = TransformersPeftBackend(self.config.backend)
        telemetry.append(memory_checkpoint("before_base_load", backend))
        base = self.registry.base_components()[0]
        base_started = perf_counter()
        backend.load_component(base)
        backend.synchronize()
        manifest["base_load_ms"] = (perf_counter() - base_started) * 1000
        telemetry.append(memory_checkpoint("base_loaded", backend))
        self._write_json(run_path / "manifest.json", manifest)

        experts = {component.id: component for component in self.registry.routable_components()}
        rows: list[dict[str, Any]] = []
        decisions: list[dict[str, Any]] = []
        active_context: dict[str, str | None] = {"policy": None, "case_id": None, "phase": None}

        def checkpoint(label: str) -> None:
            telemetry.append(memory_checkpoint(label, backend, **active_context))

        manager = AdapterResidencyManager(backend, experts, cache_size=0, checkpoint=checkpoint)
        try:
            for policy in POLICIES:
                active_context.update(policy=policy.name, case_id=None, phase="policy_reset")
                manager.clear()
                backend.cleanup_allocator()
                checkpoint("after_intentional_policy_cleanup")
                manager = AdapterResidencyManager(
                    backend, experts, cache_size=policy.cache_size, checkpoint=checkpoint
                )
                if policy.all_resident:
                    manager.ensure(experts, retain_all=True)
                    checkpoint("all_adapters_resident")

                cases = self.dataset.ordered(policy.locality)
                for repetition in range(warm_repetitions + 1):
                    phase = "cold_workload" if repetition == 0 else "warm"
                    for sequence_index, case in enumerate(cases):
                        active_context.update(policy=policy.name, case_id=case.id, phase=phase)
                        row, decision = self._run_case(
                            backend,
                            manager,
                            policy,
                            case,
                            repetition,
                            sequence_index,
                            checkpoint,
                        )
                        rows.append(row)
                        decisions.append(decision)
                self._write_jsonl(run_path / "raw_results.partial.jsonl", rows)
                self._write_jsonl(run_path / "telemetry.partial.jsonl", telemetry)

            self._add_relative_quality(rows)
            rlc_rows = self._run_rlc_matrix(
                backend, manager, rows, experts, warm_repetitions, telemetry
            )
            summary = summarize(rows, manifest)
            self._write_jsonl(run_path / "raw_results.jsonl", rows)
            self._write_jsonl(
                run_path / "raw_responses.jsonl", [self._response_row(row) for row in rows]
            )
            self._write_jsonl(run_path / "routing_decisions.jsonl", decisions)
            self._write_jsonl(run_path / "telemetry.jsonl", telemetry)
            self._write_jsonl(run_path / "rlc_matrix.jsonl", rlc_rows)
            self._write_jsonl(
                run_path / "evaluation_outputs.jsonl",
                [
                    {
                        "policy": row["policy"],
                        "phase": row["phase"],
                        "repetition": row["repetition"],
                        "case_id": row["case_id"],
                        "quality": row["quality"],
                        "evaluation": row["evaluation_details"],
                    }
                    for row in rows
                ],
            )
            self._write_json(run_path / "summary.json", summary)
            write_summary_csv(summary, run_path / "summary.csv")
            self._write_failures(rows, rlc_rows, run_path / "failure_analysis.md")
            generate_plots(summary, run_path / "plots")
            write_report(summary, manifest, run_path / "report.md")
            manifest["status"] = "completed"
            manifest["completed_at"] = datetime.now(UTC).isoformat()
            self._write_json(run_path / "manifest.json", manifest)
            self._publish_latest(run_path)
        except Exception as exc:
            manifest["status"] = "failed"
            manifest["failure"] = f"{type(exc).__name__}: {exc}"
            self._write_json(run_path / "manifest.json", manifest)
            self._write_jsonl(run_path / "telemetry.partial.jsonl", telemetry)
            raise
        return run_path

    def _run_case(
        self,
        backend: TransformersPeftBackend,
        manager: AdapterResidencyManager,
        policy: Policy,
        case: RealBenchmarkCase,
        repetition: int,
        sequence_index: int,
        checkpoint: Any,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        total_started = perf_counter()
        profile = self.analyzer.analyze(case.prompt)
        router = self._router(policy.router, repetition)
        routing = router.route(
            profile,
            self.registry,
            expected_experts=case.expected_experts if policy.router == "oracle" else None,
        )
        plan_started = perf_counter()
        selected = list(routing.selected)
        rejected: dict[str, str] = {}
        if policy.router != "oracle" and len(selected) > 2:
            rejected = {item: "active_expert_limit" for item in selected[2:]}
            selected = selected[:2]
        planning_ms = (perf_counter() - plan_started) * 1000

        checkpoint("before_adapter_prepare")
        events = manager.ensure(selected, retain_all=policy.all_resident)
        activation = backend.activate_adapters(selected)
        checkpoint("immediately_before_generation")
        before = memory_checkpoint(
            "row_before_generation",
            backend,
            policy=policy.name,
            case_id=case.id,
            phase="cold_workload" if repetition == 0 else "warm",
        )
        sync_started = perf_counter()
        backend.synchronize()
        boundary_sync_ms = (perf_counter() - sync_started) * 1000
        output = backend.generate(case.prompt, [self.registry.get(item) for item in selected])
        sync_started = perf_counter()
        backend.synchronize()
        boundary_sync_ms += (perf_counter() - sync_started) * 1000
        after = memory_checkpoint(
            "immediately_after_generation",
            backend,
            policy=policy.name,
            case_id=case.id,
            phase="cold_workload" if repetition == 0 else "warm",
        )
        checkpoint("immediately_after_generation")
        release_events = manager.release(selected, retain_all=policy.all_resident)
        events.extend(release_events)
        checkpoint("after_adapter_eviction")
        quality, evaluation = score_response(case, output.text)
        scores = routing_scores(case.expected_experts, selected)
        requests = sum(event.action in {"hit", "miss"} for event in events)
        misses = sum(event.action == "miss" for event in events)
        loads = sum(event.action == "load" for event in events)
        evictions = sum(event.action == "unload" for event in events)
        loading_ms = sum(event.duration_ms for event in events if event.action == "load")
        unloading_ms = sum(event.duration_ms for event in events if event.action == "unload")
        peak = output.metadata["generation_peak_memory"]
        end_to_end_ms = (perf_counter() - total_started) * 1000
        row: dict[str, Any] = {
            "run_backend": "transformers-peft",
            "policy": policy.name,
            "routing_method": policy.router,
            "locality": policy.locality,
            "cache_size": policy.cache_size,
            "all_resident": policy.all_resident,
            "phase": "cold_workload" if repetition == 0 else "warm",
            "repetition": repetition,
            "sequence_index": sequence_index,
            "case_id": case.id,
            "prompt": case.prompt,
            "tags": case.tags,
            "expected_experts": case.expected_experts,
            "selected_experts": selected,
            "rejected_experts": rejected,
            "resident_adapters_before_inference": before["resident_adapters"],
            "active_adapters": output.metadata["active_adapters"],
            "response": output.text,
            "quality": quality,
            "quality_delta_base": None,
            "quality_delta_oracle": None,
            "evaluation_details": evaluation,
            "routing_precision": scores["precision"],
            "routing_recall": scores["recall"],
            "routing_f1": scores["f1"],
            "top1_accuracy": scores["top1_accuracy"],
            "topk_recall": scores["topk_recall"],
            "false_activations": scores["false_activations"],
            "routing_confidence": routing.confidence,
            "candidate_scores": {
                candidate.component_id: candidate.score for candidate in routing.candidates
            },
            "routing_ms": routing.latency_ms,
            "planning_ms": planning_ms,
            "loading_ms": loading_ms,
            "unloading_ms": unloading_ms,
            "activation_ms": activation["activation_ms"],
            "synchronization_ms": (activation["activation_synchronization_ms"] + boundary_sync_ms),
            "first_token_ms": output.first_token_ms,
            "generation_ms": output.generation_ms,
            "end_to_end_ms": end_to_end_ms,
            "tokens": output.token_count,
            "tokens_per_second": (
                output.token_count / (output.generation_ms / 1000) if output.generation_ms else None
            ),
            "cache_hits": requests - misses,
            "cache_misses": misses,
            "cache_hit_rate": (requests - misses) / requests if requests else 0.0,
            "adapter_loads": loads,
            "adapter_evictions": evictions,
            "resident_adapter_count": len(before["resident_adapters"]),
            "active_adapter_count": len(selected),
            "host_rss_before_generation_mb": before["host_rss_mb"],
            "host_rss_after_generation_mb": after["host_rss_mb"],
            "mps_current_before_generation_mb": before["mps_current_allocated_mb"],
            "mps_current_after_generation_mb": after["mps_current_allocated_mb"],
            "mps_current_peak_generation_mb": peak["mps_current_allocated_mb"],
            "mps_driver_before_generation_mb": before["mps_driver_allocated_mb"],
            "mps_driver_after_generation_mb": after["mps_driver_allocated_mb"],
            "mps_driver_peak_generation_mb": peak["mps_driver_allocated_mb"],
        }
        decision = {
            "policy": policy.name,
            "phase": row["phase"],
            "repetition": repetition,
            "case_id": case.id,
            "profile": profile.model_dump(mode="json"),
            "routing": routing.model_dump(mode="json"),
            "selected_after_budget": selected,
            "rejected": rejected,
            "resident_before_inference": before["resident_adapters"],
            "active": output.metadata["active_adapters"],
            "events": [event.model_dump(mode="json") for event in events],
        }
        return row, decision

    def _router(self, name: str, repetition: int) -> Any:
        if name == "base":
            return BaseOnlyRouter()
        if name == "random":
            return RandomRouter(seed=self.config.seed + repetition, top_k=1)
        if name == "keyword":
            return KeywordRouter(top_k=2, threshold=0.01)
        if name == "oracle":
            return OracleRouter()
        return HybridRouter(
            dimension=self.config.analyzer.dimension,
            top_k=self.config.router.top_k,
            threshold=self.config.router.threshold,
            embedding_weight=self.config.router.embedding_weight,
            keyword_weight=self.config.router.keyword_weight,
        )

    @staticmethod
    def _add_relative_quality(rows: list[dict[str, Any]]) -> None:
        base = {
            (row["phase"], row["repetition"], row["case_id"]): row["quality"]
            for row in rows
            if row["policy"] == "base_only"
        }
        oracle = {
            (row["phase"], row["repetition"], row["case_id"]): row["quality"]
            for row in rows
            if row["policy"] == "oracle"
        }
        for row in rows:
            key = (row["phase"], row["repetition"], row["case_id"])
            row["quality_delta_base"] = row["quality"] - base[key]
            row["quality_delta_oracle"] = row["quality"] - oracle[key]

    def _run_rlc_matrix(
        self,
        backend: TransformersPeftBackend,
        manager: AdapterResidencyManager,
        rows: list[dict[str, Any]],
        experts: dict[str, CapacityComponent],
        warm_repetitions: int,
        telemetry: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        case = next(item for item in self.dataset.cases if item.id == "rlc_python")
        output: list[dict[str, Any]] = []
        source_policies = {
            "base_only": "base_only",
            "semantic": "semantic_cache0_low",
            "oracle": "oracle",
        }
        for label, source in source_policies.items():
            for row in rows:
                if row["policy"] == source and row["case_id"] == case.id and row["phase"] == "warm":
                    output.append(
                        {
                            "variant": label,
                            "repetition": row["repetition"],
                            "active_adapters": row["active_adapters"],
                            "quality": row["quality"],
                            "response": row["response"],
                            "status": "completed",
                        }
                    )
        manager.clear()
        manager = AdapterResidencyManager(backend, experts, cache_size=0)
        variants = {
            "code_only": ["code_expert"],
            "science_only": ["science_expert"],
            "code_plus_science": ["code_expert", "science_expert"],
        }
        for label, selected in variants.items():
            for repetition in range(1, warm_repetitions + 1):
                try:
                    events = manager.ensure(selected)
                    activation = backend.activate_adapters(selected)
                    before = memory_checkpoint(
                        "rlc_before_generation",
                        backend,
                        policy=f"rlc_{label}",
                        case_id=case.id,
                        phase="warm",
                    )
                    result = backend.generate(case.prompt, [experts[item] for item in selected])
                    quality, evaluation = score_response(case, result.text)
                    output.append(
                        {
                            "variant": label,
                            "repetition": repetition,
                            "active_adapters": result.metadata["active_adapters"],
                            "resident_adapters": before["resident_adapters"],
                            "quality": quality,
                            "evaluation": evaluation,
                            "response": result.text,
                            "activation_ms": activation["activation_ms"],
                            "loading_ms": sum(
                                event.duration_ms for event in events if event.action == "load"
                            ),
                            "generation_ms": result.generation_ms,
                            "status": "completed",
                        }
                    )
                    manager.release(selected)
                except RuntimeError as exc:
                    output.append(
                        {
                            "variant": label,
                            "repetition": repetition,
                            "active_adapters": selected,
                            "quality": None,
                            "response": None,
                            "status": "unsupported",
                            "error": str(exc),
                        }
                    )
                    manager.clear()
                    break
        telemetry.append(memory_checkpoint("rlc_matrix_complete", backend))
        return output

    @staticmethod
    def _response_row(row: dict[str, Any]) -> dict[str, Any]:
        return {
            key: row[key]
            for key in (
                "policy",
                "phase",
                "repetition",
                "case_id",
                "prompt",
                "expected_experts",
                "selected_experts",
                "active_adapters",
                "quality",
                "response",
            )
        }

    @staticmethod
    def _write_failures(
        rows: list[dict[str, Any]], rlc_rows: list[dict[str, Any]], path: Path
    ) -> None:
        base = {
            (row["phase"], row["repetition"], row["case_id"]): row["quality"]
            for row in rows
            if row["policy"] == "base_only"
        }
        oracle = {
            (row["phase"], row["repetition"], row["case_id"]): row["quality"]
            for row in rows
            if row["policy"] == "oracle"
        }
        lines = [
            "# Real-Model Failure Analysis",
            "",
            "All categories were fixed before method-level outputs were inspected.",
            "",
        ]
        count = 0
        for row in rows:
            reasons: list[str] = []
            key = (row["phase"], row["repetition"], row["case_id"])
            if row["routing_recall"] < 1:
                reasons.append("misroute or missing expected expert")
            if row["false_activations"]:
                reasons.append("unnecessary expert activation")
            if row["routing_recall"] == 1 and row["quality"] < base[key]:
                reasons.append("correct routing decreased quality versus base")
            if row["policy"] == "oracle" and row["quality"] < base[key]:
                reasons.append("oracle worse than base")
            if row["policy"] == "random" and row["quality"] > oracle[key]:
                reasons.append("random beat oracle")
            if (
                not row["expected_experts"]
                and row["selected_experts"]
                and row["quality"] < base[key]
            ):
                reasons.append("adapter damaged no-specialist response")
            if not reasons:
                continue
            count += 1
            lines.extend(
                [
                    f"## {row['policy']} / {row['case_id']} / {row['phase']} {row['repetition']}",
                    "",
                    f"**Reasons:** {', '.join(reasons)}",
                    f"**Expected:** `{row['expected_experts']}`",
                    f"**Selected:** `{row['selected_experts']}`",
                    f"**Resident:** `{row['resident_adapters_before_inference']}`",
                    f"**Quality:** `{row['quality']:.3f}`; base `{base[key]:.3f}`; oracle `{oracle[key]:.3f}`",
                    "",
                    row["response"],
                    "",
                ]
            )
        degraded = [
            row
            for row in rlc_rows
            if row.get("variant") == "code_plus_science" and row.get("status") != "completed"
        ]
        if degraded:
            lines.extend(["## RLC composition constraint", "", json.dumps(degraded, indent=2), ""])
        if count == 0 and not degraded:
            lines.append("No configured failure category was observed.\n")
        path.write_text("\n".join(lines), encoding="utf-8")

    def _publish_latest(self, run_path: Path) -> None:
        latest = self.results_root / "latest"
        if latest.exists():
            shutil.rmtree(latest)
        shutil.copytree(run_path, latest)

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
