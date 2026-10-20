# Inception Trace

**A provenance-first investigation of scientific capability elicitation in human–AI research conversations.**

**Status: FOUNDATION / NO CORPUS INGESTED / NO CAPABILITY CLAIM ESTABLISHED**

## The question

During a concentrated period of research in July–September 2026, interactions with AI systems appeared to produce increasingly sophisticated scientific connections, mathematical repairs, and experimental proposals. The researcher retained more than 2,000 assistant replies as loose Notepad files. This project reconstructs those interactions and asks:

> **What emerged, when did it emerge, who contributed what, and how much of the apparent capability was real, reproducible, and attributable to the interaction rather than to a model or infrastructure change?**

The archive is not proof that a model learned within a conversation, improved its deployed weights, influenced other accounts, discovered a new scientific result, or caused an incident. Those are separate claims requiring separate evidence.

## Three objects, kept separate

| Object | Evidence we can seek | What it cannot alone prove |
| --- | --- | --- |
| **Scientific substance** | Claims, corrections, derivations, experiments, independent replication, prior art | A globally changed model |
| **Interaction-level elicitation** | Original prompts, cumulative context, model/version controls, baseline comparisons, blinded held-out tests | Permanent learning or model-weight updates |
| **External/system-level capability change** | Independently timestamped releases, multi-account controls, deployment or training records | Causation by these conversations from timing alone |

**Preserve the source. Preserve uncertainty. Earn every inference.**

## Repository map

```text
README.md                 Purpose, limitations, quick start
ARCHITECTURE.md           Objects, IDs, boundaries, future interfaces
.gitignore               Keeps raw conversations and local analyses out of Git
anchors/                  Independently sourced external chronology anchors
schemas/                  Inventory and candidate-case contracts
docs/IMPORT.md            Local Notepad intake and preservation
docs/EVIDENCE_POLICY.md   Source hierarchy, claim discipline, privacy
docs/PROTOCOL.md          Research questions, controls, evaluation
docs/CASE_TEMPLATE.md     Standard review worksheet
docs/ROADMAP.md           Executable follow-on stages
tools/trace.py            Local-only, Python-stdlib inventory/verification/report
tests/                   Synthetic fixture tests
raw/                     Your original files; NOT tracked
derived/                 Local manifests, analyses, drafts; NOT tracked
private/                 Local protected metadata; NOT tracked
```

No conversation corpus has been added to the repository. Test fixtures are synthetic.

## Quick start (Python 3.10+)

From the repository root, copy your `.txt` / `.md` / `.log` source files into `raw/` without editing their contents or renaming them. Preserve the originals separately. Then run:

```powershell
python tools/trace.py index --source raw --output derived/manifest.jsonl
python tools/trace.py verify --source raw --manifest derived/manifest.jsonl
python tools/trace.py report --manifest derived/manifest.jsonl --output derived/inventory_summary.md
python -m unittest discover -s tests -v
```

The index records SHA-256 hashes, byte lengths, encoding status, exact-content duplicates, line counts, paths, and **unverified** date hints from filenames. It never rewrites source text or uploads content. If an old Windows ANSI Notepad file cannot be decoded, you may opt in to `--fallback-encoding cp1252` **only after verifying that code page**. Unreadable files remain inventoried without lossy text conversion.

**Important:** this GitHub repository is public. `raw/`, `derived/`, `private/`, and `working/` are ignored by default. Do not commit saved conversations or metadata containing private information without deliberate review and permission from everyone whose information may be included. Removing a file later does not reliably remove it from Git history.

## Current evidence boundary

We know a research-repository creation burst occurred in July 2026. GitHub creation timestamps are observable; the dates on which ideas were first conceived are not automatically recoverable. One previously shared mathematical conversation demonstrated plausible cross-domain synthesis and also contained proof gaps. Neither observation establishes a general capability jump. The supplied 2,000+ replies have not yet been inventoried or scientifically reviewed here.

Read [the evidence policy](docs/EVIDENCE_POLICY.md) and [the study protocol](docs/PROTOCOL.md) before interpreting any corpus statistics as research results.
