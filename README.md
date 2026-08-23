# HashApe

HashApe is a small local Python utility for learning about hexadecimal password hashes, verifying candidate plaintexts, performing bounded demonstration searches, and checking a local wordlist.

## Scope

HashApe is intended for local educational use and authorized recovery/testing only. It does not perform network authentication attempts and it deliberately avoids optimized cracking engines.

## Changes in the 2026 refresh

- fixes the broken dictionary lookup path;
- validates algorithms and hexadecimal digest input;
- corrects SHA-256 identification text;
- removes the historical duplicate-work threading behavior while keeping a compatibility wrapper;
- adds bounded input handling and clearer errors;
- adds a lowercase canonical `hashape.py` entry point while retaining `Hashape.py` for compatibility;
- adds standard-library unit tests;
- requires no third-party Python packages.

## Requirements

- Python 3.10 or newer

## Run

```bash
python hashape.py
```

The historical command also continues to work:

```bash
python Hashape.py
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## Supported hashing operations

The active verification/search functions support:

- MD5
- SHA-256

Hash identification additionally reports length-based candidates for SHA-1 and SHA-512. A digest length is only a hint and cannot prove which algorithm produced a value.

## Safety and performance

The built-in brute-force demonstration is intentionally simple, local, single-process, and bounded to short candidate lengths. For real password storage, use a modern password-hashing scheme such as Argon2id, scrypt, or bcrypt rather than fast general-purpose hashes such as MD5 or SHA-256.
