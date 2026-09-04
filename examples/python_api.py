"""Minimal public Python API example."""

from selectivellm import SelectiveLLM

engine = SelectiveLLM.from_config("configs/default.yaml")
result = engine.generate("Write a Python implementation of Dijkstra's algorithm")

print(result.text)
print(result.routing.model_dump())
print(result.metrics.model_dump())
