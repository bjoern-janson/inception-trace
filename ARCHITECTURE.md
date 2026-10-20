# Architecture and invariants

## Purpose

Inception Trace is a **forensic research corpus**, not an agentic self-improvement system. It reconstructs a human–AI research history while keeping source evidence separate from interpretation, causal hypotheses, and scientific standing.

## Units of analysis

1. **Source file.** Byte-preserved local artifact. One file may contain zero, one, or several replies. A file is not automatically a message, a prompt-response pair, or a dated event.
2. **Message / turn.** A unit derived only when explicit delimiters or trustworthy supplemental data support segmentation. Such units must reference offsets into a source file; do not infer missing user prompts.
3. **Candidate connection.** A scoped assertion, correction, lemma, test, or synthesis that appears in one or more sources. Not synonymous with a valid finding.
4. **Case assessment.** Reviewed evidence for one claim, including earlier prompt exposure, prior art, proof/experiment, alternatives, and nulls.
5. **Chronology anchor.** External event with its own source, clock, and provenance. Its proximity to a conversation is not causal attribution.

## Source identifiers

- `source_id = "sha256:" + SHA256(original file bytes)`. This persists through renames and detects exact duplicates.
- `record_id = "file-" + first 20 hex digits of SHA256(UTF-8 relative path)`. This distinguishes two separate file locations, even if their content is identical; it changes on rename.
- `duplicate_of` points to the first record by deterministic path sorting with identical bytes; duplicate source records are preserved, never dropped.
- Later message IDs must include `source_id` and byte offsets (plus a parser version). Never construct them from paraphrased content.

## Temporal custody

Four distinct time concepts must not be substituted for one another:

- **Conversation time:** authenticated platform event time, if available.
- **Content reference time:** date mentioned in the conversation; may not be the date the conversation occurred.
- **File metadata time:** local `mtime` observed at ingestion; copying/extracting can change it.
- **Filename date hint:** syntactic interpretation of a filename, never authoritative by itself.

Repository `created_at`, commit author/committer time, and model-release announcement time are three *additional* clocks. Keep their sources explicit. Unknown means unknown.

## Data flow

```text
original files (raw/, immutable by policy)
            |
            v
byte inventory --> SHA-256 integrity verification
            |
            v
local manifest (derived/) --> local counts, deduplication, date hints
            |
            v
human-verified chronology + source-linked message segmentation [not implemented]
            |
            v
candidate connection ledger --> claim review / prior art / proof / replication [not implemented]
            |
            v
controlled comparison of elicitation hypotheses [not implemented]
```

Only **the first two stages and summary counts** are implemented. All others require the actual files, provenance decisions, and further testing. No inference model or API is invoked by the current tool.

## Privacy boundary

The source corpus, path-bearing manifests, annotations, and working results default to ignored local directories. Public material (templates, synthetic tests, reviewed claim summaries and independently attributable public anchors) may be committed separately after human review. No automatic promotion from `derived/` to public documentation.

## Extension constraints

- Ingestion must be additive and non-destructive; do not alter or normalize source bytes.
- Importers must emit uncertainty and parser version for inferred segmentation.
- No model label, user text, missing prompt, or exact date is filled in from contextual plausibility.
- Provenance is not evidence of scientific truth; a mathematically valid connection is not automatically novel.
- Later assessments supersede earlier interpretations **without deleting** their historical status.
- Large future corpora may use a local database, but retain stable source hashes and exportable text/JSONL.
