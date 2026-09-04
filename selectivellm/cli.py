"""Rich command-line interface for SelectiveLLM."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from selectivellm import __version__
from selectivellm.benchmarking import BenchmarkRunner
from selectivellm.config import SelectiveLLMConfig
from selectivellm.engine import SelectiveLLM
from selectivellm.runtime.device import inspect_hardware

app = typer.Typer(
    name="selectivellm",
    help="Semantic capacity routing experiments for memory-constrained LLM inference.",
    no_args_is_help=True,
)
registry_app = typer.Typer(help="Inspect the configured capacity registry.")
app.add_typer(registry_app, name="registry")
console = Console()


def _config(path: Path | None, seed: int | None = None) -> SelectiveLLMConfig:
    config = SelectiveLLMConfig.from_yaml(path) if path else SelectiveLLMConfig()
    if seed is not None:
        config.seed = seed
    return config


def _engine(path: Path | None, seed: int | None = None) -> SelectiveLLM:
    return SelectiveLLM.from_config(config=_config(path, seed))


def _render_result(prompt: str, engine: SelectiveLLM, *, verbose: bool) -> None:
    result = engine.generate(prompt)
    console.print(Panel.fit(prompt, title="SelectiveLLM", border_style="cyan"))
    console.print(f"[bold]Backend[/bold]  {result.backend} ({result.backend_kind})")
    if result.backend_kind == "control":
        console.print(
            "[yellow]Control backend: declared capacity is simulated; no VRAM claim.[/yellow]"
        )
    console.print(f"[bold]Domains[/bold]  {', '.join(result.profile.capabilities)}")
    route = Table(title="Router decision", show_header=True)
    route.add_column("Component")
    route.add_column("Score", justify="right")
    route.add_column("Selected")
    for candidate in result.routing.candidates[:5]:
        route.add_row(
            candidate.component_id,
            f"{candidate.score:.3f}",
            "yes" if candidate.component_id in result.routing.selected else "",
        )
    console.print(route)
    plan = Table(title="Capacity plan", show_header=False)
    plan.add_row("Active", ", ".join(result.plan.selected))
    plan.add_row("Rejected", json.dumps(result.plan.rejected) if result.plan.rejected else "none")
    console.print(plan)
    runtime = Table(title="Runtime", show_header=False)
    runtime.add_row("Budget", f"{result.plan.budget_mb:.1f} MB declared capacity")
    runtime.add_row(
        "Resident at inference", f"{result.memory.declared_resident_capacity_mb:.1f} MB declared"
    )
    runtime.add_row("Host RSS", f"{result.memory.host_rss_mb:.1f} MB")
    accelerator = (
        f"{result.memory.accelerator_peak_allocated_mb:.1f} MB observed"
        if result.memory.accelerator_peak_allocated_mb is not None
        else f"unavailable ({result.memory.unavailable_reason})"
    )
    runtime.add_row("Accelerator peak", accelerator)
    runtime.add_row("Routing", f"{result.metrics.routing_ms:.3f} ms")
    runtime.add_row("Loading", f"{result.metrics.loading_ms:.3f} ms")
    runtime.add_row("End to end", f"{result.metrics.end_to_end_ms:.3f} ms")
    runtime.add_row(
        "Cache", f"{result.metrics.cache_hits} hit / {result.metrics.cache_misses} miss"
    )
    console.print(runtime)
    console.print(Panel(Text(result.text), title="Output", border_style="green"))
    if verbose:
        console.print_json(
            json.dumps(
                {
                    "routing": result.routing.model_dump(mode="json"),
                    "plan": result.plan.model_dump(mode="json"),
                    "events": [event.model_dump(mode="json") for event in result.runtime_events],
                }
            )
        )


@app.command()
def run(
    prompt: Annotated[str, typer.Option("--prompt", "-p", help="Prompt to route and run.")],
    config: Annotated[Path | None, typer.Option("--config", exists=True, dir_okay=False)] = None,
    model: Annotated[str | None, typer.Option("--model", help="Override base model path.")] = None,
    mode: Annotated[
        str | None,
        typer.Option("--mode", help="full_model, offload, or semantic_routing."),
    ] = None,
    seed: Annotated[int | None, typer.Option("--seed")] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Route one prompt and generate through the configured backend."""
    loaded = _config(config, seed)
    if model:
        loaded.backend.model_path = model
    if mode:
        loaded.mode = mode
    engine = SelectiveLLM.from_config(config=loaded)
    _render_result(prompt, engine, verbose=verbose)


