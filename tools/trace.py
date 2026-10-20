#!/usr/bin/env python3
"""Lossless, local-only inventory of user-supplied conversation extracts.

Never writes extracted text, calls network services, or silently infers model
identity / message timestamp / scientific truth from a filename.
"""
from __future__ import annotations

import argparse
import codecs
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

TEXT_EXTENSIONS = {".txt", ".md", ".markdown", ".log"}
DATE_PATTERN = re.compile(r"(?<!\d)(20\d{2})[-_]?([01]\d)[-_]?([0-3]\d)(?!\d)")
DEFAULT_MANIFEST = Path("derived/manifest.jsonl")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def filename_date_hint(relative_path: str) -> str | None:
    """Return a syntactically valid date *hint* found in filename, not a timestamp."""
    for match in DATE_PATTERN.finditer(Path(relative_path).name):
        try:
            return datetime.strptime("".join(match.groups()), "%Y%m%d").date().isoformat()
        except ValueError:
            continue
    return None


def _utf16_from_null_pattern(data: bytes) -> str | None:
    """Detect BOM-less Notepad UTF-16 on strongly alternating NUL patterns."""
    sample = data[:4096]
    if len(sample) < 8 or len(sample) % 2:
        return None
    even = sample[0::2]
    odd = sample[1::2]
    even_ratio = even.count(0) / len(even)
    odd_ratio = odd.count(0) / len(odd)
    if odd_ratio > 0.6 and even_ratio < 0.1:
        return "utf-16-le"
    if even_ratio > 0.6 and odd_ratio < 0.1:
        return "utf-16-be"
    return None


def decode_metadata(raw: bytes, fallback_encoding: str | None = None) -> tuple[str | None, str, int | None]:
    """Decode only to count lines; undecodable content stays unread, never replaced."""
    if raw.startswith(codecs.BOM_UTF8):
        candidates = [("utf-8-sig", "bom")]
    elif raw.startswith(codecs.BOM_UTF16_LE) or raw.startswith(codecs.BOM_UTF16_BE):
        candidates = [("utf-16", "bom")]
    else:
        inferred = _utf16_from_null_pattern(raw)
        candidates = ([(inferred, "zero_byte_pattern")] if inferred else [])
        candidates.append(("utf-8", "strict_utf8"))
        if fallback_encoding:
            candidates.append((fallback_encoding, "user_selected_fallback"))
    for enc, basis in candidates:
        try:
            decoded = raw.decode(enc, errors="strict")
            return enc, basis, len(decoded.splitlines())
        except (UnicodeError, LookupError):
            continue
    return None, "unresolved", None


def scan(source: Path, fallback_encoding: str | None = None) -> list[dict]:
    if not source.is_dir():
        raise ValueError(f"Source directory not found: {source}")
    if fallback_encoding:
        codecs.lookup(fallback_encoding)
    paths = sorted(
        (p for p in source.rglob("*") if p.is_file() and not p.is_symlink()
         and p.suffix.lower() in TEXT_EXTENSIONS),
        key=lambda p: (p.relative_to(source).as_posix().casefold(), p.relative_to(source).as_posix()),
    )
    records = []
    first_for_hash = {}
    for path in paths:
        rel = path.relative_to(source).as_posix()
        raw = path.read_bytes()
        digest = sha256(raw)
        enc, basis, line_count = decode_metadata(raw, fallback_encoding)
        record_id = "file-" + sha256(rel.encode("utf-8"))[:20]
        item = {
            "record_id": record_id,
            "source_id": "sha256:" + digest,
            "relative_path": rel,
            "sha256": digest,
            "size_bytes": len(raw),
            "encoding": enc,
            "encoding_basis": basis,
            "line_count": line_count,
            "filename_date_hint": filename_date_hint(rel),
            "mtime_utc_observed": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
            "duplicate_of": first_for_hash.get(digest),
            "unit_type": "source_file_unknown_message_count",
        }
        first_for_hash.setdefault(digest, record_id)
        records.append(item)
    return records


