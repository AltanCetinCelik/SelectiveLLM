# SelectiveLLM v0.1.1 real-model evidence

## Result in one sentence

On an Apple M4, SelectiveLLM genuinely loaded, activated, composed, cached, and evicted three independently trained LoRA capacities around a shared Qwen2.5-1.5B base, and measured a real live-tensor residency tradeoff, but this nine-case run did **not** show that better routing reliably produced better answers.

This is a negative scientific result and a positive systems result. It is not evidence for parameter-level semantic paging.

## Run contract

- Run: `20260904T131326Z`
- Backend: `transformers-peft` (`real`)
- Fingerprint: `a24ac14e5122d5681ddf091602c57777897c6a637d578ce6407dc8031fe51b03`
- Hardware: MacBook Air `Mac16,12`, Apple M4, 10 CPU cores, 8 GPU cores, 16 GB unified memory, Metal 4, MPS
- Disk: 15 GiB available before asset download; 10 GiB available after the completed run
- Software: macOS 26.5.2, Python 3.12.14, PyTorch 2.14.0, Transformers 5.16.1, PEFT 0.20.0
- Benchmark: `real-hero-1.0.0`, 9 fixed cases, 11 policies, 396 primary observations and 18 RLC matrix observations
- Repetition policy: one cold ordered workload and three warm repetitions per policy, greedy decoding, seed 42, maximum 96 new tokens
- Quality: fixed exact, numeric, and concept-coverage rubrics from `deterministic-rubric-1.0.0`; no synthetic capability score and no LLM judge

The 27 warm observations per policy are three repetitions of the same nine authored cases. Confidence intervals in `summary.json` describe those observations; they are not population-level claims, and the cases are not independent draws.

## Pinned capacity

