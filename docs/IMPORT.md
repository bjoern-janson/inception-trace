# Importing loose Notepad replies

## Before copying anything

This is a **public** GitHub repository. Keep private source messages in `raw/` locally, not in GitHub. Check for names, account data, access tokens, screenshots, private communications, and details of third parties. A `.gitignore` file reduces accidents but is not an access-control mechanism: `git add -f` can still publish ignored files.

1. Preserve an untouched, offline backup of the original Notepad folder (including subfolders and names). Do not batch-rename or edit the originals. A ZIP kept **outside the public repo** is useful as a preservation copy.
2. Copy files into the repository's local `raw/` directory. Nested folders are okay. The tooling doesn't modify these files.
3. Retain any external evidence of prompt text, platform message timestamps, model selection, account plan, model/system notices, and export history as *separate* sources; don't splice them into archived assistant replies.
4. Work from the repository root in PowerShell, CMD, or a terminal.

If preserving Windows copy metadata matters, consider Windows `robocopy` rather than a paste that changes metadata. **Even faithfully copied filesystem timestamps do not prove the conversation date.**

## Commands

```powershell
python tools/trace.py index --source raw --output derived/manifest.jsonl
python tools/trace.py verify --source raw --manifest derived/manifest.jsonl
python tools/trace.py report --manifest derived/manifest.jsonl --output derived/inventory_summary.md
```

The inventory supports `.txt`, `.md`, `.markdown`, `.log` (case-insensitive), recurses through subdirectories, skips symlinked files, hashes the **original bytes**, and records duplicates without deleting them. It excludes `.rtf`, images, documents, and binary archives until a separate, appropriately validated importer exists.

The manifest is one JSON object per source **file**, not per message. Its fields are defined in `schemas/source-record.schema.json`.

### Notepad encoding

The tool attempts strict UTF-8 (with or without BOM), BOM-marked UTF-16, and strongly indicated BOM-less UTF-16. It will **not** silently replace undecodable bytes. If your original files are from an older Western Windows ANSI code page and you've verified that encoding independently, run:

```powershell
python tools/trace.py index --source raw --output derived/manifest.jsonl --fallback-encoding cp1252
```

A selected fallback is recorded as such; no charset guess becomes source truth. Original bytes and SHA-256 remain unchanged. Non-Western Windows code pages must be chosen appropriately instead of blindly using `cp1252`.

### After importing

Read `derived/inventory_summary.md`; check unexpected undated/unreadable files and exact duplicates. `verify` will flag missing, changed, and newly added files. Re-index intentionally if the source set changed; preserve the previous manifest in private archival storage if you need to prove when an inventory snapshot was taken.

**Do not publish raw files just because the inventory succeeded.** Upload a ZIP to a private analysis context instead, or explicitly approve a reviewed, redacted public subset later.
