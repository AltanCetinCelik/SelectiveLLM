"""Hardware discovery without assuming an NVIDIA accelerator."""

from __future__ import annotations

import os
import platform
import sys
from dataclasses import asdict, dataclass
from typing import Any

import psutil


@dataclass(frozen=True)
class HardwareInfo:
    os: str
    os_version: str
    architecture: str
    cpu: str
    logical_cpus: int
    total_ram_gb: float
    device: str
    device_class: str
    accelerator: str | None
    accelerator_memory_mb: float | None
    cuda_version: str | None
    torch_version: str | None
    mps_available: bool
    python_version: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _torch_info() -> tuple[Any | None, str | None]:
    try:
        import torch

        return torch, str(torch.__version__)
    except ImportError:
        return None, None


def detect_device(requested: str = "auto") -> str:
    if requested != "auto":
        return requested
    torch, _ = _torch_info()
    if torch is not None and torch.cuda.is_available():
        return "cuda"
    if torch is not None and hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def inspect_hardware(requested: str = "auto") -> HardwareInfo:
    torch, torch_version = _torch_info()
    device = detect_device(requested)
    accelerator: str | None = None
    accelerator_memory_mb: float | None = None
    cuda_version: str | None = None
    mps_available = bool(
        torch is not None and hasattr(torch.backends, "mps") and torch.backends.mps.is_available()
    )

    if device.startswith("cuda") and torch is not None:
        index = torch.cuda.current_device()
        properties = torch.cuda.get_device_properties(index)
        accelerator = properties.name
        accelerator_memory_mb = properties.total_memory / (1024 * 1024)
        cuda_version = str(torch.version.cuda) if torch.version.cuda else None
    elif device == "mps":
        accelerator = "Apple Metal Performance Shaders"

    cpu = platform.processor() or os.environ.get("PROCESSOR_IDENTIFIER", "unknown")
    return HardwareInfo(
        os=platform.system(),
        os_version=platform.release(),
        architecture=platform.machine(),
        cpu=cpu,
        logical_cpus=psutil.cpu_count(logical=True) or 1,
        total_ram_gb=round(psutil.virtual_memory().total / (1024**3), 2),
        device=device,
        device_class=device.split(":", maxsplit=1)[0],
        accelerator=accelerator,
        accelerator_memory_mb=accelerator_memory_mb,
        cuda_version=cuda_version,
        torch_version=torch_version,
        mps_available=mps_available,
        python_version=sys.version.split()[0],
    )
