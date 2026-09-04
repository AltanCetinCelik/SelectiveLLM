from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from selectivellm.benchmarking import BenchmarkRunner
from selectivellm.cli import app
from selectivellm.config import SelectiveLLMConfig


def test_benchmark_writes_complete_labeled_artifact(
    tmp_path: Path, control_config: SelectiveLLMConfig
) -> None:
    run = BenchmarkRunner(control_config, results_root=tmp_path).run(
        repetitions=1, report=True, run_id="test-run"
    )
    expected = {
        "config.yaml",
        "environment.json",
        "manifest.json",
        "raw_results.jsonl",
        "routing_decisions.jsonl",
        "summary.json",
        "summary.csv",
        "report.md",
        "routing_failures.md",
    }
    assert expected <= {path.name for path in run.iterdir()}
    assert len(list((run / "plots").glob("*.png"))) == 5
    manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "completed"
    assert manifest["backend_kind"] == "control"
    assert len(manifest["benchmark_fingerprint"]) == 64
    report = (run / "report.md").read_text(encoding="utf-8")
    assert "do not demonstrate physical VRAM savings" in report
    raw = [json.loads(line) for line in (run / "raw_results.jsonl").read_text().splitlines()]
    assert {row["method"] for row in raw} == {
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
    }
    assert all(row["benchmark_fingerprint"] == manifest["benchmark_fingerprint"] for row in raw)


def test_cli_inspect_and_registry_are_cpu_safe() -> None:
    runner = CliRunner()
    inspected = runner.invoke(app, ["inspect", "--device", "cpu"])
    listed = runner.invoke(app, ["registry", "list"])
    assert inspected.exit_code == 0
    assert "Device Class" in inspected.stdout
    assert listed.exit_code == 0
    assert "Declared MB is registry metadata" in listed.stdout


def test_security_default_disables_remote_code() -> None:
    assert SelectiveLLMConfig().backend.trust_remote_code is False
