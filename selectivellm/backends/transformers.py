"""First-class Hugging Face Transformers + PEFT backend (optional dependency)."""

from __future__ import annotations

import gc
import threading
import time
from time import perf_counter
from typing import Any, Literal

from selectivellm.backends.base import InferenceBackend
from selectivellm.config import BackendConfig
from selectivellm.runtime.device import detect_device
from selectivellm.schemas import BackendOutput, CapacityComponent, ComponentType


class TransformersPeftBackend(InferenceBackend):
    name = "transformers-peft"
    kind: Literal["real"] = "real"

    def __init__(self, config: BackendConfig) -> None:
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError("Transformers backend requires `pip install -e '.[hf]'`") from exc
        self._torch = torch
        self._auto_model = AutoModelForCausalLM
        self._auto_tokenizer = AutoTokenizer
        self.config = config
        self.device = detect_device(config.device)
        self.model_identity = config.model_path or "unconfigured"
        self.model: Any | None = None
        self.tokenizer: Any | None = None
        self.loaded_adapters: set[str] = set()
        self.active_adapters: list[str] = []
        self._composition_adapter: str | None = None
        self._activation_metadata: dict[str, Any] = {"composition_mode": "none"}

    def load_component(self, component: CapacityComponent) -> None:
        if component.type is ComponentType.BASE_MODEL:
            path = component.model_path or self.config.model_path
            if not path:
                raise ValueError("Transformers base component requires model_path")
            self.model_identity = path
            self.tokenizer = self._auto_tokenizer.from_pretrained(
                self.config.tokenizer_path or path,
                revision=self.config.tokenizer_revision or self.config.model_revision,
                trust_remote_code=self.config.trust_remote_code,
            )
            kwargs: dict[str, Any] = {
                "revision": self.config.model_revision,
                "trust_remote_code": self.config.trust_remote_code,
            }
            if self.config.dtype != "auto":
                try:
                    kwargs["dtype"] = getattr(self._torch, self.config.dtype)
                except AttributeError as exc:
                    raise ValueError(f"unsupported torch dtype: {self.config.dtype}") from exc
            if self.config.device_map and self.device == "cuda":
                kwargs["device_map"] = self.config.device_map
                if self.config.max_memory:
                    kwargs["max_memory"] = self.config.max_memory
            model: Any = self._auto_model.from_pretrained(path, **kwargs)
            if self.device in {"cpu", "mps"}:
                model.to(self.device)
            model.eval()
            self.model = model
            return

        if component.type in {ComponentType.ADAPTER, ComponentType.LORA}:
            if self.model is None:
                raise RuntimeError("load the base model before adapters")
            if not component.model_path:
                raise ValueError(f"adapter {component.id} requires model_path")
            try:
                from peft import PeftModel
            except ImportError as exc:
                raise RuntimeError("PEFT adapters require the `peft` optional dependency") from exc
            if not isinstance(self.model, PeftModel):
                self.model = PeftModel.from_pretrained(
                    self.model,
                    component.model_path,
                    adapter_name=component.id,
                    is_trainable=False,
                    revision=component.metadata.get("revision"),
                )
            else:
                self.model.load_adapter(
                    component.model_path,
                    adapter_name=component.id,
                    is_trainable=False,
                    revision=component.metadata.get("revision"),
                )
            self.loaded_adapters.add(component.id)

    def unload_component(self, component: CapacityComponent) -> None:
        if component.id in self.loaded_adapters and self.model is not None:
            self._drop_composition()
            if len(self.loaded_adapters) == 1 and hasattr(self.model, "unload"):
                self.model = self.model.unload()
                self.model.eval()
            elif hasattr(self.model, "delete_adapter"):
                self.model.delete_adapter(component.id)
            self.loaded_adapters.discard(component.id)
            self.active_adapters = [item for item in self.active_adapters if item != component.id]
            gc.collect()
        if component.type is ComponentType.BASE_MODEL:
            self.model = None
            self.tokenizer = None

    def generate(self, prompt: str, active_components: list[CapacityComponent]) -> BackendOutput:
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Transformers model is not loaded")
        adapters = [
            component.id
            for component in active_components
            if component.type in {ComponentType.ADAPTER, ComponentType.LORA}
        ]
        activation = self.activate_adapters(adapters)

        messages = [{"role": "user", "content": prompt}]
        if getattr(self.tokenizer, "chat_template", None):
            inputs = self.tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                tokenize=True,
                return_dict=True,
                return_tensors="pt",
            )
        else:
            inputs = self.tokenizer(prompt, return_tensors="pt")
        inputs = {key: value.to(self.device) for key, value in inputs.items()}
        self.synchronize()
        started = perf_counter()
        first_token: list[float] = []
        prompt_length = int(inputs["input_ids"].shape[-1])

        from transformers import StoppingCriteria, StoppingCriteriaList

        backend = self

        class FirstTokenCriteria(StoppingCriteria):
            def __call__(self, input_ids: Any, scores: Any, **kwargs: Any) -> bool:
                del scores, kwargs
                if not first_token and int(input_ids.shape[-1]) > prompt_length:
                    backend.synchronize()
                    first_token.append((perf_counter() - started) * 1000)
                return False

        peak = self.memory_metrics()
        stop_sampler = threading.Event()

        def sample_memory() -> None:
            while not stop_sampler.is_set():
                sample = self.memory_metrics()
                for key in ("mps_current_allocated_mb", "mps_driver_allocated_mb"):
                    value = sample.get(key)
                    if value is not None:
                        peak[key] = max(float(peak.get(key) or 0.0), float(value))
                time.sleep(0.005)

        sampler = threading.Thread(target=sample_memory, daemon=True)
        sampler.start()
        with self._torch.inference_mode():
            output = self.model.generate(
                **inputs,
                max_new_tokens=self.config.max_new_tokens,
                do_sample=False,
                stopping_criteria=StoppingCriteriaList([FirstTokenCriteria()]),
                pad_token_id=self.tokenizer.eos_token_id,
            )
        self.synchronize()
        stop_sampler.set()
        sampler.join(timeout=1)
        elapsed = (perf_counter() - started) * 1000
        generated = output[0][inputs["input_ids"].shape[-1] :]
        text = self.tokenizer.decode(generated, skip_special_tokens=True)
        count = int(generated.shape[-1])
        return BackendOutput(
            text=text,
            token_count=count,
            first_token_ms=first_token[0] if first_token else None,
            generation_ms=elapsed,
            metadata={
                "first_token_availability": "measured by synchronized first-token stopping criterion",
                "active_adapters": adapters,
                "resident_adapters": sorted(self.loaded_adapters),
                "backend_active_adapter": self._composition_adapter
                or (adapters[0] if adapters else None),
                **activation,
                **self._activation_metadata,
                "generation_peak_memory": peak,
            },
        )

    def activate_adapters(self, adapters: list[str]) -> dict[str, Any]:
        if self.model is None:
            raise RuntimeError("Transformers model is not loaded")
        if adapters and adapters == self.active_adapters:
            return {
                "activation_ms": 0.0,
                "activation_synchronization_ms": 0.0,
                **self._activation_metadata,
            }
        activation_started = perf_counter()
        self._drop_composition()
        self._activation_metadata = {
            "composition_mode": "none",
            "direct_multi_adapter_activation_supported": False,
        }
        if len(adapters) > 1 and hasattr(self.model, "set_adapter"):
            tuner = getattr(self.model, "base_model", None)
            if tuner is None or not hasattr(tuner, "add_weighted_adapter"):
                raise RuntimeError("installed PEFT backend cannot compose multiple LoRA adapters")
            self._composition_adapter = "selectivellm_weighted_composition"
            tuner.add_weighted_adapter(
                adapters,
                [1.0] * len(adapters),
                self._composition_adapter,
                combination_type="linear",
            )
            self.model.set_adapter(self._composition_adapter)
            self._activation_metadata = {
                "composition_mode": "weighted_linear_derived_adapter",
                "composition_sources": adapters,
                "direct_multi_adapter_activation_supported": False,
            }
        elif adapters and hasattr(self.model, "set_adapter"):
            try:
                if hasattr(self.model, "enable_adapter_layers"):
                    self.model.enable_adapter_layers()
                self.model.set_adapter(adapters if len(adapters) > 1 else adapters[0])
            except (TypeError, ValueError) as exc:
                raise RuntimeError(
                    "configured adapters cannot be composed by this PEFT model"
                ) from exc
        elif not adapters and hasattr(self.model, "disable_adapter_layers"):
            self.model.disable_adapter_layers()
        self.active_adapters = adapters
        activation_ms = (perf_counter() - activation_started) * 1000
        sync_started = perf_counter()
        self.synchronize()
        activation_sync_ms = (perf_counter() - sync_started) * 1000
        return {
            "activation_ms": activation_ms,
            "activation_synchronization_ms": activation_sync_ms,
            **self._activation_metadata,
        }

    def _drop_composition(self) -> None:
        if self._composition_adapter and self.model is not None:
            if hasattr(self.model, "delete_adapter"):
                self.model.delete_adapter(self._composition_adapter)
            self._composition_adapter = None

    def memory_metrics(self) -> dict[str, float | None]:
        if self.device != "mps" or not hasattr(self._torch, "mps"):
            return {
                "mps_current_allocated_mb": None,
                "mps_driver_allocated_mb": None,
                "mps_recommended_max_mb": None,
            }
        divisor = 1024 * 1024
        return {
            "mps_current_allocated_mb": self._torch.mps.current_allocated_memory() / divisor,
            "mps_driver_allocated_mb": self._torch.mps.driver_allocated_memory() / divisor,
            "mps_recommended_max_mb": self._torch.mps.recommended_max_memory() / divisor,
        }

    def cleanup_allocator(self) -> None:
        """Deliberate cold-policy cleanup; never called between ordinary cases."""
        gc.collect()
        if self.device == "mps" and hasattr(self._torch, "mps"):
            self.synchronize()
            self._torch.mps.empty_cache()
            self.synchronize()

    def synchronize(self) -> None:
        if self.device.startswith("cuda"):
            self._torch.cuda.synchronize()
        elif self.device == "mps" and hasattr(self._torch, "mps"):
            self._torch.mps.synchronize()
