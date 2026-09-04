# Routing Failure Analysis

Failures are retained by policy. Scores below are backend-specific and must be read with the run manifest.

## random / py_binary_search / repetition 0

**Prompt:** Implement binary search in Python and state its time complexity.

**Expected:** `['python_expert']`
**Selected:** `['math_expert', 'reasoning_expert']`
**Confidence:** `0.938`
**Scores:** `{'math_expert': 0.9380959440344502, 'reasoning_expert': 0.8040658104426929, 'scientific_writing_expert': 0.7531323911517029, 'software_engineering_expert': 0.5436544377954576, 'electrical_engineering_expert': 0.5425781165511119, 'python_expert': 0.16339827955689035}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / py_fastapi / repetition 0

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['scientific_writing_expert', 'reasoning_expert']`
**Confidence:** `0.939`
**Scores:** `{'scientific_writing_expert': 0.9386772041024447, 'reasoning_expert': 0.7964557611363805, 'electrical_engineering_expert': 0.6663004010218379, 'python_expert': 0.3747146241172683, 'math_expert': 0.25270279496780756, 'software_engineering_expert': 0.13962982665673074}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / py_paraphrase / repetition 0

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `['software_engineering_expert', 'scientific_writing_expert']`
**Confidence:** `0.965`
**Scores:** `{'software_engineering_expert': 0.9654073107470069, 'scientific_writing_expert': 0.9089966549926075, 'python_expert': 0.8626458841961201, 'math_expert': 0.7084635276847095, 'reasoning_expert': 0.23527606162315717, 'electrical_engineering_expert': 0.1775718576812353}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / math_integral / repetition 0

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert', 'scientific_writing_expert']`
**Confidence:** `0.971`
**Scores:** `{'math_expert': 0.9714106098366966, 'scientific_writing_expert': 0.8912106190687142, 'software_engineering_expert': 0.7233464108745224, 'python_expert': 0.6543349624605656, 'reasoning_expert': 0.34631392090874247, 'electrical_engineering_expert': 0.11791959774741911}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / math_probability / repetition 0

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.941`
**Scores:** `{'electrical_engineering_expert': 0.9407619520310853, 'python_expert': 0.9291982133385251, 'math_expert': 0.8727800550871097, 'scientific_writing_expert': 0.6730009730144768, 'reasoning_expert': 0.24874824419246822, 'software_engineering_expert': 0.1180763620352131}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / math_proof / repetition 0

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['python_expert', 'software_engineering_expert']`
**Confidence:** `0.978`
**Scores:** `{'python_expert': 0.9775197528387026, 'software_engineering_expert': 0.6271374440781138, 'reasoning_expert': 0.6249657442849668, 'electrical_engineering_expert': 0.38008844052260216, 'scientific_writing_expert': 0.35891818137558484, 'math_expert': 0.18332463070966531}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / ee_mosfet / repetition 0

**Prompt:** Explain why a MOSFET gate driver must source and sink current quickly.

**Expected:** `['electrical_engineering_expert']`
**Selected:** `['python_expert', 'math_expert']`
**Confidence:** `0.864`
**Scores:** `{'python_expert': 0.8644091384278695, 'math_expert': 0.8504035411254627, 'software_engineering_expert': 0.7937442060983931, 'electrical_engineering_expert': 0.7773034231271972, 'reasoning_expert': 0.7039593738482787, 'scientific_writing_expert': 0.2625813494760483}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / ee_filter / repetition 0

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['scientific_writing_expert', 'reasoning_expert']`
**Confidence:** `0.676`
**Scores:** `{'scientific_writing_expert': 0.6758705175984904, 'reasoning_expert': 0.5566145762869753, 'electrical_engineering_expert': 0.5523313928727486, 'software_engineering_expert': 0.48622441164039265, 'math_expert': 0.3458016773705105, 'python_expert': 0.27891627365033833}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / rlc_python / repetition 0

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['scientific_writing_expert', 'electrical_engineering_expert']`
**Confidence:** `0.947`
**Scores:** `{'scientific_writing_expert': 0.9468481647627406, 'electrical_engineering_expert': 0.9210927068047888, 'software_engineering_expert': 0.894150130227921, 'math_expert': 0.740550597193634, 'reasoning_expert': 0.30042366604899884, 'python_expert': 0.0013312194836664348}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / reasoning_logic / repetition 0

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['python_expert', 'math_expert']`
**Confidence:** `0.703`
**Scores:** `{'python_expert': 0.7027315650629974, 'math_expert': 0.4706849834615232, 'reasoning_expert': 0.374368665294608, 'scientific_writing_expert': 0.3203246236006344, 'software_engineering_expert': 0.2727681496679851, 'electrical_engineering_expert': 0.04763247172914331}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / general_capital / repetition 0

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `['python_expert', 'scientific_writing_expert']`
**Confidence:** `0.878`
**Scores:** `{'python_expert': 0.878465467767137, 'scientific_writing_expert': 0.8579468728765545, 'reasoning_expert': 0.5979144798821951, 'electrical_engineering_expert': 0.4821596265023209, 'math_expert': 0.24875559956288762, 'software_engineering_expert': 0.03760246099560649}`
**Quality:** `0.900` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## random / general_summary / repetition 0

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['math_expert', 'software_engineering_expert']`
**Confidence:** `0.954`
**Scores:** `{'math_expert': 0.9540963543786382, 'software_engineering_expert': 0.9412993388110645, 'python_expert': 0.6131124334862246, 'electrical_engineering_expert': 0.5952029615650318, 'scientific_writing_expert': 0.368509117645598, 'reasoning_expert': 0.3592774772000318}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / irrelevant_python / repetition 0

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['math_expert', 'electrical_engineering_expert']`
**Confidence:** `0.942`
**Scores:** `{'math_expert': 0.9424842238963019, 'electrical_engineering_expert': 0.8163348741912293, 'python_expert': 0.31517237908498663, 'scientific_writing_expert': 0.21796924685495023, 'reasoning_expert': 0.20535080002176487, 'software_engineering_expert': 0.07806940564023657}`
**Quality:** `0.900` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## random / irrelevant_current / repetition 0

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['math_expert', 'python_expert']`
**Confidence:** `0.568`
**Scores:** `{'math_expert': 0.5682826890566011, 'python_expert': 0.4230344616587133, 'reasoning_expert': 0.38908914550891394, 'software_engineering_expert': 0.3600758149613076, 'electrical_engineering_expert': 0.2944478490032063, 'scientific_writing_expert': 0.04260019923101421}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / scientific_abstract / repetition 0

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['reasoning_expert', 'software_engineering_expert']`
**Confidence:** `0.823`
**Scores:** `{'reasoning_expert': 0.823019000326674, 'software_engineering_expert': 0.6691929421036884, 'electrical_engineering_expert': 0.5665832471693156, 'scientific_writing_expert': 0.5264014872004104, 'math_expert': 0.3390591936196147, 'python_expert': 0.24674755565681528}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / py_binary_search / repetition 1

**Prompt:** Implement binary search in Python and state its time complexity.

**Expected:** `['python_expert']`
**Selected:** `['math_expert', 'reasoning_expert']`
**Confidence:** `0.938`
**Scores:** `{'math_expert': 0.9380959440344502, 'reasoning_expert': 0.8040658104426929, 'scientific_writing_expert': 0.7531323911517029, 'software_engineering_expert': 0.5436544377954576, 'electrical_engineering_expert': 0.5425781165511119, 'python_expert': 0.16339827955689035}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / py_fastapi / repetition 1

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['scientific_writing_expert', 'reasoning_expert']`
**Confidence:** `0.939`
**Scores:** `{'scientific_writing_expert': 0.9386772041024447, 'reasoning_expert': 0.7964557611363805, 'electrical_engineering_expert': 0.6663004010218379, 'python_expert': 0.3747146241172683, 'math_expert': 0.25270279496780756, 'software_engineering_expert': 0.13962982665673074}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / py_paraphrase / repetition 1

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `['software_engineering_expert', 'scientific_writing_expert']`
**Confidence:** `0.965`
**Scores:** `{'software_engineering_expert': 0.9654073107470069, 'scientific_writing_expert': 0.9089966549926075, 'python_expert': 0.8626458841961201, 'math_expert': 0.7084635276847095, 'reasoning_expert': 0.23527606162315717, 'electrical_engineering_expert': 0.1775718576812353}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / math_integral / repetition 1

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert', 'scientific_writing_expert']`
**Confidence:** `0.971`
**Scores:** `{'math_expert': 0.9714106098366966, 'scientific_writing_expert': 0.8912106190687142, 'software_engineering_expert': 0.7233464108745224, 'python_expert': 0.6543349624605656, 'reasoning_expert': 0.34631392090874247, 'electrical_engineering_expert': 0.11791959774741911}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / math_probability / repetition 1

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.941`
**Scores:** `{'electrical_engineering_expert': 0.9407619520310853, 'python_expert': 0.9291982133385251, 'math_expert': 0.8727800550871097, 'scientific_writing_expert': 0.6730009730144768, 'reasoning_expert': 0.24874824419246822, 'software_engineering_expert': 0.1180763620352131}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / math_proof / repetition 1

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['python_expert', 'software_engineering_expert']`
**Confidence:** `0.978`
**Scores:** `{'python_expert': 0.9775197528387026, 'software_engineering_expert': 0.6271374440781138, 'reasoning_expert': 0.6249657442849668, 'electrical_engineering_expert': 0.38008844052260216, 'scientific_writing_expert': 0.35891818137558484, 'math_expert': 0.18332463070966531}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / ee_mosfet / repetition 1

**Prompt:** Explain why a MOSFET gate driver must source and sink current quickly.

**Expected:** `['electrical_engineering_expert']`
**Selected:** `['python_expert', 'math_expert']`
**Confidence:** `0.864`
**Scores:** `{'python_expert': 0.8644091384278695, 'math_expert': 0.8504035411254627, 'software_engineering_expert': 0.7937442060983931, 'electrical_engineering_expert': 0.7773034231271972, 'reasoning_expert': 0.7039593738482787, 'scientific_writing_expert': 0.2625813494760483}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / ee_filter / repetition 1

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['scientific_writing_expert', 'reasoning_expert']`
**Confidence:** `0.676`
**Scores:** `{'scientific_writing_expert': 0.6758705175984904, 'reasoning_expert': 0.5566145762869753, 'electrical_engineering_expert': 0.5523313928727486, 'software_engineering_expert': 0.48622441164039265, 'math_expert': 0.3458016773705105, 'python_expert': 0.27891627365033833}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / rlc_python / repetition 1

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['scientific_writing_expert', 'electrical_engineering_expert']`
**Confidence:** `0.947`
**Scores:** `{'scientific_writing_expert': 0.9468481647627406, 'electrical_engineering_expert': 0.9210927068047888, 'software_engineering_expert': 0.894150130227921, 'math_expert': 0.740550597193634, 'reasoning_expert': 0.30042366604899884, 'python_expert': 0.0013312194836664348}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / reasoning_logic / repetition 1

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['python_expert', 'math_expert']`
**Confidence:** `0.703`
**Scores:** `{'python_expert': 0.7027315650629974, 'math_expert': 0.4706849834615232, 'reasoning_expert': 0.374368665294608, 'scientific_writing_expert': 0.3203246236006344, 'software_engineering_expert': 0.2727681496679851, 'electrical_engineering_expert': 0.04763247172914331}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / general_capital / repetition 1

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `['python_expert', 'scientific_writing_expert']`
**Confidence:** `0.878`
**Scores:** `{'python_expert': 0.878465467767137, 'scientific_writing_expert': 0.8579468728765545, 'reasoning_expert': 0.5979144798821951, 'electrical_engineering_expert': 0.4821596265023209, 'math_expert': 0.24875559956288762, 'software_engineering_expert': 0.03760246099560649}`
**Quality:** `0.900` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## random / general_summary / repetition 1

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['math_expert', 'software_engineering_expert']`
**Confidence:** `0.954`
**Scores:** `{'math_expert': 0.9540963543786382, 'software_engineering_expert': 0.9412993388110645, 'python_expert': 0.6131124334862246, 'electrical_engineering_expert': 0.5952029615650318, 'scientific_writing_expert': 0.368509117645598, 'reasoning_expert': 0.3592774772000318}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / irrelevant_python / repetition 1

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['math_expert', 'electrical_engineering_expert']`
**Confidence:** `0.942`
**Scores:** `{'math_expert': 0.9424842238963019, 'electrical_engineering_expert': 0.8163348741912293, 'python_expert': 0.31517237908498663, 'scientific_writing_expert': 0.21796924685495023, 'reasoning_expert': 0.20535080002176487, 'software_engineering_expert': 0.07806940564023657}`
**Quality:** `0.900` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## random / irrelevant_current / repetition 1

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['math_expert', 'python_expert']`
**Confidence:** `0.568`
**Scores:** `{'math_expert': 0.5682826890566011, 'python_expert': 0.4230344616587133, 'reasoning_expert': 0.38908914550891394, 'software_engineering_expert': 0.3600758149613076, 'electrical_engineering_expert': 0.2944478490032063, 'scientific_writing_expert': 0.04260019923101421}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / scientific_abstract / repetition 1

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['reasoning_expert', 'software_engineering_expert']`
**Confidence:** `0.823`
**Scores:** `{'reasoning_expert': 0.823019000326674, 'software_engineering_expert': 0.6691929421036884, 'electrical_engineering_expert': 0.5665832471693156, 'scientific_writing_expert': 0.5264014872004104, 'math_expert': 0.3390591936196147, 'python_expert': 0.24674755565681528}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / py_binary_search / repetition 2

**Prompt:** Implement binary search in Python and state its time complexity.

**Expected:** `['python_expert']`
**Selected:** `['math_expert', 'reasoning_expert']`
**Confidence:** `0.938`
**Scores:** `{'math_expert': 0.9380959440344502, 'reasoning_expert': 0.8040658104426929, 'scientific_writing_expert': 0.7531323911517029, 'software_engineering_expert': 0.5436544377954576, 'electrical_engineering_expert': 0.5425781165511119, 'python_expert': 0.16339827955689035}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / py_fastapi / repetition 2

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['scientific_writing_expert', 'reasoning_expert']`
**Confidence:** `0.939`
**Scores:** `{'scientific_writing_expert': 0.9386772041024447, 'reasoning_expert': 0.7964557611363805, 'electrical_engineering_expert': 0.6663004010218379, 'python_expert': 0.3747146241172683, 'math_expert': 0.25270279496780756, 'software_engineering_expert': 0.13962982665673074}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / py_paraphrase / repetition 2

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `['software_engineering_expert', 'scientific_writing_expert']`
**Confidence:** `0.965`
**Scores:** `{'software_engineering_expert': 0.9654073107470069, 'scientific_writing_expert': 0.9089966549926075, 'python_expert': 0.8626458841961201, 'math_expert': 0.7084635276847095, 'reasoning_expert': 0.23527606162315717, 'electrical_engineering_expert': 0.1775718576812353}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / math_integral / repetition 2

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert', 'scientific_writing_expert']`
**Confidence:** `0.971`
**Scores:** `{'math_expert': 0.9714106098366966, 'scientific_writing_expert': 0.8912106190687142, 'software_engineering_expert': 0.7233464108745224, 'python_expert': 0.6543349624605656, 'reasoning_expert': 0.34631392090874247, 'electrical_engineering_expert': 0.11791959774741911}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / math_probability / repetition 2

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.941`
**Scores:** `{'electrical_engineering_expert': 0.9407619520310853, 'python_expert': 0.9291982133385251, 'math_expert': 0.8727800550871097, 'scientific_writing_expert': 0.6730009730144768, 'reasoning_expert': 0.24874824419246822, 'software_engineering_expert': 0.1180763620352131}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / math_proof / repetition 2

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['python_expert', 'software_engineering_expert']`
**Confidence:** `0.978`
**Scores:** `{'python_expert': 0.9775197528387026, 'software_engineering_expert': 0.6271374440781138, 'reasoning_expert': 0.6249657442849668, 'electrical_engineering_expert': 0.38008844052260216, 'scientific_writing_expert': 0.35891818137558484, 'math_expert': 0.18332463070966531}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / ee_mosfet / repetition 2

**Prompt:** Explain why a MOSFET gate driver must source and sink current quickly.

**Expected:** `['electrical_engineering_expert']`
**Selected:** `['python_expert', 'math_expert']`
**Confidence:** `0.864`
**Scores:** `{'python_expert': 0.8644091384278695, 'math_expert': 0.8504035411254627, 'software_engineering_expert': 0.7937442060983931, 'electrical_engineering_expert': 0.7773034231271972, 'reasoning_expert': 0.7039593738482787, 'scientific_writing_expert': 0.2625813494760483}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / ee_filter / repetition 2

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['scientific_writing_expert', 'reasoning_expert']`
**Confidence:** `0.676`
**Scores:** `{'scientific_writing_expert': 0.6758705175984904, 'reasoning_expert': 0.5566145762869753, 'electrical_engineering_expert': 0.5523313928727486, 'software_engineering_expert': 0.48622441164039265, 'math_expert': 0.3458016773705105, 'python_expert': 0.27891627365033833}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / rlc_python / repetition 2

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['scientific_writing_expert', 'electrical_engineering_expert']`
**Confidence:** `0.947`
**Scores:** `{'scientific_writing_expert': 0.9468481647627406, 'electrical_engineering_expert': 0.9210927068047888, 'software_engineering_expert': 0.894150130227921, 'math_expert': 0.740550597193634, 'reasoning_expert': 0.30042366604899884, 'python_expert': 0.0013312194836664348}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / reasoning_logic / repetition 2

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['python_expert', 'math_expert']`
**Confidence:** `0.703`
**Scores:** `{'python_expert': 0.7027315650629974, 'math_expert': 0.4706849834615232, 'reasoning_expert': 0.374368665294608, 'scientific_writing_expert': 0.3203246236006344, 'software_engineering_expert': 0.2727681496679851, 'electrical_engineering_expert': 0.04763247172914331}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / general_capital / repetition 2

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `['python_expert', 'scientific_writing_expert']`
**Confidence:** `0.878`
**Scores:** `{'python_expert': 0.878465467767137, 'scientific_writing_expert': 0.8579468728765545, 'reasoning_expert': 0.5979144798821951, 'electrical_engineering_expert': 0.4821596265023209, 'math_expert': 0.24875559956288762, 'software_engineering_expert': 0.03760246099560649}`
**Quality:** `0.900` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## random / general_summary / repetition 2

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['math_expert', 'software_engineering_expert']`
**Confidence:** `0.954`
**Scores:** `{'math_expert': 0.9540963543786382, 'software_engineering_expert': 0.9412993388110645, 'python_expert': 0.6131124334862246, 'electrical_engineering_expert': 0.5952029615650318, 'scientific_writing_expert': 0.368509117645598, 'reasoning_expert': 0.3592774772000318}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / irrelevant_python / repetition 2

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['math_expert', 'electrical_engineering_expert']`
**Confidence:** `0.942`
**Scores:** `{'math_expert': 0.9424842238963019, 'electrical_engineering_expert': 0.8163348741912293, 'python_expert': 0.31517237908498663, 'scientific_writing_expert': 0.21796924685495023, 'reasoning_expert': 0.20535080002176487, 'software_engineering_expert': 0.07806940564023657}`
**Quality:** `0.900` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## random / irrelevant_current / repetition 2

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['math_expert', 'python_expert']`
**Confidence:** `0.568`
**Scores:** `{'math_expert': 0.5682826890566011, 'python_expert': 0.4230344616587133, 'reasoning_expert': 0.38908914550891394, 'software_engineering_expert': 0.3600758149613076, 'electrical_engineering_expert': 0.2944478490032063, 'scientific_writing_expert': 0.04260019923101421}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / scientific_abstract / repetition 2

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['reasoning_expert', 'software_engineering_expert']`
**Confidence:** `0.823`
**Scores:** `{'reasoning_expert': 0.823019000326674, 'software_engineering_expert': 0.6691929421036884, 'electrical_engineering_expert': 0.5665832471693156, 'scientific_writing_expert': 0.5264014872004104, 'math_expert': 0.3390591936196147, 'python_expert': 0.24674755565681528}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / py_binary_search / repetition 3

**Prompt:** Implement binary search in Python and state its time complexity.

**Expected:** `['python_expert']`
**Selected:** `['math_expert', 'reasoning_expert']`
**Confidence:** `0.938`
**Scores:** `{'math_expert': 0.9380959440344502, 'reasoning_expert': 0.8040658104426929, 'scientific_writing_expert': 0.7531323911517029, 'software_engineering_expert': 0.5436544377954576, 'electrical_engineering_expert': 0.5425781165511119, 'python_expert': 0.16339827955689035}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / py_fastapi / repetition 3

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['scientific_writing_expert', 'reasoning_expert']`
**Confidence:** `0.939`
**Scores:** `{'scientific_writing_expert': 0.9386772041024447, 'reasoning_expert': 0.7964557611363805, 'electrical_engineering_expert': 0.6663004010218379, 'python_expert': 0.3747146241172683, 'math_expert': 0.25270279496780756, 'software_engineering_expert': 0.13962982665673074}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / py_paraphrase / repetition 3

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `['software_engineering_expert', 'scientific_writing_expert']`
**Confidence:** `0.965`
**Scores:** `{'software_engineering_expert': 0.9654073107470069, 'scientific_writing_expert': 0.9089966549926075, 'python_expert': 0.8626458841961201, 'math_expert': 0.7084635276847095, 'reasoning_expert': 0.23527606162315717, 'electrical_engineering_expert': 0.1775718576812353}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / math_integral / repetition 3

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert', 'scientific_writing_expert']`
**Confidence:** `0.971`
**Scores:** `{'math_expert': 0.9714106098366966, 'scientific_writing_expert': 0.8912106190687142, 'software_engineering_expert': 0.7233464108745224, 'python_expert': 0.6543349624605656, 'reasoning_expert': 0.34631392090874247, 'electrical_engineering_expert': 0.11791959774741911}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / math_probability / repetition 3

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.941`
**Scores:** `{'electrical_engineering_expert': 0.9407619520310853, 'python_expert': 0.9291982133385251, 'math_expert': 0.8727800550871097, 'scientific_writing_expert': 0.6730009730144768, 'reasoning_expert': 0.24874824419246822, 'software_engineering_expert': 0.1180763620352131}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / math_proof / repetition 3

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['python_expert', 'software_engineering_expert']`
**Confidence:** `0.978`
**Scores:** `{'python_expert': 0.9775197528387026, 'software_engineering_expert': 0.6271374440781138, 'reasoning_expert': 0.6249657442849668, 'electrical_engineering_expert': 0.38008844052260216, 'scientific_writing_expert': 0.35891818137558484, 'math_expert': 0.18332463070966531}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / ee_mosfet / repetition 3

**Prompt:** Explain why a MOSFET gate driver must source and sink current quickly.

**Expected:** `['electrical_engineering_expert']`
**Selected:** `['python_expert', 'math_expert']`
**Confidence:** `0.864`
**Scores:** `{'python_expert': 0.8644091384278695, 'math_expert': 0.8504035411254627, 'software_engineering_expert': 0.7937442060983931, 'electrical_engineering_expert': 0.7773034231271972, 'reasoning_expert': 0.7039593738482787, 'scientific_writing_expert': 0.2625813494760483}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / ee_filter / repetition 3

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['scientific_writing_expert', 'reasoning_expert']`
**Confidence:** `0.676`
**Scores:** `{'scientific_writing_expert': 0.6758705175984904, 'reasoning_expert': 0.5566145762869753, 'electrical_engineering_expert': 0.5523313928727486, 'software_engineering_expert': 0.48622441164039265, 'math_expert': 0.3458016773705105, 'python_expert': 0.27891627365033833}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / rlc_python / repetition 3

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['scientific_writing_expert', 'electrical_engineering_expert']`
**Confidence:** `0.947`
**Scores:** `{'scientific_writing_expert': 0.9468481647627406, 'electrical_engineering_expert': 0.9210927068047888, 'software_engineering_expert': 0.894150130227921, 'math_expert': 0.740550597193634, 'reasoning_expert': 0.30042366604899884, 'python_expert': 0.0013312194836664348}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / reasoning_logic / repetition 3

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['python_expert', 'math_expert']`
**Confidence:** `0.703`
**Scores:** `{'python_expert': 0.7027315650629974, 'math_expert': 0.4706849834615232, 'reasoning_expert': 0.374368665294608, 'scientific_writing_expert': 0.3203246236006344, 'software_engineering_expert': 0.2727681496679851, 'electrical_engineering_expert': 0.04763247172914331}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / general_capital / repetition 3

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `['python_expert', 'scientific_writing_expert']`
**Confidence:** `0.878`
**Scores:** `{'python_expert': 0.878465467767137, 'scientific_writing_expert': 0.8579468728765545, 'reasoning_expert': 0.5979144798821951, 'electrical_engineering_expert': 0.4821596265023209, 'math_expert': 0.24875559956288762, 'software_engineering_expert': 0.03760246099560649}`
**Quality:** `0.900` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## random / general_summary / repetition 3

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['math_expert', 'software_engineering_expert']`
**Confidence:** `0.954`
**Scores:** `{'math_expert': 0.9540963543786382, 'software_engineering_expert': 0.9412993388110645, 'python_expert': 0.6131124334862246, 'electrical_engineering_expert': 0.5952029615650318, 'scientific_writing_expert': 0.368509117645598, 'reasoning_expert': 0.3592774772000318}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / irrelevant_python / repetition 3

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['math_expert', 'electrical_engineering_expert']`
**Confidence:** `0.942`
**Scores:** `{'math_expert': 0.9424842238963019, 'electrical_engineering_expert': 0.8163348741912293, 'python_expert': 0.31517237908498663, 'scientific_writing_expert': 0.21796924685495023, 'reasoning_expert': 0.20535080002176487, 'software_engineering_expert': 0.07806940564023657}`
**Quality:** `0.900` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## random / irrelevant_current / repetition 3

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['math_expert', 'python_expert']`
**Confidence:** `0.568`
**Scores:** `{'math_expert': 0.5682826890566011, 'python_expert': 0.4230344616587133, 'reasoning_expert': 0.38908914550891394, 'software_engineering_expert': 0.3600758149613076, 'electrical_engineering_expert': 0.2944478490032063, 'scientific_writing_expert': 0.04260019923101421}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / scientific_abstract / repetition 3

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['reasoning_expert', 'software_engineering_expert']`
**Confidence:** `0.823`
**Scores:** `{'reasoning_expert': 0.823019000326674, 'software_engineering_expert': 0.6691929421036884, 'electrical_engineering_expert': 0.5665832471693156, 'scientific_writing_expert': 0.5264014872004104, 'math_expert': 0.3390591936196147, 'python_expert': 0.24674755565681528}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / py_binary_search / repetition 4

**Prompt:** Implement binary search in Python and state its time complexity.

**Expected:** `['python_expert']`
**Selected:** `['math_expert', 'reasoning_expert']`
**Confidence:** `0.938`
**Scores:** `{'math_expert': 0.9380959440344502, 'reasoning_expert': 0.8040658104426929, 'scientific_writing_expert': 0.7531323911517029, 'software_engineering_expert': 0.5436544377954576, 'electrical_engineering_expert': 0.5425781165511119, 'python_expert': 0.16339827955689035}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / py_fastapi / repetition 4

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['scientific_writing_expert', 'reasoning_expert']`
**Confidence:** `0.939`
**Scores:** `{'scientific_writing_expert': 0.9386772041024447, 'reasoning_expert': 0.7964557611363805, 'electrical_engineering_expert': 0.6663004010218379, 'python_expert': 0.3747146241172683, 'math_expert': 0.25270279496780756, 'software_engineering_expert': 0.13962982665673074}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / py_paraphrase / repetition 4

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `['software_engineering_expert', 'scientific_writing_expert']`
**Confidence:** `0.965`
**Scores:** `{'software_engineering_expert': 0.9654073107470069, 'scientific_writing_expert': 0.9089966549926075, 'python_expert': 0.8626458841961201, 'math_expert': 0.7084635276847095, 'reasoning_expert': 0.23527606162315717, 'electrical_engineering_expert': 0.1775718576812353}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / math_integral / repetition 4

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert', 'scientific_writing_expert']`
**Confidence:** `0.971`
**Scores:** `{'math_expert': 0.9714106098366966, 'scientific_writing_expert': 0.8912106190687142, 'software_engineering_expert': 0.7233464108745224, 'python_expert': 0.6543349624605656, 'reasoning_expert': 0.34631392090874247, 'electrical_engineering_expert': 0.11791959774741911}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / math_probability / repetition 4

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.941`
**Scores:** `{'electrical_engineering_expert': 0.9407619520310853, 'python_expert': 0.9291982133385251, 'math_expert': 0.8727800550871097, 'scientific_writing_expert': 0.6730009730144768, 'reasoning_expert': 0.24874824419246822, 'software_engineering_expert': 0.1180763620352131}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / math_proof / repetition 4

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['python_expert', 'software_engineering_expert']`
**Confidence:** `0.978`
**Scores:** `{'python_expert': 0.9775197528387026, 'software_engineering_expert': 0.6271374440781138, 'reasoning_expert': 0.6249657442849668, 'electrical_engineering_expert': 0.38008844052260216, 'scientific_writing_expert': 0.35891818137558484, 'math_expert': 0.18332463070966531}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / ee_mosfet / repetition 4

**Prompt:** Explain why a MOSFET gate driver must source and sink current quickly.

**Expected:** `['electrical_engineering_expert']`
**Selected:** `['python_expert', 'math_expert']`
**Confidence:** `0.864`
**Scores:** `{'python_expert': 0.8644091384278695, 'math_expert': 0.8504035411254627, 'software_engineering_expert': 0.7937442060983931, 'electrical_engineering_expert': 0.7773034231271972, 'reasoning_expert': 0.7039593738482787, 'scientific_writing_expert': 0.2625813494760483}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / ee_filter / repetition 4

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['scientific_writing_expert', 'reasoning_expert']`
**Confidence:** `0.676`
**Scores:** `{'scientific_writing_expert': 0.6758705175984904, 'reasoning_expert': 0.5566145762869753, 'electrical_engineering_expert': 0.5523313928727486, 'software_engineering_expert': 0.48622441164039265, 'math_expert': 0.3458016773705105, 'python_expert': 0.27891627365033833}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / rlc_python / repetition 4

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['scientific_writing_expert', 'electrical_engineering_expert']`
**Confidence:** `0.947`
**Scores:** `{'scientific_writing_expert': 0.9468481647627406, 'electrical_engineering_expert': 0.9210927068047888, 'software_engineering_expert': 0.894150130227921, 'math_expert': 0.740550597193634, 'reasoning_expert': 0.30042366604899884, 'python_expert': 0.0013312194836664348}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / reasoning_logic / repetition 4

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['python_expert', 'math_expert']`
**Confidence:** `0.703`
**Scores:** `{'python_expert': 0.7027315650629974, 'math_expert': 0.4706849834615232, 'reasoning_expert': 0.374368665294608, 'scientific_writing_expert': 0.3203246236006344, 'software_engineering_expert': 0.2727681496679851, 'electrical_engineering_expert': 0.04763247172914331}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / general_capital / repetition 4

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `['python_expert', 'scientific_writing_expert']`
**Confidence:** `0.878`
**Scores:** `{'python_expert': 0.878465467767137, 'scientific_writing_expert': 0.8579468728765545, 'reasoning_expert': 0.5979144798821951, 'electrical_engineering_expert': 0.4821596265023209, 'math_expert': 0.24875559956288762, 'software_engineering_expert': 0.03760246099560649}`
**Quality:** `0.900` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## random / general_summary / repetition 4

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['math_expert', 'software_engineering_expert']`
**Confidence:** `0.954`
**Scores:** `{'math_expert': 0.9540963543786382, 'software_engineering_expert': 0.9412993388110645, 'python_expert': 0.6131124334862246, 'electrical_engineering_expert': 0.5952029615650318, 'scientific_writing_expert': 0.368509117645598, 'reasoning_expert': 0.3592774772000318}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## random / irrelevant_python / repetition 4

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['math_expert', 'electrical_engineering_expert']`
**Confidence:** `0.942`
**Scores:** `{'math_expert': 0.9424842238963019, 'electrical_engineering_expert': 0.8163348741912293, 'python_expert': 0.31517237908498663, 'scientific_writing_expert': 0.21796924685495023, 'reasoning_expert': 0.20535080002176487, 'software_engineering_expert': 0.07806940564023657}`
**Quality:** `0.900` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## random / irrelevant_current / repetition 4

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['math_expert', 'python_expert']`
**Confidence:** `0.568`
**Scores:** `{'math_expert': 0.5682826890566011, 'python_expert': 0.4230344616587133, 'reasoning_expert': 0.38908914550891394, 'software_engineering_expert': 0.3600758149613076, 'electrical_engineering_expert': 0.2944478490032063, 'scientific_writing_expert': 0.04260019923101421}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, relevant expert rejected by memory budget

## random / scientific_abstract / repetition 4

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['reasoning_expert', 'software_engineering_expert']`
**Confidence:** `0.823`
**Scores:** `{'reasoning_expert': 0.823019000326674, 'software_engineering_expert': 0.6691929421036884, 'electrical_engineering_expert': 0.5665832471693156, 'scientific_writing_expert': 0.5264014872004104, 'math_expert': 0.3390591936196147, 'python_expert': 0.24674755565681528}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation

## keyword / py_fastapi / repetition 0

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / py_paraphrase / repetition 0

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / math_integral / repetition 0

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / math_probability / repetition 0

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / math_proof / repetition 0

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.250`
**Scores:** `{'math_expert': 0.25, 'electrical_engineering_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / ee_mosfet / repetition 0

**Prompt:** Explain why a MOSFET gate driver must source and sink current quickly.

**Expected:** `['electrical_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / ee_filter / repetition 0

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / rlc_python / repetition 0

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['python_expert']`
**Confidence:** `0.333`
**Scores:** `{'python_expert': 0.3333333333333333, 'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## keyword / reasoning_schedule / repetition 0

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / reasoning_logic / repetition 0

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / general_capital / repetition 0

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## keyword / general_summary / repetition 0

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / irrelevant_python / repetition 0

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.333`
**Scores:** `{'python_expert': 0.3333333333333333, 'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## keyword / irrelevant_current / repetition 0

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / scientific_abstract / repetition 0

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / py_fastapi / repetition 1

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / py_paraphrase / repetition 1

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / math_integral / repetition 1

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / math_probability / repetition 1

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / math_proof / repetition 1

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.250`
**Scores:** `{'math_expert': 0.25, 'electrical_engineering_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / ee_mosfet / repetition 1

**Prompt:** Explain why a MOSFET gate driver must source and sink current quickly.

**Expected:** `['electrical_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / ee_filter / repetition 1

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / rlc_python / repetition 1

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['python_expert']`
**Confidence:** `0.333`
**Scores:** `{'python_expert': 0.3333333333333333, 'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## keyword / reasoning_schedule / repetition 1

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / reasoning_logic / repetition 1

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / general_capital / repetition 1

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## keyword / general_summary / repetition 1

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / irrelevant_python / repetition 1

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.333`
**Scores:** `{'python_expert': 0.3333333333333333, 'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## keyword / irrelevant_current / repetition 1

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / scientific_abstract / repetition 1

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / py_fastapi / repetition 2

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / py_paraphrase / repetition 2

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / math_integral / repetition 2

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / math_probability / repetition 2

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / math_proof / repetition 2

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.250`
**Scores:** `{'math_expert': 0.25, 'electrical_engineering_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / ee_mosfet / repetition 2

**Prompt:** Explain why a MOSFET gate driver must source and sink current quickly.

**Expected:** `['electrical_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / ee_filter / repetition 2

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / rlc_python / repetition 2

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['python_expert']`
**Confidence:** `0.333`
**Scores:** `{'python_expert': 0.3333333333333333, 'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## keyword / reasoning_schedule / repetition 2

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / reasoning_logic / repetition 2

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / general_capital / repetition 2

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## keyword / general_summary / repetition 2

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / irrelevant_python / repetition 2

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.333`
**Scores:** `{'python_expert': 0.3333333333333333, 'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## keyword / irrelevant_current / repetition 2

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / scientific_abstract / repetition 2

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / py_fastapi / repetition 3

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / py_paraphrase / repetition 3

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / math_integral / repetition 3

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / math_probability / repetition 3

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / math_proof / repetition 3

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.250`
**Scores:** `{'math_expert': 0.25, 'electrical_engineering_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / ee_mosfet / repetition 3

**Prompt:** Explain why a MOSFET gate driver must source and sink current quickly.

**Expected:** `['electrical_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / ee_filter / repetition 3

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / rlc_python / repetition 3

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['python_expert']`
**Confidence:** `0.333`
**Scores:** `{'python_expert': 0.3333333333333333, 'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## keyword / reasoning_schedule / repetition 3

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / reasoning_logic / repetition 3

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / general_capital / repetition 3

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## keyword / general_summary / repetition 3

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / irrelevant_python / repetition 3

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.333`
**Scores:** `{'python_expert': 0.3333333333333333, 'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## keyword / irrelevant_current / repetition 3

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / scientific_abstract / repetition 3

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / py_fastapi / repetition 4

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / py_paraphrase / repetition 4

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / math_integral / repetition 4

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / math_probability / repetition 4

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / math_proof / repetition 4

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.250`
**Scores:** `{'math_expert': 0.25, 'electrical_engineering_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / ee_mosfet / repetition 4

**Prompt:** Explain why a MOSFET gate driver must source and sink current quickly.

**Expected:** `['electrical_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / ee_filter / repetition 4

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / rlc_python / repetition 4

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['python_expert']`
**Confidence:** `0.333`
**Scores:** `{'python_expert': 0.3333333333333333, 'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## keyword / reasoning_schedule / repetition 4

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / reasoning_logic / repetition 4

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / general_capital / repetition 4

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## keyword / general_summary / repetition 4

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / irrelevant_python / repetition 4

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.333`
**Scores:** `{'python_expert': 0.3333333333333333, 'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## keyword / irrelevant_current / repetition 4

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## keyword / scientific_abstract / repetition 4

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.000`
**Scores:** `{'electrical_engineering_expert': 0.0, 'math_expert': 0.0, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / py_fastapi / repetition 0

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert', 'python_expert']`
**Confidence:** `0.221`
**Scores:** `{'software_engineering_expert': 0.22108743121425362, 'python_expert': 0.20544282455585694, 'scientific_writing_expert': 0.07010217197868432, 'electrical_engineering_expert': 0.04865666641587785, 'reasoning_expert': 0.03679900360969936, 'math_expert': 0.016329899513886338}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## embedding / py_paraphrase / repetition 0

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.099`
**Scores:** `{'reasoning_expert': 0.09880057193315663, 'scientific_writing_expert': 0.0926909548896622, 'math_expert': 0.09071098547707243, 'software_engineering_expert': 0.06551442577363069, 'electrical_engineering_expert': 0.041465381930757716, 'python_expert': 0.02631541603651035}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / math_integral / repetition 0

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.354`
**Scores:** `{'math_expert': 0.3535859889433672, 'software_engineering_expert': 0.10473949971155488, 'electrical_engineering_expert': 0.08689364217539193, 'python_expert': 0.07220403251730655, 'scientific_writing_expert': 0.06514781027053318, 'reasoning_expert': 0.05443954832654065}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## embedding / math_probability / repetition 0

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.239`
**Scores:** `{'math_expert': 0.23934864408297543, 'python_expert': 0.03728824548864505, 'software_engineering_expert': 0.03166908864097655, 'electrical_engineering_expert': 0.027285651519958803, 'reasoning_expert': 0.017149928542113276, 'scientific_writing_expert': 0.004961235736467761}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## embedding / math_proof / repetition 0

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.210`
**Scores:** `{'math_expert': 0.2103189005541128, 'python_expert': 0.04740349578609558, 'reasoning_expert': 0.024253964048604554, 'scientific_writing_expert': 0.003683065537213861, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / ee_filter / repetition 0

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.201`
**Scores:** `{'electrical_engineering_expert': 0.20124305173610013, 'software_engineering_expert': 0.008616833135038462, 'math_expert': 0.001604084827691705, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / rlc_python / repetition 0

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.472`
**Scores:** `{'electrical_engineering_expert': 0.47227588152585, 'python_expert': 0.3312078525235358, 'math_expert': 0.20073735684045307, 'scientific_writing_expert': 0.0737331993802376, 'reasoning_expert': 0.06138888888888889, 'software_engineering_expert': 0.006795077403759057}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## embedding / reasoning_schedule / repetition 0

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.329`
**Scores:** `{'reasoning_expert': 0.3287876723724231, 'scientific_writing_expert': 0.17844098606284528, 'electrical_engineering_expert': 0.13616097612602301, 'math_expert': 0.13290167235496772, 'software_engineering_expert': 0.10721561038099502, 'python_expert': 0.05388980419353213}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## embedding / reasoning_logic / repetition 0

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.161`
**Scores:** `{'reasoning_expert': 0.16051817866659096, 'software_engineering_expert': 0.0629379537757725, 'python_expert': 0.05567555049887776, 'electrical_engineering_expert': 0.05293186324056928, 'scientific_writing_expert': 0.01770737695664429, 'math_expert': 0.006300720123452086}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / general_capital / repetition 0

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.082`
**Scores:** `{'software_engineering_expert': 0.08188994341296398, 'python_expert': 0.051056575744335086, 'math_expert': 0.0469792656395143, 'scientific_writing_expert': 0.0054701674384415545, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## embedding / irrelevant_python / repetition 0

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.327`
**Scores:** `{'python_expert': 0.3269035340425982, 'software_engineering_expert': 0.1602356566661836, 'reasoning_expert': 0.08784741395074418, 'math_expert': 0.08694940923812301, 'electrical_engineering_expert': 0.06477893898051565, 'scientific_writing_expert': 0.01570464421837313}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## embedding / irrelevant_current / repetition 0

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.278`
**Scores:** `{'electrical_engineering_expert': 0.27803051135057655, 'math_expert': 0.14931484408859874, 'reasoning_expert': 0.10285826158275774, 'software_engineering_expert': 0.09647740869637009, 'scientific_writing_expert': 0.08381690974873192, 'python_expert': 0.03876522919760435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## embedding / scientific_abstract / repetition 0

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.460`
**Scores:** `{'scientific_writing_expert': 0.45993069328607755, 'software_engineering_expert': 0.173399467181427, 'electrical_engineering_expert': 0.1598963500110333, 'reasoning_expert': 0.1384934511988626, 'python_expert': 0.06917367006017436, 'math_expert': 0.012539739164266227}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## embedding / py_fastapi / repetition 1

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert', 'python_expert']`
**Confidence:** `0.221`
**Scores:** `{'software_engineering_expert': 0.22108743121425362, 'python_expert': 0.20544282455585694, 'scientific_writing_expert': 0.07010217197868432, 'electrical_engineering_expert': 0.04865666641587785, 'reasoning_expert': 0.03679900360969936, 'math_expert': 0.016329899513886338}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## embedding / py_paraphrase / repetition 1

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.099`
**Scores:** `{'reasoning_expert': 0.09880057193315663, 'scientific_writing_expert': 0.0926909548896622, 'math_expert': 0.09071098547707243, 'software_engineering_expert': 0.06551442577363069, 'electrical_engineering_expert': 0.041465381930757716, 'python_expert': 0.02631541603651035}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / math_integral / repetition 1

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.354`
**Scores:** `{'math_expert': 0.3535859889433672, 'software_engineering_expert': 0.10473949971155488, 'electrical_engineering_expert': 0.08689364217539193, 'python_expert': 0.07220403251730655, 'scientific_writing_expert': 0.06514781027053318, 'reasoning_expert': 0.05443954832654065}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## embedding / math_probability / repetition 1

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.239`
**Scores:** `{'math_expert': 0.23934864408297543, 'python_expert': 0.03728824548864505, 'software_engineering_expert': 0.03166908864097655, 'electrical_engineering_expert': 0.027285651519958803, 'reasoning_expert': 0.017149928542113276, 'scientific_writing_expert': 0.004961235736467761}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## embedding / math_proof / repetition 1

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.210`
**Scores:** `{'math_expert': 0.2103189005541128, 'python_expert': 0.04740349578609558, 'reasoning_expert': 0.024253964048604554, 'scientific_writing_expert': 0.003683065537213861, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / ee_filter / repetition 1

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.201`
**Scores:** `{'electrical_engineering_expert': 0.20124305173610013, 'software_engineering_expert': 0.008616833135038462, 'math_expert': 0.001604084827691705, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / rlc_python / repetition 1

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.472`
**Scores:** `{'electrical_engineering_expert': 0.47227588152585, 'python_expert': 0.3312078525235358, 'math_expert': 0.20073735684045307, 'scientific_writing_expert': 0.0737331993802376, 'reasoning_expert': 0.06138888888888889, 'software_engineering_expert': 0.006795077403759057}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## embedding / reasoning_schedule / repetition 1

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.329`
**Scores:** `{'reasoning_expert': 0.3287876723724231, 'scientific_writing_expert': 0.17844098606284528, 'electrical_engineering_expert': 0.13616097612602301, 'math_expert': 0.13290167235496772, 'software_engineering_expert': 0.10721561038099502, 'python_expert': 0.05388980419353213}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## embedding / reasoning_logic / repetition 1

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.161`
**Scores:** `{'reasoning_expert': 0.16051817866659096, 'software_engineering_expert': 0.0629379537757725, 'python_expert': 0.05567555049887776, 'electrical_engineering_expert': 0.05293186324056928, 'scientific_writing_expert': 0.01770737695664429, 'math_expert': 0.006300720123452086}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / general_capital / repetition 1

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.082`
**Scores:** `{'software_engineering_expert': 0.08188994341296398, 'python_expert': 0.051056575744335086, 'math_expert': 0.0469792656395143, 'scientific_writing_expert': 0.0054701674384415545, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## embedding / irrelevant_python / repetition 1

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.327`
**Scores:** `{'python_expert': 0.3269035340425982, 'software_engineering_expert': 0.1602356566661836, 'reasoning_expert': 0.08784741395074418, 'math_expert': 0.08694940923812301, 'electrical_engineering_expert': 0.06477893898051565, 'scientific_writing_expert': 0.01570464421837313}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## embedding / irrelevant_current / repetition 1

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.278`
**Scores:** `{'electrical_engineering_expert': 0.27803051135057655, 'math_expert': 0.14931484408859874, 'reasoning_expert': 0.10285826158275774, 'software_engineering_expert': 0.09647740869637009, 'scientific_writing_expert': 0.08381690974873192, 'python_expert': 0.03876522919760435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## embedding / scientific_abstract / repetition 1

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.460`
**Scores:** `{'scientific_writing_expert': 0.45993069328607755, 'software_engineering_expert': 0.173399467181427, 'electrical_engineering_expert': 0.1598963500110333, 'reasoning_expert': 0.1384934511988626, 'python_expert': 0.06917367006017436, 'math_expert': 0.012539739164266227}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## embedding / py_fastapi / repetition 2

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert', 'python_expert']`
**Confidence:** `0.221`
**Scores:** `{'software_engineering_expert': 0.22108743121425362, 'python_expert': 0.20544282455585694, 'scientific_writing_expert': 0.07010217197868432, 'electrical_engineering_expert': 0.04865666641587785, 'reasoning_expert': 0.03679900360969936, 'math_expert': 0.016329899513886338}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## embedding / py_paraphrase / repetition 2

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.099`
**Scores:** `{'reasoning_expert': 0.09880057193315663, 'scientific_writing_expert': 0.0926909548896622, 'math_expert': 0.09071098547707243, 'software_engineering_expert': 0.06551442577363069, 'electrical_engineering_expert': 0.041465381930757716, 'python_expert': 0.02631541603651035}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / math_integral / repetition 2

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.354`
**Scores:** `{'math_expert': 0.3535859889433672, 'software_engineering_expert': 0.10473949971155488, 'electrical_engineering_expert': 0.08689364217539193, 'python_expert': 0.07220403251730655, 'scientific_writing_expert': 0.06514781027053318, 'reasoning_expert': 0.05443954832654065}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## embedding / math_probability / repetition 2

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.239`
**Scores:** `{'math_expert': 0.23934864408297543, 'python_expert': 0.03728824548864505, 'software_engineering_expert': 0.03166908864097655, 'electrical_engineering_expert': 0.027285651519958803, 'reasoning_expert': 0.017149928542113276, 'scientific_writing_expert': 0.004961235736467761}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## embedding / math_proof / repetition 2

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.210`
**Scores:** `{'math_expert': 0.2103189005541128, 'python_expert': 0.04740349578609558, 'reasoning_expert': 0.024253964048604554, 'scientific_writing_expert': 0.003683065537213861, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / ee_filter / repetition 2

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.201`
**Scores:** `{'electrical_engineering_expert': 0.20124305173610013, 'software_engineering_expert': 0.008616833135038462, 'math_expert': 0.001604084827691705, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / rlc_python / repetition 2

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.472`
**Scores:** `{'electrical_engineering_expert': 0.47227588152585, 'python_expert': 0.3312078525235358, 'math_expert': 0.20073735684045307, 'scientific_writing_expert': 0.0737331993802376, 'reasoning_expert': 0.06138888888888889, 'software_engineering_expert': 0.006795077403759057}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## embedding / reasoning_schedule / repetition 2

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.329`
**Scores:** `{'reasoning_expert': 0.3287876723724231, 'scientific_writing_expert': 0.17844098606284528, 'electrical_engineering_expert': 0.13616097612602301, 'math_expert': 0.13290167235496772, 'software_engineering_expert': 0.10721561038099502, 'python_expert': 0.05388980419353213}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## embedding / reasoning_logic / repetition 2

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.161`
**Scores:** `{'reasoning_expert': 0.16051817866659096, 'software_engineering_expert': 0.0629379537757725, 'python_expert': 0.05567555049887776, 'electrical_engineering_expert': 0.05293186324056928, 'scientific_writing_expert': 0.01770737695664429, 'math_expert': 0.006300720123452086}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / general_capital / repetition 2

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.082`
**Scores:** `{'software_engineering_expert': 0.08188994341296398, 'python_expert': 0.051056575744335086, 'math_expert': 0.0469792656395143, 'scientific_writing_expert': 0.0054701674384415545, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## embedding / irrelevant_python / repetition 2

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.327`
**Scores:** `{'python_expert': 0.3269035340425982, 'software_engineering_expert': 0.1602356566661836, 'reasoning_expert': 0.08784741395074418, 'math_expert': 0.08694940923812301, 'electrical_engineering_expert': 0.06477893898051565, 'scientific_writing_expert': 0.01570464421837313}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## embedding / irrelevant_current / repetition 2

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.278`
**Scores:** `{'electrical_engineering_expert': 0.27803051135057655, 'math_expert': 0.14931484408859874, 'reasoning_expert': 0.10285826158275774, 'software_engineering_expert': 0.09647740869637009, 'scientific_writing_expert': 0.08381690974873192, 'python_expert': 0.03876522919760435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## embedding / scientific_abstract / repetition 2

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.460`
**Scores:** `{'scientific_writing_expert': 0.45993069328607755, 'software_engineering_expert': 0.173399467181427, 'electrical_engineering_expert': 0.1598963500110333, 'reasoning_expert': 0.1384934511988626, 'python_expert': 0.06917367006017436, 'math_expert': 0.012539739164266227}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## embedding / py_fastapi / repetition 3

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert', 'python_expert']`
**Confidence:** `0.221`
**Scores:** `{'software_engineering_expert': 0.22108743121425362, 'python_expert': 0.20544282455585694, 'scientific_writing_expert': 0.07010217197868432, 'electrical_engineering_expert': 0.04865666641587785, 'reasoning_expert': 0.03679900360969936, 'math_expert': 0.016329899513886338}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## embedding / py_paraphrase / repetition 3

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.099`
**Scores:** `{'reasoning_expert': 0.09880057193315663, 'scientific_writing_expert': 0.0926909548896622, 'math_expert': 0.09071098547707243, 'software_engineering_expert': 0.06551442577363069, 'electrical_engineering_expert': 0.041465381930757716, 'python_expert': 0.02631541603651035}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / math_integral / repetition 3

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.354`
**Scores:** `{'math_expert': 0.3535859889433672, 'software_engineering_expert': 0.10473949971155488, 'electrical_engineering_expert': 0.08689364217539193, 'python_expert': 0.07220403251730655, 'scientific_writing_expert': 0.06514781027053318, 'reasoning_expert': 0.05443954832654065}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## embedding / math_probability / repetition 3

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.239`
**Scores:** `{'math_expert': 0.23934864408297543, 'python_expert': 0.03728824548864505, 'software_engineering_expert': 0.03166908864097655, 'electrical_engineering_expert': 0.027285651519958803, 'reasoning_expert': 0.017149928542113276, 'scientific_writing_expert': 0.004961235736467761}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## embedding / math_proof / repetition 3

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.210`
**Scores:** `{'math_expert': 0.2103189005541128, 'python_expert': 0.04740349578609558, 'reasoning_expert': 0.024253964048604554, 'scientific_writing_expert': 0.003683065537213861, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / ee_filter / repetition 3

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.201`
**Scores:** `{'electrical_engineering_expert': 0.20124305173610013, 'software_engineering_expert': 0.008616833135038462, 'math_expert': 0.001604084827691705, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / rlc_python / repetition 3

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.472`
**Scores:** `{'electrical_engineering_expert': 0.47227588152585, 'python_expert': 0.3312078525235358, 'math_expert': 0.20073735684045307, 'scientific_writing_expert': 0.0737331993802376, 'reasoning_expert': 0.06138888888888889, 'software_engineering_expert': 0.006795077403759057}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## embedding / reasoning_schedule / repetition 3

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.329`
**Scores:** `{'reasoning_expert': 0.3287876723724231, 'scientific_writing_expert': 0.17844098606284528, 'electrical_engineering_expert': 0.13616097612602301, 'math_expert': 0.13290167235496772, 'software_engineering_expert': 0.10721561038099502, 'python_expert': 0.05388980419353213}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## embedding / reasoning_logic / repetition 3

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.161`
**Scores:** `{'reasoning_expert': 0.16051817866659096, 'software_engineering_expert': 0.0629379537757725, 'python_expert': 0.05567555049887776, 'electrical_engineering_expert': 0.05293186324056928, 'scientific_writing_expert': 0.01770737695664429, 'math_expert': 0.006300720123452086}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / general_capital / repetition 3

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.082`
**Scores:** `{'software_engineering_expert': 0.08188994341296398, 'python_expert': 0.051056575744335086, 'math_expert': 0.0469792656395143, 'scientific_writing_expert': 0.0054701674384415545, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## embedding / irrelevant_python / repetition 3

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.327`
**Scores:** `{'python_expert': 0.3269035340425982, 'software_engineering_expert': 0.1602356566661836, 'reasoning_expert': 0.08784741395074418, 'math_expert': 0.08694940923812301, 'electrical_engineering_expert': 0.06477893898051565, 'scientific_writing_expert': 0.01570464421837313}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## embedding / irrelevant_current / repetition 3

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.278`
**Scores:** `{'electrical_engineering_expert': 0.27803051135057655, 'math_expert': 0.14931484408859874, 'reasoning_expert': 0.10285826158275774, 'software_engineering_expert': 0.09647740869637009, 'scientific_writing_expert': 0.08381690974873192, 'python_expert': 0.03876522919760435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## embedding / scientific_abstract / repetition 3

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.460`
**Scores:** `{'scientific_writing_expert': 0.45993069328607755, 'software_engineering_expert': 0.173399467181427, 'electrical_engineering_expert': 0.1598963500110333, 'reasoning_expert': 0.1384934511988626, 'python_expert': 0.06917367006017436, 'math_expert': 0.012539739164266227}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## embedding / py_fastapi / repetition 4

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert', 'python_expert']`
**Confidence:** `0.221`
**Scores:** `{'software_engineering_expert': 0.22108743121425362, 'python_expert': 0.20544282455585694, 'scientific_writing_expert': 0.07010217197868432, 'electrical_engineering_expert': 0.04865666641587785, 'reasoning_expert': 0.03679900360969936, 'math_expert': 0.016329899513886338}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## embedding / py_paraphrase / repetition 4

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.099`
**Scores:** `{'reasoning_expert': 0.09880057193315663, 'scientific_writing_expert': 0.0926909548896622, 'math_expert': 0.09071098547707243, 'software_engineering_expert': 0.06551442577363069, 'electrical_engineering_expert': 0.041465381930757716, 'python_expert': 0.02631541603651035}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / math_integral / repetition 4

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.354`
**Scores:** `{'math_expert': 0.3535859889433672, 'software_engineering_expert': 0.10473949971155488, 'electrical_engineering_expert': 0.08689364217539193, 'python_expert': 0.07220403251730655, 'scientific_writing_expert': 0.06514781027053318, 'reasoning_expert': 0.05443954832654065}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## embedding / math_probability / repetition 4

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.239`
**Scores:** `{'math_expert': 0.23934864408297543, 'python_expert': 0.03728824548864505, 'software_engineering_expert': 0.03166908864097655, 'electrical_engineering_expert': 0.027285651519958803, 'reasoning_expert': 0.017149928542113276, 'scientific_writing_expert': 0.004961235736467761}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## embedding / math_proof / repetition 4

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.210`
**Scores:** `{'math_expert': 0.2103189005541128, 'python_expert': 0.04740349578609558, 'reasoning_expert': 0.024253964048604554, 'scientific_writing_expert': 0.003683065537213861, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / ee_filter / repetition 4

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.201`
**Scores:** `{'electrical_engineering_expert': 0.20124305173610013, 'software_engineering_expert': 0.008616833135038462, 'math_expert': 0.001604084827691705, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / rlc_python / repetition 4

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.472`
**Scores:** `{'electrical_engineering_expert': 0.47227588152585, 'python_expert': 0.3312078525235358, 'math_expert': 0.20073735684045307, 'scientific_writing_expert': 0.0737331993802376, 'reasoning_expert': 0.06138888888888889, 'software_engineering_expert': 0.006795077403759057}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## embedding / reasoning_schedule / repetition 4

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.329`
**Scores:** `{'reasoning_expert': 0.3287876723724231, 'scientific_writing_expert': 0.17844098606284528, 'electrical_engineering_expert': 0.13616097612602301, 'math_expert': 0.13290167235496772, 'software_engineering_expert': 0.10721561038099502, 'python_expert': 0.05388980419353213}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## embedding / reasoning_logic / repetition 4

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.161`
**Scores:** `{'reasoning_expert': 0.16051817866659096, 'software_engineering_expert': 0.0629379537757725, 'python_expert': 0.05567555049887776, 'electrical_engineering_expert': 0.05293186324056928, 'scientific_writing_expert': 0.01770737695664429, 'math_expert': 0.006300720123452086}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## embedding / general_capital / repetition 4

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.082`
**Scores:** `{'software_engineering_expert': 0.08188994341296398, 'python_expert': 0.051056575744335086, 'math_expert': 0.0469792656395143, 'scientific_writing_expert': 0.0054701674384415545, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## embedding / irrelevant_python / repetition 4

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.327`
**Scores:** `{'python_expert': 0.3269035340425982, 'software_engineering_expert': 0.1602356566661836, 'reasoning_expert': 0.08784741395074418, 'math_expert': 0.08694940923812301, 'electrical_engineering_expert': 0.06477893898051565, 'scientific_writing_expert': 0.01570464421837313}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## embedding / irrelevant_current / repetition 4

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.278`
**Scores:** `{'electrical_engineering_expert': 0.27803051135057655, 'math_expert': 0.14931484408859874, 'reasoning_expert': 0.10285826158275774, 'software_engineering_expert': 0.09647740869637009, 'scientific_writing_expert': 0.08381690974873192, 'python_expert': 0.03876522919760435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## embedding / scientific_abstract / repetition 4

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.460`
**Scores:** `{'scientific_writing_expert': 0.45993069328607755, 'software_engineering_expert': 0.173399467181427, 'electrical_engineering_expert': 0.1598963500110333, 'reasoning_expert': 0.1384934511988626, 'python_expert': 0.06917367006017436, 'math_expert': 0.012539739164266227}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / py_fastapi / repetition 0

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / py_paraphrase / repetition 0

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / math_integral / repetition 0

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / math_probability / repetition 0

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_top1 / math_proof / repetition 0

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / ee_filter / repetition 0

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / rlc_python / repetition 0

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / reasoning_schedule / repetition 0

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / reasoning_logic / repetition 0

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_top1 / general_capital / repetition 0

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_top1 / general_summary / repetition 0

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_top1 / irrelevant_python / repetition 0

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_top1 / irrelevant_current / repetition 0

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic_top1 / scientific_abstract / repetition 0

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / py_fastapi / repetition 1

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / py_paraphrase / repetition 1

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / math_integral / repetition 1

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / math_probability / repetition 1

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_top1 / math_proof / repetition 1

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / ee_filter / repetition 1

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / rlc_python / repetition 1

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / reasoning_schedule / repetition 1

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / reasoning_logic / repetition 1

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_top1 / general_capital / repetition 1

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_top1 / general_summary / repetition 1

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_top1 / irrelevant_python / repetition 1

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_top1 / irrelevant_current / repetition 1

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic_top1 / scientific_abstract / repetition 1

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / py_fastapi / repetition 2

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / py_paraphrase / repetition 2

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / math_integral / repetition 2

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / math_probability / repetition 2

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_top1 / math_proof / repetition 2

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / ee_filter / repetition 2

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / rlc_python / repetition 2

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / reasoning_schedule / repetition 2

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / reasoning_logic / repetition 2

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_top1 / general_capital / repetition 2

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_top1 / general_summary / repetition 2

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_top1 / irrelevant_python / repetition 2

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_top1 / irrelevant_current / repetition 2

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic_top1 / scientific_abstract / repetition 2

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / py_fastapi / repetition 3

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / py_paraphrase / repetition 3

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / math_integral / repetition 3

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / math_probability / repetition 3

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_top1 / math_proof / repetition 3

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / ee_filter / repetition 3

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / rlc_python / repetition 3

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / reasoning_schedule / repetition 3

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / reasoning_logic / repetition 3

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_top1 / general_capital / repetition 3

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_top1 / general_summary / repetition 3

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_top1 / irrelevant_python / repetition 3

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_top1 / irrelevant_current / repetition 3

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic_top1 / scientific_abstract / repetition 3

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / py_fastapi / repetition 4

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / py_paraphrase / repetition 4

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / math_integral / repetition 4

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / math_probability / repetition 4

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_top1 / math_proof / repetition 4

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / ee_filter / repetition 4

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / rlc_python / repetition 4

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_top1 / reasoning_schedule / repetition 4

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_top1 / reasoning_logic / repetition 4

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_top1 / general_capital / repetition 4

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_top1 / general_summary / repetition 4

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_top1 / irrelevant_python / repetition 4

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_top1 / irrelevant_current / repetition 4

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic_top1 / scientific_abstract / repetition 4

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic / py_fastapi / repetition 0

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert', 'python_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / py_paraphrase / repetition 0

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic / math_integral / repetition 0

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic / math_probability / repetition 0

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / math_proof / repetition 0

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic / ee_filter / repetition 0

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic / rlc_python / repetition 0

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## semantic / reasoning_schedule / repetition 0

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic / reasoning_logic / repetition 0

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / general_capital / repetition 0

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic / general_summary / repetition 0

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / irrelevant_python / repetition 0

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic / irrelevant_current / repetition 0

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic / scientific_abstract / repetition 0

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic / py_fastapi / repetition 1

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert', 'python_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / py_paraphrase / repetition 1

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic / math_integral / repetition 1

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic / math_probability / repetition 1

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / math_proof / repetition 1

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic / ee_filter / repetition 1

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic / rlc_python / repetition 1

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## semantic / reasoning_schedule / repetition 1

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic / reasoning_logic / repetition 1

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / general_capital / repetition 1

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic / general_summary / repetition 1

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / irrelevant_python / repetition 1

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic / irrelevant_current / repetition 1

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic / scientific_abstract / repetition 1

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic / py_fastapi / repetition 2

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert', 'python_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / py_paraphrase / repetition 2

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic / math_integral / repetition 2

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic / math_probability / repetition 2

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / math_proof / repetition 2

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic / ee_filter / repetition 2

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic / rlc_python / repetition 2

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## semantic / reasoning_schedule / repetition 2

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic / reasoning_logic / repetition 2

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / general_capital / repetition 2

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic / general_summary / repetition 2

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / irrelevant_python / repetition 2

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic / irrelevant_current / repetition 2

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic / scientific_abstract / repetition 2

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic / py_fastapi / repetition 3

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert', 'python_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / py_paraphrase / repetition 3

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic / math_integral / repetition 3

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic / math_probability / repetition 3

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / math_proof / repetition 3

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic / ee_filter / repetition 3

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic / rlc_python / repetition 3

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## semantic / reasoning_schedule / repetition 3

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic / reasoning_logic / repetition 3

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / general_capital / repetition 3

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic / general_summary / repetition 3

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / irrelevant_python / repetition 3

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic / irrelevant_current / repetition 3

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic / scientific_abstract / repetition 3

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic / py_fastapi / repetition 4

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert', 'python_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / py_paraphrase / repetition 4

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic / math_integral / repetition 4

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic / math_probability / repetition 4

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / math_proof / repetition 4

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic / ee_filter / repetition 4

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic / rlc_python / repetition 4

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## semantic / reasoning_schedule / repetition 4

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic / reasoning_logic / repetition 4

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / general_capital / repetition 4

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic / general_summary / repetition 4

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic / irrelevant_python / repetition 4

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic / irrelevant_current / repetition 4

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic / scientific_abstract / repetition 4

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / py_fastapi / repetition 0

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / py_paraphrase / repetition 0

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / math_integral / repetition 0

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / math_probability / repetition 0

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `[]`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / math_proof / repetition 0

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / ee_mosfet / repetition 0

**Prompt:** Explain why a MOSFET gate driver must source and sink current quickly.

**Expected:** `['electrical_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.395`
**Scores:** `{'electrical_engineering_expert': 0.3953015314915881, 'reasoning_expert': 0.15869591413843676, 'software_engineering_expert': 0.025684360764877057, 'scientific_writing_expert': 0.02126432550020091, 'python_expert': 0.011628889196009313, 'math_expert': 0.0019965979177571803}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / ee_filter / repetition 0

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `[]`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / rlc_python / repetition 0

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / reasoning_schedule / repetition 0

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / reasoning_logic / repetition 0

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / general_capital / repetition 0

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_threshold_high / general_summary / repetition 0

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `[]`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / irrelevant_python / repetition 0

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_threshold_high / irrelevant_current / repetition 0

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / scientific_abstract / repetition 0

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / py_fastapi / repetition 1

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / py_paraphrase / repetition 1

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / math_integral / repetition 1

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / math_probability / repetition 1

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `[]`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / math_proof / repetition 1

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / ee_mosfet / repetition 1

**Prompt:** Explain why a MOSFET gate driver must source and sink current quickly.

**Expected:** `['electrical_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.395`
**Scores:** `{'electrical_engineering_expert': 0.3953015314915881, 'reasoning_expert': 0.15869591413843676, 'software_engineering_expert': 0.025684360764877057, 'scientific_writing_expert': 0.02126432550020091, 'python_expert': 0.011628889196009313, 'math_expert': 0.0019965979177571803}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / ee_filter / repetition 1

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `[]`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / rlc_python / repetition 1

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / reasoning_schedule / repetition 1

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / reasoning_logic / repetition 1

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / general_capital / repetition 1

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_threshold_high / general_summary / repetition 1

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `[]`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / irrelevant_python / repetition 1

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_threshold_high / irrelevant_current / repetition 1

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / scientific_abstract / repetition 1

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / py_fastapi / repetition 2

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / py_paraphrase / repetition 2

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / math_integral / repetition 2

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / math_probability / repetition 2

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `[]`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / math_proof / repetition 2

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / ee_mosfet / repetition 2

**Prompt:** Explain why a MOSFET gate driver must source and sink current quickly.

**Expected:** `['electrical_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.395`
**Scores:** `{'electrical_engineering_expert': 0.3953015314915881, 'reasoning_expert': 0.15869591413843676, 'software_engineering_expert': 0.025684360764877057, 'scientific_writing_expert': 0.02126432550020091, 'python_expert': 0.011628889196009313, 'math_expert': 0.0019965979177571803}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / ee_filter / repetition 2

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `[]`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / rlc_python / repetition 2

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / reasoning_schedule / repetition 2

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / reasoning_logic / repetition 2

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / general_capital / repetition 2

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_threshold_high / general_summary / repetition 2

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `[]`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / irrelevant_python / repetition 2

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_threshold_high / irrelevant_current / repetition 2

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / scientific_abstract / repetition 2

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / py_fastapi / repetition 3

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / py_paraphrase / repetition 3

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / math_integral / repetition 3

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / math_probability / repetition 3

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `[]`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / math_proof / repetition 3

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / ee_mosfet / repetition 3

**Prompt:** Explain why a MOSFET gate driver must source and sink current quickly.

**Expected:** `['electrical_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.395`
**Scores:** `{'electrical_engineering_expert': 0.3953015314915881, 'reasoning_expert': 0.15869591413843676, 'software_engineering_expert': 0.025684360764877057, 'scientific_writing_expert': 0.02126432550020091, 'python_expert': 0.011628889196009313, 'math_expert': 0.0019965979177571803}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / ee_filter / repetition 3

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `[]`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / rlc_python / repetition 3

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / reasoning_schedule / repetition 3

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / reasoning_logic / repetition 3

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / general_capital / repetition 3

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_threshold_high / general_summary / repetition 3

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `[]`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / irrelevant_python / repetition 3

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_threshold_high / irrelevant_current / repetition 3

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / scientific_abstract / repetition 3

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / py_fastapi / repetition 4

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / py_paraphrase / repetition 4

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / math_integral / repetition 4

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / math_probability / repetition 4

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `[]`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / math_proof / repetition 4

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / ee_mosfet / repetition 4

**Prompt:** Explain why a MOSFET gate driver must source and sink current quickly.

**Expected:** `['electrical_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.395`
**Scores:** `{'electrical_engineering_expert': 0.3953015314915881, 'reasoning_expert': 0.15869591413843676, 'software_engineering_expert': 0.025684360764877057, 'scientific_writing_expert': 0.02126432550020091, 'python_expert': 0.011628889196009313, 'math_expert': 0.0019965979177571803}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / ee_filter / repetition 4

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `[]`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / rlc_python / repetition 4

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_threshold_high / reasoning_schedule / repetition 4

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `[]`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / reasoning_logic / repetition 4

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / general_capital / repetition 4

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_threshold_high / general_summary / repetition 4

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `[]`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / irrelevant_python / repetition 4

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_threshold_high / irrelevant_current / repetition 4

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_threshold_high / scientific_abstract / repetition 4

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache / py_fastapi / repetition 0

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert', 'python_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / py_paraphrase / repetition 0

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache / math_integral / repetition 0

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache / math_probability / repetition 0

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / math_proof / repetition 0

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache / ee_filter / repetition 0

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache / rlc_python / repetition 0

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## semantic_cache / reasoning_schedule / repetition 0

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache / reasoning_logic / repetition 0

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / general_capital / repetition 0

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_cache / general_summary / repetition 0

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / irrelevant_python / repetition 0

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_cache / irrelevant_current / repetition 0

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic_cache / scientific_abstract / repetition 0

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache / py_fastapi / repetition 1

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert', 'python_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / py_paraphrase / repetition 1

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache / math_integral / repetition 1

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache / math_probability / repetition 1

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / math_proof / repetition 1

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache / ee_filter / repetition 1

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache / rlc_python / repetition 1

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## semantic_cache / reasoning_schedule / repetition 1

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache / reasoning_logic / repetition 1

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / general_capital / repetition 1

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_cache / general_summary / repetition 1

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / irrelevant_python / repetition 1

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_cache / irrelevant_current / repetition 1

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic_cache / scientific_abstract / repetition 1

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache / py_fastapi / repetition 2

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert', 'python_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / py_paraphrase / repetition 2

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache / math_integral / repetition 2

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache / math_probability / repetition 2

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / math_proof / repetition 2

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache / ee_filter / repetition 2

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache / rlc_python / repetition 2

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## semantic_cache / reasoning_schedule / repetition 2

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache / reasoning_logic / repetition 2

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / general_capital / repetition 2

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_cache / general_summary / repetition 2

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / irrelevant_python / repetition 2

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_cache / irrelevant_current / repetition 2

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic_cache / scientific_abstract / repetition 2

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache / py_fastapi / repetition 3

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert', 'python_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / py_paraphrase / repetition 3

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache / math_integral / repetition 3

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache / math_probability / repetition 3

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / math_proof / repetition 3

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache / ee_filter / repetition 3

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache / rlc_python / repetition 3

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## semantic_cache / reasoning_schedule / repetition 3

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache / reasoning_logic / repetition 3

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / general_capital / repetition 3

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_cache / general_summary / repetition 3

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / irrelevant_python / repetition 3

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_cache / irrelevant_current / repetition 3

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic_cache / scientific_abstract / repetition 3

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache / py_fastapi / repetition 4

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert', 'python_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / py_paraphrase / repetition 4

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache / math_integral / repetition 4

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache / math_probability / repetition 4

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / math_proof / repetition 4

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache / ee_filter / repetition 4

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache / rlc_python / repetition 4

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert', 'python_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.783` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## semantic_cache / reasoning_schedule / repetition 4

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache / reasoning_logic / repetition 4

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / general_capital / repetition 4

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_cache / general_summary / repetition 4

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache / irrelevant_python / repetition 4

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_cache / irrelevant_current / repetition 4

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic_cache / scientific_abstract / repetition 4

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache_small / py_fastapi / repetition 0

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget, low confidence

## semantic_cache_small / py_paraphrase / repetition 0

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache_small / math_integral / repetition 0

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache_small / math_probability / repetition 0

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache_small / math_proof / repetition 0

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache_small / ee_filter / repetition 0

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache_small / rlc_python / repetition 0

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## semantic_cache_small / reasoning_schedule / repetition 0

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache_small / reasoning_logic / repetition 0

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache_small / general_capital / repetition 0

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_cache_small / general_summary / repetition 0

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache_small / irrelevant_python / repetition 0

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_cache_small / irrelevant_current / repetition 0

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic_cache_small / scientific_abstract / repetition 0

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache_small / py_fastapi / repetition 1

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget, low confidence

## semantic_cache_small / py_paraphrase / repetition 1

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache_small / math_integral / repetition 1

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache_small / math_probability / repetition 1

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache_small / math_proof / repetition 1

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache_small / ee_filter / repetition 1

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache_small / rlc_python / repetition 1

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## semantic_cache_small / reasoning_schedule / repetition 1

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache_small / reasoning_logic / repetition 1

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache_small / general_capital / repetition 1

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_cache_small / general_summary / repetition 1

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache_small / irrelevant_python / repetition 1

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_cache_small / irrelevant_current / repetition 1

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic_cache_small / scientific_abstract / repetition 1

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache_small / py_fastapi / repetition 2

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget, low confidence

## semantic_cache_small / py_paraphrase / repetition 2

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache_small / math_integral / repetition 2

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache_small / math_probability / repetition 2

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache_small / math_proof / repetition 2

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache_small / ee_filter / repetition 2

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache_small / rlc_python / repetition 2

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## semantic_cache_small / reasoning_schedule / repetition 2

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache_small / reasoning_logic / repetition 2

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache_small / general_capital / repetition 2

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_cache_small / general_summary / repetition 2

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache_small / irrelevant_python / repetition 2

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_cache_small / irrelevant_current / repetition 2

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic_cache_small / scientific_abstract / repetition 2

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache_small / py_fastapi / repetition 3

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget, low confidence

## semantic_cache_small / py_paraphrase / repetition 3

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache_small / math_integral / repetition 3

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache_small / math_probability / repetition 3

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache_small / math_proof / repetition 3

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache_small / ee_filter / repetition 3

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache_small / rlc_python / repetition 3

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## semantic_cache_small / reasoning_schedule / repetition 3

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache_small / reasoning_logic / repetition 3

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache_small / general_capital / repetition 3

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_cache_small / general_summary / repetition 3

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache_small / irrelevant_python / repetition 3

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_cache_small / irrelevant_current / repetition 3

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic_cache_small / scientific_abstract / repetition 3

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache_small / py_fastapi / repetition 4

**Prompt:** Write a FastAPI endpoint with input validation and a unit test.

**Expected:** `['python_expert', 'software_engineering_expert']`
**Selected:** `['software_engineering_expert']`
**Confidence:** `0.227`
**Scores:** `{'software_engineering_expert': 0.22739204050664935, 'python_expert': 0.2133046793848109, 'scientific_writing_expert': 0.04556641178614481, 'electrical_engineering_expert': 0.037541188902740136, 'reasoning_expert': 0.023919352346304584, 'math_expert': 0.014350758272811485}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget, low confidence

## semantic_cache_small / py_paraphrase / repetition 4

**Prompt:** Show an idiomatic generator that lazily walks a tree, including edge-case checks.

**Expected:** `['python_expert', 'reasoning_expert']`
**Selected:** `[]`
**Confidence:** `0.070`
**Scores:** `{'math_expert': 0.07002356908202076, 'reasoning_expert': 0.06746960253833847, 'scientific_writing_expert': 0.062129035201661256, 'software_engineering_expert': 0.05259664418744585, 'electrical_engineering_expert': 0.028491796494959913, 'python_expert': 0.02206083996236598}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache_small / math_integral / repetition 4

**Prompt:** Calculate the integral of x squared from zero to three and explain each step.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.382`
**Scores:** `{'math_expert': 0.3822169680305278, 'software_engineering_expert': 0.07003190616919389, 'electrical_engineering_expert': 0.05648086741400476, 'scientific_writing_expert': 0.04875747083034059, 'python_expert': 0.046932621136249256, 'reasoning_expert': 0.03538570641225142}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache_small / math_probability / repetition 4

**Prompt:** Two fair dice are rolled. Compute the probability that their sum is eight.

**Expected:** `['math_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.241`
**Scores:** `{'math_expert': 0.2411072147569235, 'python_expert': 0.03135506312196252, 'software_engineering_expert': 0.022598098196535434, 'reasoning_expert': 0.020947412719295504, 'electrical_engineering_expert': 0.01773567348797322, 'scientific_writing_expert': 0.0060597950781141946}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache_small / math_proof / repetition 4

**Prompt:** Give a concise proof that the square root of two is irrational.

**Expected:** `['math_expert', 'reasoning_expert']`
**Selected:** `['math_expert']`
**Confidence:** `0.304`
**Scores:** `{'math_expert': 0.30444855487082423, 'python_expert': 0.03081227226096213, 'reasoning_expert': 0.024859053866055796, 'scientific_writing_expert': 0.00449860147759693, 'electrical_engineering_expert': 0.0, 'software_engineering_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert

## semantic_cache_small / ee_filter / repetition 4

**Prompt:** Derive the cutoff frequency of a first-order RC low-pass circuit.

**Expected:** `['electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.212`
**Scores:** `{'electrical_engineering_expert': 0.2123902615672348, 'software_engineering_expert': 0.005600941537775001, 'math_expert': 0.0019592750395377254, 'python_expert': 0.0, 'reasoning_expert': 0.0, 'scientific_writing_expert': 0.0}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache_small / rlc_python / repetition 4

**Prompt:** Use Python to simulate an RLC circuit and plot the transient response.

**Expected:** `['python_expert', 'electrical_engineering_expert', 'math_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.461`
**Scores:** `{'electrical_engineering_expert': 0.46085780322363085, 'python_expert': 0.40587505495575227, 'math_expert': 0.22047928194629451, 'scientific_writing_expert': 0.05703980336581212, 'reasoning_expert': 0.03990277777777778, 'software_engineering_expert': 0.008299701686019992}`
**Quality:** `0.567` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, relevant expert rejected by memory budget

## semantic_cache_small / reasoning_schedule / repetition 4

**Prompt:** Analyze two competing project schedules and identify the critical dependency.

**Expected:** `['reasoning_expert', 'software_engineering_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.295`
**Scores:** `{'reasoning_expert': 0.2951367476775854, 'scientific_writing_expert': 0.11698694720393661, 'math_expert': 0.09181914071067335, 'electrical_engineering_expert': 0.08850463448191496, 'software_engineering_expert': 0.07501769419619161, 'python_expert': 0.035781801711387715}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, low confidence

## semantic_cache_small / reasoning_logic / repetition 4

**Prompt:** Deduce which statement must be true when exactly one of three claims is false.

**Expected:** `['reasoning_expert']`
**Selected:** `['reasoning_expert']`
**Confidence:** `0.185`
**Scores:** `{'reasoning_expert': 0.1848042175417016, 'electrical_engineering_expert': 0.04824666373604729, 'python_expert': 0.04667413989078791, 'software_engineering_expert': 0.04302796631859294, 'scientific_writing_expert': 0.01648146618193123, 'math_expert': 0.007695879579359334}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache_small / general_capital / repetition 4

**Prompt:** What is the capital of Japan?

**Expected:** `[]`
**Selected:** `[]`
**Confidence:** `0.058`
**Scores:** `{'software_engineering_expert': 0.05822280390704877, 'math_expert': 0.036195687249865396, 'python_expert': 0.0355411290128049, 'scientific_writing_expert': 0.0066814187998107556, 'electrical_engineering_expert': 0.0, 'reasoning_expert': 0.0}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence, correct routing did not improve output quality

## semantic_cache_small / general_summary / repetition 4

**Prompt:** Summarize why reproducibility matters in scientific experiments.

**Expected:** `['scientific_writing_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.291`
**Scores:** `{'scientific_writing_expert': 0.2912130938625435, 'reasoning_expert': 0.1575889993626587, 'math_expert': 0.0738420392484285, 'electrical_engineering_expert': 0.026206036830279656, 'software_engineering_expert': 0.005105943459448609, 'python_expert': 0.00326043074667231}`
**Quality:** `1.000` (`synthetic_capability_coverage_v1`)
**Possible reason:** low confidence

## semantic_cache_small / irrelevant_python / repetition 4

**Prompt:** Name one Python species found in Southeast Asia.

**Expected:** `[]`
**Selected:** `['python_expert']`
**Confidence:** `0.408`
**Scores:** `{'python_expert': 0.40767249118274296, 'software_engineering_expert': 0.12207638131049096, 'math_expert': 0.06362528695630429, 'reasoning_expert': 0.05903966152889281, 'electrical_engineering_expert': 0.042106310337335175, 'scientific_writing_expert': 0.019182101152441462}`
**Quality:** `0.950` (`synthetic_capability_coverage_v1`)
**Possible reason:** unnecessary expert activation

## semantic_cache_small / irrelevant_current / repetition 4

**Prompt:** Explain the current state of a historical debate without discussing electricity.

**Expected:** `['reasoning_expert']`
**Selected:** `['electrical_engineering_expert']`
**Confidence:** `0.248`
**Scores:** `{'electrical_engineering_expert': 0.24799279394030654, 'math_expert': 0.11464462354372378, 'reasoning_expert': 0.07325505066839598, 'software_engineering_expert': 0.07059529369114668, 'scientific_writing_expert': 0.05448099133667575, 'python_expert': 0.03146986059904435}`
**Quality:** `0.350` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert, unnecessary expert activation, low confidence

## semantic_cache_small / scientific_abstract / repetition 4

**Prompt:** Draft a scientific abstract describing a controlled routing experiment and its limitations.

**Expected:** `['scientific_writing_expert', 'reasoning_expert']`
**Selected:** `['scientific_writing_expert']`
**Confidence:** `0.439`
**Scores:** `{'scientific_writing_expert': 0.43864604518094996, 'software_engineering_expert': 0.12397088099153367, 'electrical_engineering_expert': 0.10393262750717165, 'reasoning_expert': 0.0953502945625847, 'python_expert': 0.054252924111619284, 'math_expert': 0.008150830456773048}`
**Quality:** `0.675` (`synthetic_capability_coverage_v1`)
**Possible reason:** missing required expert
