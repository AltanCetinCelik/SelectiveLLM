"""First-class Hugging Face Transformers + PEFT backend (optional dependency)."""

from __future__ import annotations

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

    def load_component(self, component: CapacityComponent) -> None:
        if component.type is ComponentType.BASE_MODEL:
            path = component.model_path or self.config.model_path
            if not path:
                raise ValueError("Transformers base component requires model_path")
            self.model_identity = path
            self.tokenizer = self._auto_tokenizer.from_pretrained(
                self.config.tokenizer_path or path,
                trust_remote_code=self.config.trust_remote_code,
            )
            kwargs: dict[str, Any] = {
                "trust_remote_code": self.config.trust_remote_code,
            }
            if self.config.device_map and self.device == "cuda":
                kwargs["device_map"] = self.config.device_map
                if self.config.max_memory:
                    kwargs["max_memory"] = self.config.max_memory
            self.model = self._auto_model.from_pretrained(path, **kwargs)
            if self.device in {"cpu", "mps"}:
                self.model.to(self.device)
            self.model.eval()
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
                )
            else:
                self.model.load_adapter(
                    component.model_path, adapter_name=component.id, is_trainable=False
                )
            self.loaded_adapters.add(component.id)

    def unload_component(self, component: CapacityComponent) -> None:
        if component.id in self.loaded_adapters and self.model is not None:
            if hasattr(self.model, "delete_adapter"):
                self.model.delete_adapter(component.id)
            self.loaded_adapters.discard(component.id)
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
        if adapters and hasattr(self.model, "set_adapter"):
            try:
                self.model.set_adapter(adapters if len(adapters) > 1 else adapters[0])
            except (TypeError, ValueError) as exc:
                raise RuntimeError(
                    "configured adapters cannot be composed by this PEFT model"
                ) from exc
        inputs = self.tokenizer(prompt, return_tensors="pt")
        inputs = {key: value.to(self.device) for key, value in inputs.items()}
        self.synchronize()
        started = perf_counter()
        with self._torch.inference_mode():
            output = self.model.generate(
                **inputs,
                max_new_tokens=self.config.max_new_tokens,
                do_sample=False,
            )
        self.synchronize()
        elapsed = (perf_counter() - started) * 1000
        generated = output[0][inputs["input_ids"].shape[-1] :]
        text = self.tokenizer.decode(generated, skip_special_tokens=True)
        count = int(generated.shape[-1])
        return BackendOutput(
            text=text,
            token_count=count,
            first_token_ms=None,
            generation_ms=elapsed,
            metadata={
                "first_token_availability": "not measured without streaming instrumentation",
                "active_adapters": adapters,
            },
        )

    def synchronize(self) -> None:
        if self.device.startswith("cuda"):
            self._torch.cuda.synchronize()
        elif self.device == "mps" and hasattr(self._torch, "mps"):
            self._torch.mps.synchronize()
