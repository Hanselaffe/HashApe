from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

import hashape_core as hashape


class HashApeTests(unittest.TestCase):
    def test_hash_string_md5(self) -> None:
        self.assertEqual(hashape.hash_string("test", "md5"), hashlib.md5(b"test").hexdigest())

    def test_hash_string_sha256(self) -> None:
        self.assertEqual(
            hashape.hash_string("test", "sha256"),
            hashlib.sha256(b"test").hexdigest(),
        )

    def test_unsupported_algorithm_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            hashape.hash_string("test", "sha1")

    def test_validate_hash_rejects_non_hex(self) -> None:
        with self.assertRaises(ValueError):
            hashape.validate_hash("z" * 32, "md5")

    def test_identify_hash_sha256_candidate(self) -> None:
        self.assertEqual(
            hashape.identify_hash("a" * 64),
            "SHA-256 candidate (64 hexadecimal characters)",
        )

    def test_dictionary_attack_finds_matching_word(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "words.txt"
            path.write_text("alpha\nbeta\ngamma\n", encoding="utf-8")
            target = hashape.hash_string("beta", "sha256")
            self.assertEqual(hashape.dictionary_attack(target, "sha256", path), "beta")

    def test_dictionary_attack_returns_none_without_match(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "words.txt"
            path.write_text("alpha\nbeta\n", encoding="utf-8")
            target = hashape.hash_string("gamma", "md5")
            self.assertIsNone(hashape.dictionary_attack(target, "md5", path))

    def test_bounded_brute_force_finds_small_fixture(self) -> None:
        target = hashape.hash_string("ba", "md5")
        self.assertEqual(hashape.brute_force(target, "md5", charset="ab", max_length=2), "ba")

    def test_brute_force_rejects_unbounded_length(self) -> None:
        target = hashape.hash_string("a", "md5")
        with self.assertRaises(ValueError):
            hashape.brute_force(target, "md5", charset="ab", max_length=9)


if __name__ == "__main__":
    unittest.main()
