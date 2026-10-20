"""Synthetic fixtures only. No user conversation text appears in this repository."""
import json
from pathlib import Path
import tempfile
import unittest

from tools.trace import (
    decode_metadata, filename_date_hint, read_jsonl, scan, summary,
    verify, write_jsonl, _output_outside_source,
)


class ArchiveTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.raw = self.root / "raw"
        self.raw.mkdir()

    def test_filename_hints_are_validated(self):
        self.assertEqual(filename_date_hint("20260717-note.txt"), "2026-07-17")
        self.assertEqual(filename_date_hint("m/2026_08_09.txt"), "2026-08-09")
        self.assertIsNone(filename_date_hint("20261355-claim.txt"))
        self.assertIsNone(filename_date_hint("undated.txt"))

    def test_bomless_utf16_recognition(self):
        enc, basis, lines = decode_metadata("one\ntwo\n".encode("utf-16-le"))
        self.assertEqual((enc, basis, lines), ("utf-16-le", "zero_byte_pattern", 2))

    def test_lossless_manifest_duplicates_and_verify(self):
        (self.raw / "20260717-a.txt").write_bytes(b"first\nsecond\n")
        (self.raw / "copy.txt").write_bytes(b"first\nsecond\n")
        (self.raw / "utf16.txt").write_bytes("hello\nworld\n".encode("utf-16"))
        (self.raw / "image.jpg").write_bytes(b"not text")
        nested = self.raw / "nested"
        nested.mkdir()
        (nested / "unknown.txt").write_bytes(b"\x81\x82")
        rows = scan(self.raw)
        self.assertEqual(len(rows), 4)
        self.assertEqual(sum(bool(r["duplicate_of"]) for r in rows), 1)
        self.assertEqual(sum(r["encoding"] is None for r in rows), 1)
        self.assertIn("2026-07", summary(rows))
        manifest = self.root / "derived" / "manifest.jsonl"
        write_jsonl(rows, manifest)
        loaded = read_jsonl(manifest)
        self.assertEqual(rows, loaded)
        self.assertEqual(verify(self.raw, loaded), [])
        (self.raw / "copy.txt").write_bytes(b"modified")
        self.assertTrue(any("mismatch" in issue for issue in verify(self.raw, loaded)))
        (self.raw / "new.txt").write_text("new")
        self.assertTrue(any("unindexed" in issue for issue in verify(self.raw, loaded)))

    def test_output_must_be_outside_raw(self):
        with self.assertRaises(ValueError):
            _output_outside_source(self.raw, self.raw / "manifest.jsonl")

    def test_optional_codepage_is_explicit(self):
        raw = "café".encode("cp1252")
        self.assertEqual(decode_metadata(raw)[:2], (None, "unresolved"))
        self.assertEqual(decode_metadata(raw, "cp1252")[:2], ("cp1252", "user_selected_fallback"))


if __name__ == "__main__":
    unittest.main()