@app.command()
def inspect(
    device: Annotated[str, typer.Option("--device", help="auto, cuda, mps, or cpu")] = "auto",
) -> None:
    """Report hardware and available accelerator measurements."""
    info = inspect_hardware(device)
    table = Table(title=f"SelectiveLLM {__version__} hardware", show_header=False)
    for key, value in info.to_dict().items():
        table.add_row(
            key.replace("_", " ").title(), str(value if value is not None else "unavailable")
        )
    console.print(table)


@app.command()
def profile(
    prompt: Annotated[str, typer.Option("--prompt", "-p")],
    config: Annotated[Path | None, typer.Option("--config", exists=True, dir_okay=False)] = None,
    seed: Annotated[int | None, typer.Option("--seed")] = None,
) -> None:
    """Print stage-separated latency and memory data as JSON."""
    result = _engine(config, seed).generate(prompt)
    payload = {
        "backend": result.backend,
        "backend_kind": result.backend_kind,
        "measurement_warning": (
            "declared capacity is simulated; this is not a VRAM result"
            if result.backend_kind == "control"
            else None
        ),
        "metrics": result.metrics.model_dump(mode="json"),
        "memory": result.memory.model_dump(mode="json"),
        "runtime_events": [event.model_dump(mode="json") for event in result.runtime_events],
    }
    console.print_json(json.dumps(payload))


@app.command()
def demo(
    seed: Annotated[int, typer.Option("--seed")] = 42,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Run a labeled offline multi-domain control demonstration."""
    console.print(
        Panel(
            Text(
                "Offline deterministic-control demo\n"
                "Declared expert capacity is simulated. Host RAM is observed. "
                "No physical VRAM or model-quality claim is made.",
                style="bold",
            ),
            border_style="yellow",
        )
    )
    engine = SelectiveLLM.from_config(config=_config(None, seed))
    prompts = [
        "Implement binary search in Python.",
        "Derive the cutoff frequency of an RC low-pass circuit.",
        "Use Python to simulate an RLC circuit and plot the transient response.",
        "What is the capital of Japan?",
    ]
    for prompt in prompts:
        _render_result(prompt, engine, verbose=verbose)
    console.print(
        f"[bold green]Demo complete.[/bold green] Resident cache: {', '.join(engine.runtime.resident)}"
    )


@app.command()
def benchmark(
    config: Annotated[Path | None, typer.Option("--config", exists=True, dir_okay=False)] = None,
    router: Annotated[
        str | None, typer.Option("--router", help="Run one router/method only.")
    ] = None,
    report: Annotated[bool, typer.Option("--report/--no-report")] = True,
    repetitions: Annotated[int, typer.Option("--repetitions", min=1)] = 1,
    seed: Annotated[int | None, typer.Option("--seed")] = None,
    output: Annotated[Path, typer.Option("--output")] = Path("results"),
) -> None:
    """Run the versioned hero experiment and write reproducible artifacts."""
    loaded = _config(config, seed)
    methods = [router] if router else None
    runner = BenchmarkRunner(loaded, results_root=output)
    console.print(
        "[yellow]Running deterministic-control benchmark; declared capacity is simulated.[/yellow]"
        if loaded.backend.type == "deterministic"
        else "[cyan]Running real Transformers/PEFT benchmark.[/cyan]"
    )
    path = runner.run(methods=methods, repetitions=repetitions, report=report)
    console.print(f"[bold green]Completed:[/bold green] {path}")
    console.print(f"Report: {path / 'report.md'}" if report else "Report generation disabled.")


@registry_app.command("list")
def registry_list(
    config: Annotated[Path | None, typer.Option("--config", exists=True, dir_okay=False)] = None,
) -> None:
    """List configured capacity components."""
    engine = _engine(config)
    table = Table(title=f"Capacity registry {engine.registry.version}")
    table.add_column("ID")
    table.add_column("Type")
    table.add_column("Domains")
    table.add_column("Declared MB", justify="right")
    table.add_column("Backend")
    for component in engine.registry.all():
        table.add_row(
            component.id,
            component.type.value,
            ", ".join(component.domain),
            f"{component.memory_mb:.1f}",
            component.backend,
        )
    console.print(table)
    console.print("[yellow]Declared MB is registry metadata, not observed VRAM.[/yellow]")


@registry_app.command("inspect")
def registry_inspect(
    component_id: str,
    config: Annotated[Path | None, typer.Option("--config", exists=True, dir_okay=False)] = None,
) -> None:
    """Inspect one capacity component and its dependencies."""
    component = _engine(config).registry.get(component_id)
    console.print_json(component.model_dump_json(indent=2))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
