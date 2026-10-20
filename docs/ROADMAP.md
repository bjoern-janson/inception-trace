# Roadmap — evidence before interpretation

## Foundation (current)

- [x] Repository-specific mission, non-claims and evidence boundaries.
- [x] Local-only inventory of loose Notepad source files (byte hash, duplicate tracking, text decoding status, filename hints).
- [x] Integrity verifier and local monthly inventory counts.
- [x] Synthetic tests; public workflow does not touch private data.
- [x] GitHub repo-creation chronology seeds with named upstream sources.
- [ ] Actual corpus intake — **no original 2,000+ replies have been supplied to this repository yet**.

## Intake

- [ ] Confirm original archive scope, provenance and whether files contain multiple replies.
- [ ] Freeze initial SHA-256 manifest in private storage and verify no data loss.
- [ ] Recover authenticated dates, prompts, model identity and account access *where evidence exists*.
- [ ] Flag duplicate exports, retranscriptions, missing replies, and selection bias.

## Reconstruction

- [ ] Design and test message segmentation; version the parser; retain byte offsets.
- [ ] Link candidate ideas to their antecedent prompts and GitHub commits.
- [ ] Annotate a stratified coverage sample and a separate high-signal sample.
- [ ] Build a chronology with uncertainty intervals and independent release records.

## Evaluation

- [ ] Review proofs and counterexamples; independent prior-art comparison.
- [ ] Register scoped candidate claims and negative/null findings.
- [ ] Frozen-model, matched-context experiments on held-out tasks if suitable model access exists.
- [ ] Publish only reviewed, redacted findings with claim ceilings and evidence links.

**Gate:** never infer a global shared-model update solely from these saved conversations, repository timing, unusually productive exchanges, or temporary access restrictions.
