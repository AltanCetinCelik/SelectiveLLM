"""Tokenizer-safe forced-choice scoring for the pinned dense model."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from typing import Any

from selectivellm.dense_capacity.benchmark import LABELS, AnswerLabel, DenseBenchmarkCase

PROMPT_TEMPLATE = """Choose the correct answer.

{question}

A. {option_a}
B. {option_b}
C. {option_c}
D. {option_d}

Respond with exactly one option label: A, B, C, or D."""


@dataclass(frozen=True)
class EncodedCase:
    rendered_chat: str
    input_ids: list[int]
    eligible_token_mask: list[bool]


class ForcedChoiceScorer:
    def __init__(self, model: Any, tokenizer: Any, device: str) -> None:
        import torch

        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.torch = torch
        self.option_token_ids: dict[AnswerLabel, int] = {}
        self.rendered_template_hash: str | None = None

    @staticmethod
    def prompt(case: DenseBenchmarkCase) -> str:
        return PROMPT_TEMPLATE.format(
            question=case.question,
            option_a=case.options["A"],
            option_b=case.options["B"],
            option_c=case.options["C"],
            option_d=case.options["D"],
        )

    def encode(self, case: DenseBenchmarkCase) -> EncodedCase:
        messages = [{"role": "user", "content": self.prompt(case)}]
        rendered = self.tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, tokenize=False
        )
        templated_ids = self.tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, tokenize=True, return_dict=True
        )
        encoded_ids = self.tokenizer(rendered, add_special_tokens=False)["input_ids"]
        if list(templated_ids["input_ids"]) != list(encoded_ids):
            raise ValueError("rendered chat text does not reproduce templated token IDs")
        special_ids = set(self.tokenizer.all_special_ids)
        eligible = [token_id not in special_ids for token_id in encoded_ids]
        if not any(eligible):
            raise ValueError("rendered prompt has no eligible tracing tokens")
        return EncodedCase(rendered, list(encoded_ids), eligible)

    def validate_protocol(self, cases: list[DenseBenchmarkCase]) -> dict[str, Any]:
        observed_ids: dict[str, set[int]] = {label: set() for label in LABELS}
        rendered_suffixes: set[str] = set()
        rendered_hash = hashlib.sha256()
        for case in cases:
            encoded = self.encode(case)
            rendered_hash.update(case.id.encode())
            rendered_hash.update(b"\0")
            rendered_hash.update(encoded.rendered_chat.encode())
            rendered_hash.update(b"\0")
            rendered_suffixes.add(encoded.rendered_chat[-64:])
            for label in LABELS:
                candidate_ids = self.tokenizer(
                    encoded.rendered_chat + label, add_special_tokens=False
                )["input_ids"]
                prefix_length = len(encoded.input_ids)
                if list(candidate_ids[:prefix_length]) != encoded.input_ids:
                    raise ValueError(f"candidate {label} retokenized the prefix for {case.id}")
                suffix = list(candidate_ids[prefix_length:])
                if len(suffix) != 1:
                    raise ValueError(
                        f"candidate {label} is not one token at scored position for {case.id}"
                    )
                observed_ids[label].add(int(suffix[0]))
        if any(len(values) != 1 for values in observed_ids.values()):
            raise ValueError(f"option token IDs vary by case: {observed_ids}")
        resolved = {label: next(iter(observed_ids[label])) for label in LABELS}
        if len(set(resolved.values())) != 4:
            raise ValueError(f"option token IDs are not distinct: {resolved}")
        self.option_token_ids = resolved
        self.rendered_template_hash = rendered_hash.hexdigest()
        return {
            "status": "valid",
            "case_count": len(cases),
            "option_token_ids": resolved,
            "single_token_at_scored_position": True,
            "distinct_option_token_ids": True,
            "prefix_retokenization_observed": False,
            "rendered_suffix_count": len(rendered_suffixes),
            "rendered_prompts_sha256": self.rendered_template_hash,
            "prompt_template_sha256": hashlib.sha256(PROMPT_TEMPLATE.encode()).hexdigest(),
        }

    def tensors(self, case: DenseBenchmarkCase) -> tuple[dict[str, Any], list[bool]]:
        encoded = self.encode(case)
        input_ids = self.torch.tensor(
            [encoded.input_ids], dtype=self.torch.long, device=self.device
        )
        attention_mask = self.torch.ones_like(input_ids)
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
        }, encoded.eligible_token_mask

    def score(self, case: DenseBenchmarkCase) -> dict[str, Any]:
        if set(self.option_token_ids) != set(LABELS):
            raise RuntimeError("validate tokenizer protocol before scoring")
        inputs, _ = self.tensors(case)
        with self.torch.inference_mode():
            output = self.model(**inputs, use_cache=False)
        logits = output.logits[0, -1]
        option_logits = self.torch.stack(
            [logits[self.option_token_ids[label]] for label in LABELS]
        ).float()
        probabilities = self.torch.softmax(option_logits, dim=0).detach().cpu().tolist()
        raw_logits = option_logits.detach().cpu().tolist()
        if not all(math.isfinite(float(value)) for value in [*raw_logits, *probabilities]):
            raise ValueError(f"nonfinite option score for {case.id}")
        if not math.isclose(sum(probabilities), 1.0, rel_tol=0, abs_tol=1e-6):
            raise ValueError(f"option probabilities do not sum to one for {case.id}")
        by_label = {label: float(probabilities[index]) for index, label in enumerate(LABELS)}
        logits_by_label = {label: float(raw_logits[index]) for index, label in enumerate(LABELS)}
        prediction = max(LABELS, key=lambda label: (by_label[label], -LABELS.index(label)))
        correct_probability = by_label[case.correct_label]
        return {
            "case_id": case.id,
            "domain": case.domain,
            "split": case.split,
            "correct_label": case.correct_label,
            "option_token_ids": dict(self.option_token_ids),
            "option_logits": logits_by_label,
            "option_probabilities": by_label,
            "probability_sum": sum(probabilities),
            "correct_probability": correct_probability,
            "correct_nll": -math.log(correct_probability),
            "prediction": prediction,
            "correct": prediction == case.correct_label,
            "scoring_semantics": "restricted_four_option_softmax",
        }

    @staticmethod
    def stable_hash(value: Any) -> str:
        return hashlib.sha256(
            json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
