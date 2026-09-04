"""Prompt analysis and deterministic local feature embeddings."""

from __future__ import annotations

import hashlib
import math
import re
from collections import defaultdict

from selectivellm.schemas import PromptProfile

TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_+#.\-]*")

DOMAIN_TERMS: dict[str, tuple[str, ...]] = {
    "general": ("history", "capital", "explain", "summarize", "general", "knowledge"),
    "python": (
        "python",
        "fastapi",
        "pandas",
        "numpy",
        "pytest",
        "decorator",
        "binary search",
        "dijkstra",
        "code",
        "implementation",
    ),
    "software_engineering": (
        "api",
        "database",
        "distributed",
        "refactor",
        "testing",
        "software",
        "endpoint",
    ),
    "mathematics": (
        "calculate",
        "equation",
        "integral",
        "matrix",
        "probability",
        "proof",
        "solve",
        "theorem",
    ),
    "electrical_engineering": (
        "circuit",
        "mosfet",
        "voltage",
        "current",
        "impedance",
        "rlc",
        "transient",
        "frequency response",
    ),
    "reasoning": (
        "analyze",
        "compare",
        "deduce",
        "logic",
        "reason",
        "step by step",
        "tradeoff",
        "why",
    ),
    "scientific_writing": (
        "abstract",
        "citation",
        "hypothesis",
        "methodology",
        "paper",
        "scientific",
    ),
}

TASK_TERMS: dict[str, tuple[str, ...]] = {
    "code_generation": ("code", "implement", "function", "class", "script", "simulate"),
    "calculation": ("calculate", "compute", "solve", "derive"),
    "explanation": ("explain", "describe", "why", "summarize"),
    "analysis": ("analyze", "compare", "evaluate", "tradeoff"),
}


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def contains_term(text: str, term: str) -> bool:
    normalized = term.replace("_", " ").lower()
    return re.search(rf"(?<!\w){re.escape(normalized)}(?!\w)", text.lower()) is not None


def stable_embedding(text: str, dimension: int = 256) -> list[float]:
    """Build a deterministic feature-hash embedding without network dependencies."""
    normalized = " ".join(tokenize(text))
    features = tokenize(text)
    features.extend(normalized[index : index + 3] for index in range(max(0, len(normalized) - 2)))
    vector = [0.0] * dimension
    for feature in features:
        digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=8).digest()
        bucket = int.from_bytes(digest[:4], "big") % dimension
        sign = 1.0 if digest[4] & 1 else -1.0
        vector[bucket] += sign
    norm = math.sqrt(sum(value * value for value in vector))
    return [value / norm for value in vector] if norm else vector


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise ValueError("embedding dimensions must match")
    return sum(a * b for a, b in zip(left, right, strict=True))


class DeterministicEmbeddingAnalyzer:
    """Multi-label analyzer combining transparent lexical evidence with local embeddings."""

    name = "deterministic-feature-analyzer"
    version = "1.0.0"

    def __init__(self, dimension: int = 256) -> None:
        self.dimension = dimension
        self._domain_embeddings = {
            domain: stable_embedding(" ".join(terms), dimension)
            for domain, terms in DOMAIN_TERMS.items()
        }

    def analyze(self, prompt: str) -> PromptProfile:
        lowered = prompt.lower()
        prompt_embedding = stable_embedding(prompt, self.dimension)
        scores: dict[str, float] = {}
        evidence: dict[str, list[str]] = {}
        for domain, terms in DOMAIN_TERMS.items():
            hits = [term for term in terms if contains_term(lowered, term)]
            lexical = min(1.0, len(hits) / 2.0)
            semantic = max(
                0.0, cosine_similarity(prompt_embedding, self._domain_embeddings[domain])
            )
            score = min(1.0, 0.65 * lexical + 0.35 * semantic)
            scores[domain] = score
            if hits:
                evidence[domain] = hits

        if "simulate" in lowered and any(
            term in lowered for term in ("circuit", "rlc", "transient")
        ):
            scores["mathematics"] = max(scores["mathematics"], 0.45)
            evidence.setdefault("mathematics", []).append("numerical simulation inference")

        task_scores: defaultdict[str, float] = defaultdict(float)
        for task, terms in TASK_TERMS.items():
            task_hit_count = sum(contains_term(lowered, term) for term in terms)
            task_scores[task] = min(1.0, task_hit_count / 2.0)

        ranked = sorted(scores, key=lambda domain: scores[domain], reverse=True)
        capabilities = [domain for domain in ranked if scores[domain] >= 0.18]
        if not capabilities:
            capabilities = ["general"]
            scores["general"] = max(scores["general"], 0.2)
        confidence = min(1.0, max(scores.values()))
        difficulty = (
            "high" if len(capabilities) >= 3 else "medium" if len(capabilities) == 2 else "low"
        )
        language = "python" if "python" in capabilities else None
        return PromptProfile(
            prompt=prompt,
            domain_scores=scores,
            task_scores=dict(task_scores),
            capabilities=capabilities,
            programming_language=language,
            difficulty=difficulty,
            confidence=confidence,
            evidence=evidence,
        )