def write_jsonl(records: list[dict], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp = destination.with_name(destination.name + ".tmp")
    try:
        with temp.open("w", encoding="utf-8", newline="\n") as fh:
            for item in records:
                fh.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")
        temp.replace(destination)
    finally:
        if temp.exists():
            temp.unlink()


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def verify(source: Path, records: list[dict]) -> list[str]:
    """Check file identity, content identity and complete source coverage."""
    errors: list[str] = []
    if not source.is_dir():
        return [f"Source directory not found: {source}"]
    known_paths = set()
    known_ids = set()
    for i, row in enumerate(records, 1):
        rel = row.get("relative_path")
        if not isinstance(rel, str) or not rel or "\\" in rel:
            errors.append(f"record {i}: invalid relative_path")
            continue
        p = Path(rel)
        if p.is_absolute() or any(part in ("..", ".") for part in p.parts):
            errors.append(f"record {i}: unsafe relative_path")
            continue
        if rel in known_paths:
            errors.append(f"record {i}: duplicate relative_path {rel}")
        known_paths.add(rel)
        expected_id = "file-" + sha256(rel.encode("utf-8"))[:20]
        if row.get("record_id") != expected_id or row.get("record_id") in known_ids:
            errors.append(f"record {i}: duplicate or incorrect record_id")
        known_ids.add(row.get("record_id"))
        target = source / p
        if target.is_symlink() or not target.is_file():
            errors.append(f"record {i}: missing or symlinked source: {rel}")
            continue
        raw = target.read_bytes()
        digest = sha256(raw)
        if row.get("sha256") != digest or row.get("source_id") != "sha256:" + digest:
            errors.append(f"record {i}: SHA-256 mismatch: {rel}")
        if row.get("size_bytes") != len(raw):
            errors.append(f"record {i}: byte-size mismatch: {rel}")
    actual = {
        p.relative_to(source).as_posix() for p in source.rglob("*")
        if p.is_file() and not p.is_symlink() and p.suffix.lower() in TEXT_EXTENSIONS
    }
    for rel in sorted(actual - known_paths):
        errors.append(f"unindexed source file: {rel}")
    return errors


def summary(records: list[dict]) -> str:
    dated = [r["filename_date_hint"] for r in records if r.get("filename_date_hint")]
    buckets = Counter(x[:7] for x in dated)
    dups = sum(bool(r.get("duplicate_of")) for r in records)
    undecoded = sum(r.get("encoding") is None for r in records)
    lines = [
        "# Local inventory summary", "",
        "> This is a file inventory, NOT a count of messages or scientific discoveries.",
        "> Filename-derived dates are hints, NOT authenticated conversation timestamps.", "",
        f"- Source files: **{len(records)}**",
        f"- Exact duplicate file contents: **{dups}**",
        f"- Filename date hints: **{len(dated)}**",
        f"- Files with unresolved text encoding: **{undecoded}**", "",
        "## Month from filename hint (unverified)", "",
        "| Month | Files |", "| --- | ---: |",
    ]
    lines += [f"| {month} | {count} |" for month, count in sorted(buckets.items())]
    if not buckets:
        lines.append("| No dated hints | 0 |")
    lines += ["", "Missing source dates, model identities, and user prompts must remain unknown until independently established.", ""]
    return "\n".join(lines)


def _output_outside_source(source: Path, output: Path) -> None:
    if output.resolve().is_relative_to(source.resolve()):
        raise ValueError("Output must be outside the source tree to avoid accidentally indexing generated files")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    p_index = sub.add_parser("index", help="Inventory loose text files without changing them")
    p_index.add_argument("--source", type=Path, default=Path("raw"))
    p_index.add_argument("--output", type=Path, default=DEFAULT_MANIFEST)
    p_index.add_argument("--fallback-encoding", default=None, help="Explicit legacy encoding, e.g. cp1252; never guessed")
    p_verify = sub.add_parser("verify", help="Check indexed files against SHA-256 and detect missing/new files")
    p_verify.add_argument("--source", type=Path, default=Path("raw"))
    p_verify.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    p_report = sub.add_parser("report", help="Build local-only inventory counts")
    p_report.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    p_report.add_argument("--output", type=Path, default=Path("derived/inventory_summary.md"))
    args = ap.parse_args(argv)
    try:
        if args.command == "index":
            _output_outside_source(args.source, args.output)
            rows = scan(args.source, args.fallback_encoding)
            write_jsonl(rows, args.output)
            print(f"Indexed {len(rows)} source files; wrote {args.output}; original bytes unchanged")
        elif args.command == "verify":
            issues = verify(args.source, read_jsonl(args.manifest))
            if issues:
                print("Verification FAILED:\n" + "\n".join("- " + x for x in issues), file=sys.stderr)
                return 1
            print("Verification passed: manifest and source content agree")
        else:
            rows = read_jsonl(args.manifest)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(summary(rows), encoding="utf-8")
            print(f"Wrote {args.output}")
    except (ValueError, FileNotFoundError, LookupError, OSError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
