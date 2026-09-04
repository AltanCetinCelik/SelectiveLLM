"""Transparent descriptive statistics for benchmark observations."""

from __future__ import annotations

import math
import statistics
from collections.abc import Sequence

import numpy as np

from selectivellm.schemas import AggregateStats


def aggregate(values: Sequence[float]) -> AggregateStats:
    clean = [float(value) for value in values if math.isfinite(float(value))]
    if not clean:
        return AggregateStats(count=0)
    count = len(clean)
    mean = statistics.fmean(clean)
    deviation = statistics.stdev(clean) if count > 1 else 0.0
    margin = 1.96 * deviation / math.sqrt(count) if count > 1 else None
    return AggregateStats(
        count=count,
        mean=mean,
        median=statistics.median(clean),
        standard_deviation=deviation,
        p50=float(np.percentile(clean, 50)),
        p95=float(np.percentile(clean, 95)),
        confidence_interval_95=(mean - margin, mean + margin) if margin is not None else None,
    )
