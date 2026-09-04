"""Actual process/accelerator measurements kept separate from declared capacity."""

from __future__ import annotations

import psutil

from selectivellm.schemas import MemorySnapshot


class MemoryMeter:
    def __init__(self, device: str) -> None:
        self.device = device
        self.declared_peak_mb = 0.0
        self._mps_peak_mb = 0.0

    def reset_peak(self) -> None:
        self.declared_peak_mb = 0.0
        self._mps_peak_mb = 0.0
        try:
            import torch

            if self.device.startswith("cuda") and torch.cuda.is_available():
                torch.cuda.reset_peak_memory_stats()
        except ImportError:
            pass

    def snapshot(self, declared_resident_mb: float) -> MemorySnapshot:
        self.declared_peak_mb = max(self.declared_peak_mb, declared_resident_mb)
        allocated: float | None = None
        reserved: float | None = None
        peak: float | None = None
        available = False
        reason: str | None = "CPU backend has no accelerator-memory measurement"
        try:
            import torch

            if self.device.startswith("cuda") and torch.cuda.is_available():
                allocated = torch.cuda.memory_allocated() / (1024 * 1024)
                reserved = torch.cuda.memory_reserved() / (1024 * 1024)
                peak = torch.cuda.max_memory_allocated() / (1024 * 1024)
                available = True
                reason = None
            elif self.device == "mps" and hasattr(torch, "mps"):
                allocated = torch.mps.current_allocated_memory() / (1024 * 1024)
                self._mps_peak_mb = max(self._mps_peak_mb, allocated)
                peak = self._mps_peak_mb
                available = True
                reason = "MPS reserved-memory metric is unavailable"
        except (ImportError, RuntimeError):
            reason = "Accelerator runtime unavailable"

        return MemorySnapshot(
            measurement_semantics="declared_capacity_plus_observed_process_and_accelerator",
            declared_resident_capacity_mb=declared_resident_mb,
            declared_peak_capacity_mb=self.declared_peak_mb,
            host_rss_mb=psutil.Process().memory_info().rss / (1024 * 1024),
            accelerator_allocated_mb=allocated,
            accelerator_reserved_mb=reserved,
            accelerator_peak_allocated_mb=peak,
            accelerator_measurement_available=available,
            unavailable_reason=reason,
        )
