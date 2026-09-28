# SelectiveLLM Roadmap

SelectiveLLM is being developed along two related but independent tracks:

1. **Adaptive Runtime** — selecting and managing independently loadable model capacity under runtime constraints.
2. **Selective Dense Compute** — investigating whether useful prompt-conditioned structure can eventually be exploited inside dense models.

The second track is higher-risk research.

The first track does not depend on dense semantic parameter localization succeeding.

---

# Track A — Adaptive Runtime

## v0.1 — Research framework

Completed:

- typed prompt analysis,
- multiple routing policies,
- capacity registry,
- memory-budget planner,
- runtime loading,
- dependency-aware cache behavior,
- metrics and hardware inspection,
- deterministic control backend,
- Transformers / PEFT backend,
- reproducible benchmark infrastructure,
- CLI and Python API,
- CI and network-free unit tests.

---

## v0.1.1 — Real adapter evidence

Completed:

- pinned Qwen2.5-1.5B + PEFT experiment,
- code / math / science adapter pool,
- real MPS live-memory telemetry,
- adapter residency measurements,
- load and eviction latency,
- cache locality measurements,
- multi-adapter composition experiment,
- raw response preservation,
- failure analysis.

Result:

Runtime selective loading was demonstrated.

A reliable output-quality advantage from the existing router was not established.

---

# v0.2 — Adaptive Compute Router

Primary goal:

> Replace the deterministic routing prototype with a learned, calibrated, cost-aware capacity decision layer.

## 1. Learned capacity router

Implement a trainable routing backend capable of producing:

```text
capacity_id -> probability
```

Example:

```text
code_adapter        0.94
math_adapter        0.21
science_adapter     0.04
base_only           0.02
```

Required baselines:

- random,
- keyword,
- deterministic feature hash,
- embedding similarity,
- learned classifier,
- oracle.

---

## 2. Probability calibration

Routing confidence must become measurable rather than cosmetic.

Evaluate:

- Expected Calibration Error,
- Brier score,
- reliability diagrams,
- confidence-conditioned accuracy.

Support calibration methods such as:

- temperature scaling,
- Platt-style calibration where appropriate,
- isotonic calibration where appropriate.

---

## 3. Abstention and fallback

Add uncertainty-aware execution.

Example policy:

```text
if confidence >= threshold:
    use selected capacity
else:
    use safe fallback
```

Fallback targets may include:

- base model,
- all-resident capacity,
- larger model,
- external controller.

The abstention rate must be reported alongside quality and cost.

---

## 4. Utility-aware planning

The current planner primarily enforces a memory budget.

v0.2 should support utility-aware selection.

Conceptual objective:

```text
utility(component | request)
    =
expected quality gain
    - memory cost
    - loading latency
    - cache miss cost
    - uncertainty penalty
```

Selection should support constraints such as:

```text
memory <= B
latency <= L
```

The planner should expose why each component was selected or rejected.

---

## 5. Larger held-out benchmark

Replace the current small authored routing evaluation with a substantially larger held-out workload.

Requirements:

- train / calibration / test separation,
- unseen prompts,
- multi-domain examples,
- irrelevant-domain examples,
- ambiguous examples,
- mixed capability requests,
- repeated order permutations,
- fixed generation settings.

Where appropriate, incorporate public benchmark sources rather than relying entirely on authored prompts.

---

## 6. Counterbalanced workload execution

Routing and cache experiments must not depend on one fixed request order.

Run:

- random workload permutations,
- high-locality sequences,
- low-locality sequences,
- adversarial switching sequences.

Report separately:

- routing quality,
- cache hit rate,
- transfer count,
- cold-start latency,
- warm latency.

---

## 7. Pareto evaluation

Do not optimize only for routing accuracy.

Report Pareto relationships across:

```text
quality
memory
latency
loading cost
cache locality
uncertainty
```

A routing policy is useful only if it creates an operating point that is preferable to simpler baselines.

---

## 8. Capacity abstraction

Generalize independently selectable resources beyond the current adapter use case.

Target abstraction:

```text
CapacityComponent
    kind:
        adapter
        expert
        model
        block

    cost:
        memory
        load_latency
        runtime_latency

    dependencies:
        [...]

    metadata:
        ...
```

Future extensions may include tool or retrieval resources, but model capacity remains the primary scope of SelectiveLLM.

---

## 9. Multi-model routing

Add independently executable model candidates.

Example:

```text
small general model
coding specialist
math specialist
large fallback model
```

Measure whether SelectiveLLM can choose useful capacity while accounting for:

- quality,
- resident memory,
- model startup cost,
- transfer latency,
- cache state.

---

## 10. Installation and demo

Target user experience:

```bash
pip install selectivellm
selectivellm demo
```

The demo should expose:

- routing probabilities,
- uncertainty,
- capacity cost,
- selected capacity,
- rejected capacity,
- runtime memory,
- cache behavior,
- latency.

---

# Track B — Selective Dense Compute

This is a separate high-risk research direction.

The goal is to determine whether dense language models contain stable prompt-conditioned capacity that can eventually be exploited for real compute or memory savings.

---

## Completed dense feasibility work

Completed:

- activation-based discovery,
- gradient × activation discovery,
- attention-head analysis,
- layer analysis,
- contiguous MLP block experiments,
- held-out causal ablations,
- matched random controls,
- wrong-domain controls,
- Qwen2.5-1.5B experiment,
- Qwen2.5-3B replication.

Both main experiments returned the preregistered equivalent of:

```text
Outcome C:
weak or unstable specialization
```

These results are preserved.

---

## Dense-track gate

No physical semantic paging implementation should be claimed until the following are demonstrated:

1. stable causal importance across held-out prompts,
2. stability across paraphrases,
3. consistent same-domain advantage,
4. advantage over random masks,
5. advantage over matched pruning baselines,
6. useful composition across domains,
7. mapping to hardware-efficient execution units,
8. measurable physical memory or compute savings,
9. retained downstream quality.

Logical masking alone is not sufficient.

---

## Next dense experiment

Do not continue nearby same-family scale escalation automatically.

The next experiment should change a meaningful variable such as:

- model family,
- architecture,
- substantially larger model scale,
- training regime,
- discovery granularity.

The experiment must be preregistered before held-out results are inspected.

---

# Long-term direction

SelectiveLLM ultimately targets request-conditioned computation:

```text
request
   ↓
controller
   ↓
Which model?
Which expert?
Which adapter?
How much capacity?
What should remain resident?
What should be loaded?
When should the system abstain?
   ↓
minimum sufficient computation
```

The long-term objective is:

> preserve useful model quality while spending only the memory, latency, and compute required for the current request.