| Role | Hugging Face asset | Exact revision | Reported training source |
|---|---|---|---|
| Base | [`Qwen/Qwen2.5-1.5B-Instruct`](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) | `989aa7980e4cf806f80c7fef2b1adb7bc71aa306` | Qwen instruction model |
| Code | [`uditjain/lori-qwen2.5-1.5b-code`](https://huggingface.co/uditjain/lori-qwen2.5-1.5b-code) | `e937bbd728f28a441163f94b60ea5a119513e351` | CodeAlpaca-20k and Python Code Instructions 18k |
| Math | [`uditjain/lori-qwen2.5-1.5b-math`](https://huggingface.co/uditjain/lori-qwen2.5-1.5b-math) | `f992ab536c07761c67bd46e35c787bb68ea97657` | MetaMathQA |
| Science | [`uditjain/lori-qwen2.5-1.5b-science`](https://huggingface.co/uditjain/lori-qwen2.5-1.5b-science) | `398cf3cc78a3ff8c78c84c3a424da3ba994bdd6f` | SciQ |

The compatibility preflight resolved every requested revision, license, base identity, and tokenizer. All assets report Apache-2.0. Each adapter is PEFT LoRA rank 32, alpha 64, targets the same seven projection modules, and occupies 147,770,496 bytes on disk. These adapters were independently produced by `uditjain`; SelectiveLLM did not train or alter them.

## Warm results

Every value below is a warm mean unless labeled as a count or rate. MPS live and Metal driver allocation are separate Apple unified-memory signals, not discrete VRAM.

| Policy | Quality | Routing F1 | Resident adapters | MPS live MB | Driver MB | Load ms | End-to-end ms | Request hit rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Base only | 0.267 | 0.222 | 0.000 | 2968.777 | 3170.750 | 0.000 | 9261.644 | N/A |
| Random | 0.370 | 0.278 | 1.000 | 3110.121 | 3280.380 | 734.933 | 10937.697 | 0.000 |
| Keyword | 0.350 | 0.611 | 0.667 | 3063.006 | 3282.750 | 582.213 | 10573.937 | 0.000 |
| Oracle | 0.370 | 1.000 | 1.111 | 3157.253 | 3614.251 | 861.736 | 8594.039 | 0.000 |
| Semantic, cache 0, low locality | 0.378 | 0.830 | 1.000 | 3125.732 | 3464.380 | 796.888 | 9019.740 | 0.000 |
| Semantic, cache 1, low locality | 0.378 | 0.830 | 1.111 | 3141.384 | 3458.750 | 755.753 | 9274.428 | 0.111 |
| Semantic, cache 3, low locality | 0.370 | 0.830 | 3.000 | 3413.141 | 3602.750 | 0.000 | 7846.743 | 1.000 |
| Semantic, cache 0, high locality | 0.370 | 0.830 | 1.000 | 3125.732 | 3462.306 | 1086.235 | 10384.556 | 0.000 |
| Semantic, cache 1, high locality | 0.378 | 0.830 | 1.111 | 3141.384 | 3463.961 | 521.498 | 9751.902 | 0.556 |
| Semantic, cache 3, high locality | 0.370 | 0.830 | 3.000 | 3413.138 | 3602.750 | 0.000 | 5612.470 | 1.000 |
| All resident, semantic active | 0.370 | 0.830 | 3.000 | 3412.159 | 3602.750 | 0.000 | 8296.277 | 1.000 |

The full mean, median, sample standard deviation, p50, p95, and normal-approximation 95% interval for each metric are in `results/real/latest/summary.json` and `summary.csv`.

![Observed real quality-memory tradeoff](../results/real/latest/plots/real_quality_vs_memory.png)

## What happened

### Routing

The feature-hash/keyword hybrid called semantic routing reached 0.830 mean multi-label F1, versus 0.611 keyword, 0.278 random, and 1.000 oracle. It correctly suppressed an adapter for the capital-of-Japan case. It missed the math expert on the two multi-domain circuit cases and incorrectly activated the code expert for the python-species lexical trap. This router is transparent and reproducible, but it is not a learned sentence-embedding model.

### Output quality

Oracle and semantic policies averaged about 0.104 above base, but random routing achieved the same 0.370 aggregate quality as oracle. The 95% descriptive quality intervals overlap broadly: semantic cache-0 low `[0.244, 0.512]`, random `[0.234, 0.506]`, and keyword `[0.207, 0.493]`.

Correct specialization helped four cases: binary search `+0.500`, RC filter `+0.333`, MOSFET `+0.250`, and the irrationality proof `+0.250` for oracle versus base. It did not help FastAPI or dice probability, and three-expert oracle composition reduced RLC quality by `0.400`. Better routing therefore did not translate into a reliable aggregate quality advantage.

The fixed 96-token cap was reached in 136 of 297 warm observations (45.8%), including every warm dice and proof response. The dice answer was often truncated before the final fraction. This does not invalidate the recorded score under the fixed decoding contract, but it materially limits claims about unconstrained adapter quality.

### Real memory behavior

The base occupied 2968.777 MB of MPS current live tensor allocation. Loading all three source adapters raised this lifecycle checkpoint to 3396.121 MB, a measured 427.344 MB increase that closely tracks three 140.92 MB adapter files.

During generation, dynamic semantic cache-0 averaged 3125.732 MB versus 3412.159 MB for all-resident, 286.427 MB less live tensor allocation. That is 8.4% of the full all-resident allocation and about 64.6% of the all-resident expert-over-base increment. The cache-1 policy averaged 3141.384 MB. Cache-3 retained every source adapter and therefore converged to all-resident memory.

Multi-adapter inference used a PEFT weighted-linear derived adapter because direct simultaneous activation was unsupported. That derived adapter added roughly another adapter-sized live allocation. This is why multi-capability peaks exceed the source-adapter count alone.

Metal driver allocation did not fall with ordinary adapter eviction because it includes allocator cache and framework memory. At the end of the RLC matrix, live allocation returned to the 2968.777 MB base level while driver allocation remained 3602.750 MB. Host RSS is also recorded, but it overlaps with MPS on unified memory and is never added to either MPS value.

### Loading and cache behavior

Warm adapter loads averaged 899.1 ms for code, 793.9 ms for math, and 925.2 ms for science. Unloads averaged 114.5 to 120.0 ms. One active adapter took 10.3 ms mean activation; weighted composition took 1279.9 ms for two sources and 1547.2 ms for three.

For the same high-locality order, cache size 1 raised request hit rate from 0% to 55.6%, reduced loads and evictions from 27 to 12, and reduced mean load-stage time by 564.7 ms per prompt. Under adversarial low locality it reached only 11.1%, reduced loads from 27 to 24, and recovered just 41.1 ms of mean load time. Cache size 3 reached 100% after cold fill but surrendered the memory benefit.

End-to-end timings cannot be attributed solely to caching because policies ran sequentially rather than in randomized counterbalanced order, generation dominates runtime, and later MPS executions may benefit from process-level compilation or thermal state. The load-stage and event-count comparisons are the defensible cache evidence from this run.

### Multi-domain RLC result

| Active capacity | Mean quality | Outcome |
|---|---:|---|
| Base only | 0.400 | Best tied result |
| Code only | 0.400 | Best tied result |
| Science only | 0.000 | Degraded |
| Code + science | 0.067 | Weighted composition worked technically but degraded quality |
| Semantic | 0.067 | Selected code + science and missed math |
| Oracle | 0.000 | Composed code + science + math and degraded most |

The multi-label router and runtime worked, but adapter composition did not preserve quality. The 96-token cap also affected 19 warm RLC observations across the main policy matrix, so this result should motivate a pre-registered longer-decoding replication rather than a claim that composition is universally harmful.

## Answers to the approved questions

1. **Did semantic beat random routing?** Yes on routing F1 by 0.552; no defensible output-quality advantage was observed.
2. **Did it beat keyword?** Yes on routing F1 by 0.219; quality was only 0.020 to 0.028 higher and intervals overlapped.
3. **How close was it to oracle?** F1 was 0.830 versus 1.000; aggregate quality matched or exceeded oracle by at most 0.007 due to response variation.
4. **Did correct routing improve output?** It improved four cases, tied several, and harmed RLC composition. Random tied oracle overall, so the causal link was not established.
5. **How much expert capacity remained resident?** Dynamic cache-0 averaged 1.000 source adapter, cache-1 1.111, and cache-3/all-resident 3.000 before inference.
6. **What physical difference was measurable?** Dynamic semantic used 286.427 MB less mean MPS live tensor allocation than all-resident during warm generation. This is unified-memory tensor allocation, not discrete VRAM.
7. **What did swapping cost?** Roughly 0.8 to 0.9 seconds per adapter load plus about 0.115 seconds per unload; multi-source derived composition added about 1.3 to 1.5 seconds of activation.
8. **What did caching recover?** Cache-1 recovered 564.7 ms of mean load-stage work at high locality but only 41.1 ms at low locality. Cache-3 removed warm loads by keeping all experts resident.
9. **How did multi-domain prompts behave?** The router retained multiple labels but missed math under the two-expert limit; weighted composition worked technically and performed worse than base/code-only on RLC.
10. **Where did routing fail?** The Python lexical trap caused an unnecessary code activation, and both circuit multi-domain cases lost math recall.
11. **What contradicted the hypothesis?** Random tied oracle quality, routing gains did not predict aggregate quality, and multi-adapter composition degraded the hero case.
12. **Continue toward finer-grained routing?** Continue systems work at adapter granularity, but do not claim evidence for parameter paging. Quality validation must come first.

## Recommended next experiment

Choose **E: expert training improvements**, interpreted first as expert validation. Pre-register a larger held-out per-domain suite, increase the generation budget enough to avoid systematic truncation, evaluate every adapter alone against base and oracle, and retain the same hostile controls. Only adapters that demonstrate repeatable specialization should enter a rerun of the routing experiment. Then test composition separately with an interference-aware method before considering a larger pool, learned routing, or activation tracing.

The central hypothesis would be weakened for this adapter family if that replication again finds that oracle selection cannot beat random and base after adequate decoding, or if loading/composition overhead leaves no useful memory-quality-latency operating point.

## Evidence boundary

v0.1.1 demonstrated real prompt-level retrieval over independently defined adapter capacity, real residency control, measured MPS live-memory changes, real load/eviction costs, and locality-dependent cache behavior. It did not demonstrate a semantic-router quality advantage, reliable multi-adapter composition, discrete VRAM savings, generalization beyond nine authored cases, or parameter-level paging inside a dense model.

Primary artifacts: [report](../results/real/latest/report.md), [manifest](../results/real/latest/manifest.json), [compatibility preflight](../results/real/latest/compatibility_report.json), [raw responses](../results/real/latest/raw_responses.jsonl), [raw telemetry](../results/real/latest/telemetry.jsonl), [routing decisions](../results/real/latest/routing_decisions.jsonl), [RLC matrix](../results/real/latest/rlc_matrix.jsonl), and [failure analysis](../results/real/latest/failure_analysis.md).
