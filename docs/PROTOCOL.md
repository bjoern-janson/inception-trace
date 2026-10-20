# Protocol v0.1 — From saved replies to testable claims

**Research state:** design only. Corpus not yet ingested. These hypotheses and procedures are prospective; retrospective cherry-picking cannot be disguised as a preregistration.

## Questions

**RQ1 — Substance.** Which statements in the archived dialogue constitute valid deductions, mathematical repairs, meaningful connections across established fields, or empirically productive research proposals?

**RQ2 — Process.** Does the quality or frequency of defensible connections change over the interaction's timeline, and what aspects of prompt/context/scaffolding might explain the change?

**RQ3 — Transfer.** Can a frozen model perform better on independent held-out tasks when supplied with a version of the accumulated research framing, compared with matched baselines?

**RQ4 — External changes.** How do independently sourced model/deployment changes line up temporally, and what can be inferred without internal training/deployment data? RQ4 does not authorize attributing a global update to this corpus.

## Nulls and alternatives

| Hypothesis | Distinguishing evidence | Main confounds |
| --- | --- | --- |
| `H0_selection` Saved replies exaggerate quality or change because unusual outputs were selected | Complete denominator of responses or probability sample; blinded review | Saved-only archive, missing failures |
| `H1_context` Increasingly informative prompts/context elicit better results from a fixed model | Frozen model, matched prompts, random assignment, comparable token budgets | Prompt engineering, leakage, context size |
| `H2_workflow` Human–AI correction and external artifacts improve cumulative research throughput | Provenance-linked correction sequence; independent outcomes; baseline workflow | Human expertise, tools, retrieval, model routing |
| `H3_deployment` External model or platform changes caused discontinuities | Authenticated version/routing logs, independent simultaneous controls | Release timing, availability by tier/region |
| `H4_global_influence` The conversations caused improvements in a shared deployed model | Access to training/deployment lineage and a causal test establishing influence | Timing alone; ordinary interaction has no shared-weight update pathway |

`H4_global_influence` is *not testable using the saved replies alone*. Do not imply otherwise.

## Phase 0 — Freeze corpus and scope

Before selecting showcase results: inventory every supplied file, compute immutable byte hashes, record exact duplicates, unknown dates, missing prompts, and possible multiple replies per file. Preserve an initial inventory snapshot privately. If the originals cover only **saved interesting replies**, document the selection mechanism as unknown. Divide cases into **historically pre-exposed examples** (including the previously discussed metric-entropy / Causal Twins reply) and cases first seen during this project.

## Phase 1 — Reconstruct without interpretation

Use chronological anchors only where independent evidence is available. Keep at least these separate: platform message timestamps, timestamps in the body, Notepad filename hints, filesystem mtime, repository creation, commit time, model announcement, actual model access. Cross-link to GitHub only by substantive content/provenance, never by temporal proximity alone. Record model/version as `unknown` until supplied by contemporaneous evidence.

Segment a file into individual assistant replies **only when delimiters are independently justified**. Preserve byte offsets and parser version for each segment, including ambiguities. Do not hallucinate user prompts.

## Phase 2 — Find and adjudicate connections

Candidate mining uses two lanes:

1. **Coverage lane:** sample across the entire archive/time strata before scoring, so not only dramatic examples are reviewed. Treat conclusions as descriptive of the sampled *saved corpus*, not all interactions.
2. **High-signal lane:** separately study proposed lemmas, unexpected cross-domain bridges, self-corrections, falsifiable predictions, and abrupt conceptual shifts. Explicitly flag the lane as selected for interest.

Each case documents original exact source offsets, available preceding prompts, likely prior-art fields, reconstructed formal statement, assumptions, a counterexample search, independent proof or executable test, and a verdict. When originality is alleged, record **publication dates of relevant prior art**, not merely similarities. Two reviewers blinded to output ordering/model where feasible should separately score validity and novelty; reconcile disagreements with cited evidence, not prestige or enthusiastic prose.

Working rubric (each axis recorded separately, not added into a single unvalidated intelligence score):

- `correctness`: incorrect / incomplete / valid only under declared assumptions / verified scoped
- `contribution`: restatement / useful synthesis / correct repair / testable new conjecture / independently established novelty
- `independence`: supplied in prior prompt / suggested by the reply / origin unknown
- `actionability`: vague / checkable / implemented / independently replicated
- `self_correction`: none / acknowledges issue / repairs with proof / repairs and independently tests

## Phase 3 — Controlled elicitation comparisons

Only after selecting a small set of held-out tasks, freeze the protocol:

- Hold model identifier, checkpoint or deployment snapshot, tool access, sampling parameters and computational budgets constant wherever possible.
- Compare the same tasks under (A) minimal baseline, (B) original cumulative framing, and (C) equal-length control context (shuffled/irrelevant/neutral, designed to preserve task information fairness).
- Counterbalance order; separate fresh sessions and reset any tool, cache, project memory, or persistent state that could leak treatment information. Distinguish fresh browser window from fresh backend state.
- Use blind grading and independent mathematical checks; report total trials, failures, timeout rates and uncertainty rather than selected successes.
- Additional cross-version comparisons are a **separate** experiment because model drift is a confound, not an interchangeable treatment.

An increase in performance under B would support *elicitation under the tested conditions*, not self-modification or global learning.

## Phase 4 — Chronology against model releases

Collect authenticated primary release notes and separately establish which model/account tier was actually used on each date. Date coincidences are hypothesis generators, not mechanisms. A model-release date, company incident, or temporary account access restriction must not be used to impute model identity or internal state in a conversation.

## Reporting

Every public conclusion should include: exact source IDs, sampling lane, numerator/denominator where meaningful, uncertainty, independent checks, counterexamples attempted, competitor explanations, and its **claim ceiling**. Never promote prior hypotheses solely because later documents repeat them. Zero or negative findings are preserved as valuable constraints.
