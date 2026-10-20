# Evidence and scientific standing

## Precedence

1. **Original byte-preserved files** (source hashes and verifiable custody), plus original prompts and platform exports where available.
2. **Independently dated records** (GitHub API creation time, verified commits, primary model release documentation, contemporaneous runtime/account notices).
3. **Reproducible mathematical / computational evidence** (derivations, counterexamples, tests, held-out controls and logs).
4. **Review interpretations** (claims, annotations, cross-links, syntheses), all explicitly revocable.
5. **Retrospective recollection or unsourced timestamps**, useful for leads but not conclusive dating.

A GitHub repo's creation time is not an idea's birth. An assistant's statement that a theorem is proved is not the proof. An unusual-activity access notice is not evidence of model-weight changes. An apparently original idea is not scientific novelty without relevant prior-art evaluation.

## Standing of claims

Use the narrowest defensible classification:

| Status | Meaning |
| --- | --- |
| `unreviewed` | Located in the corpus; not evaluated |
| `candidate` | Specific claim extracted with its source and missing information noted |
| `reconstructed` | Argument / experiment independently reconstructed, but not necessarily correct |
| `supported_scoped` | Correctness supported for a declared model, data set, or assumption class |
| `partially_supported` | A scoped part survives, but the full claim does not |
| `unsupported` | Insufficient evidence for asserted claim |
| `refuted` | Counterexample, contradictory data, or invalid derivation defeats the claim |
| `contaminated` | Independence, leakage, or benchmark validity prevents claimed inference |
| `unresolved` | Not enough evidence to adjudicate |

Preserve old assessments and record a superseding case/version; never silently relabel the original assistant response.

## Attribution

The corpus may consist of **assistant replies selected for saving**, with user prompts absent. Therefore:

- A claim appearing first in an archived assistant reply does not establish the model originated it.
- A reply reacting to a mathematical definition cannot be credited with inventing the definition without the preceding prompt.
- A mathematical repair may be useful despite drawing entirely from established literature.
- Repeated enthusiasm, unusual vocabulary, elaborate notation, or confident self-assessments are not independent corroboration.
- Model identities and subscription tiers need original evidence; generic style is insufficient.

## Chronology

Store each date with `time_basis` and `source_reference` and keep `observed_at`, `published_at`, `event_at`, and `file_mtime` distinct where applicable. Use UTC with explicit offsets. Do not repair gaps by interpolating GitHub dates across missing conversations.

## Privacy and consent

Saved conversations can contain sensitive details about the user or third parties. No raw archive, user account identifiers, incident reports, access tokens, contact information, or excerpts are published by default. The user controls whether and how to publish reviewed text. Public findings should quote only the minimum necessary, with source permission/redaction and a traceable **private** source hash. The original public Git history may be permanent, so review before committing.

## Explicit non-claims at foundation

- No proof of user-induced global model updates.
- No proof of persistent model learning across unrelated accounts or sessions.
- No determination that the conversation corpus contains a novel theorem or discovery.
- No verification of remembered account restrictions as capability-related.
- No scientific performance trend inferred from a handpicked corpus before selection bias and exposure confounds are addressed.
