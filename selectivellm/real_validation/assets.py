"""Pinned Hugging Face asset provenance and PEFT compatibility preflight."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class AssetSpec:
    role: str
    repo_id: str
    revision: str
    license: str = "apache-2.0"


ASSETS = (
    AssetSpec(
        "base",
        "Qwen/Qwen2.5-1.5B-Instruct",
        "989aa7980e4cf806f80c7fef2b1adb7bc71aa306",
    ),
    AssetSpec(
        "code_expert",
        "uditjain/lori-qwen2.5-1.5b-code",
        "e937bbd728f28a441163f94b60ea5a119513e351",
    ),
    AssetSpec(
        "math_expert",
        "uditjain/lori-qwen2.5-1.5b-math",
        "f992ab536c07761c67bd46e35c787bb68ea97657",
    ),
    AssetSpec(
        "science_expert",
        "uditjain/lori-qwen2.5-1.5b-science",
        "398cf3cc78a3ff8c78c84c3a424da3ba994bdd6f",
    ),
)


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_compatibility_report(report: dict[str, Any]) -> None:
    base = report["base"]
    adapters = report["adapters"]
    if base["resolved_revision"] != base["requested_revision"]:
        raise ValueError("base revision did not resolve to the requested immutable commit")
    if base["license"] != "apache-2.0":
        raise ValueError("base license is not Apache-2.0")
    signatures: set[str] = set()
    for adapter in adapters:
        if adapter["resolved_revision"] != adapter["requested_revision"]:
            raise ValueError(f"adapter revision mismatch: {adapter['repo_id']}")
        if adapter["license"] != "apache-2.0":
            raise ValueError(f"adapter license mismatch: {adapter['repo_id']}")
        if adapter["base_model_name_or_path"] != base["repo_id"]:
            raise ValueError(f"adapter base mismatch: {adapter['repo_id']}")
        if adapter["peft_type"] != "LORA":
            raise ValueError(f"adapter is not LoRA: {adapter['repo_id']}")
        signatures.add(adapter["peft_signature_hash"])
    if len(signatures) != 1:
        raise ValueError("adapters do not share rank, alpha, and target modules")
    tokenizer = report["tokenizer"]
    if tokenizer["repo_id"] != base["repo_id"]:
        raise ValueError("tokenizer does not come from the pinned base repository")
    if tokenizer["resolved_revision"] != base["resolved_revision"]:
        raise ValueError("tokenizer and base revisions differ")
    if tokenizer["max_token_id"] >= base["vocab_size"]:
        raise ValueError("tokenizer contains an id outside the base embedding table")


def verify_compatibility(output_path: str | Path | None = None) -> dict[str, Any]:
    try:
        from huggingface_hub import HfApi, hf_hub_download
        from transformers import AutoConfig, AutoTokenizer
    except ImportError as exc:
        raise RuntimeError("real validation requires `pip install -e '.[hf]'`") from exc

    api = HfApi()
    base_spec = ASSETS[0]
    base_info = api.model_info(base_spec.repo_id, revision=base_spec.revision, files_metadata=True)
    base_config_path = hf_hub_download(
        base_spec.repo_id, "config.json", revision=base_spec.revision
    )
    base_config = AutoConfig.from_pretrained(base_spec.repo_id, revision=base_spec.revision)
    tokenizer = AutoTokenizer.from_pretrained(base_spec.repo_id, revision=base_spec.revision)
    base_license = getattr(base_info.card_data, "license", None)
    report: dict[str, Any] = {
        "status": "pending_validation",
        "base": {
            **asdict(base_spec),
            "requested_revision": base_spec.revision,
            "resolved_revision": base_info.sha,
            "license": base_license,
            "model_type": base_config.model_type,
            "vocab_size": int(base_config.vocab_size),
            "config_sha256": _sha256(base_config_path),
        },
        "tokenizer": {
            "repo_id": base_spec.repo_id,
            "requested_revision": base_spec.revision,
            "resolved_revision": base_info.sha,
            "class": tokenizer.__class__.__name__,
            "vocab_size": len(tokenizer),
            "max_token_id": max(tokenizer.get_vocab().values()),
        },
        "adapters": [],
    }
    for spec in ASSETS[1:]:
        info = api.model_info(spec.repo_id, revision=spec.revision, files_metadata=True)
        config_path = hf_hub_download(spec.repo_id, "adapter_config.json", revision=spec.revision)
        raw = json.loads(Path(config_path).read_text(encoding="utf-8"))
        signature = {
            "peft_type": raw.get("peft_type"),
            "r": raw.get("r"),
            "lora_alpha": raw.get("lora_alpha"),
            "target_modules": sorted(raw.get("target_modules", [])),
        }
        siblings = {item.rfilename: item for item in info.siblings or []}
        weights = siblings.get("adapter_model.safetensors")
        report["adapters"].append(
            {
                **asdict(spec),
                "requested_revision": spec.revision,
                "resolved_revision": info.sha,
                "license": getattr(info.card_data, "license", None),
                "base_model_name_or_path": raw.get("base_model_name_or_path"),
                **signature,
                "peft_signature_hash": hashlib.sha256(
                    json.dumps(signature, sort_keys=True).encode()
                ).hexdigest(),
                "config_sha256": _sha256(config_path),
                "adapter_bytes": getattr(weights, "size", None),
            }
        )
    validate_compatibility_report(report)
    report["status"] = "compatible"
    if output_path is not None:
        Path(output_path).write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    return report
