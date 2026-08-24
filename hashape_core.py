"""HashApe core utilities and interactive CLI.

HashApe is intentionally a small, local educational tool. It does not perform
network authentication attempts and it does not include optimized cracking
engines.
"""

from __future__ import annotations

import hashlib
import itertools
import string
from pathlib import Path

_SUPPORTED_ALGORITHMS: dict[str, int] = {
    "md5": 32,
    "sha256": 64,
}

_DEFAULT_CHARSET = string.ascii_lowercase + string.digits
_MAX_BRUTE_FORCE_LENGTH = 8


def _normalize_algorithm(algorithm: str) -> str:
    normalized = algorithm.strip().lower()
    if normalized not in _SUPPORTED_ALGORITHMS:
        supported = ", ".join(sorted(_SUPPORTED_ALGORITHMS))
        raise ValueError(f"Unsupported hash algorithm: {algorithm!r}. Supported: {supported}")
    return normalized


def hash_string(text: str, algorithm: str) -> str:
    """Return the hexadecimal digest for *text* using a supported algorithm."""
    normalized = _normalize_algorithm(algorithm)
    return hashlib.new(normalized, text.encode("utf-8")).hexdigest()


def validate_hash(hash_value: str, algorithm: str) -> str:
    """Validate and normalize a hexadecimal hash value."""
    normalized_algorithm = _normalize_algorithm(algorithm)
    normalized_hash = hash_value.strip().lower()
    expected_length = _SUPPORTED_ALGORITHMS[normalized_algorithm]

    if len(normalized_hash) != expected_length:
        raise ValueError(
            f"Invalid {normalized_algorithm} digest length: expected {expected_length} hexadecimal characters"
        )

    try:
        int(normalized_hash, 16)
    except ValueError as exc:
        raise ValueError("Hash value must contain hexadecimal characters only") from exc

    return normalized_hash


def brute_force(
    hash_to_crack: str,
    algorithm: str,
    charset: str = _DEFAULT_CHARSET,
    max_length: int = 4,
) -> str | None:
    """Search a bounded local character space and return the matching plaintext.

    This implementation is deliberately simple and single-threaded. It is suited
    to demonstrations and small test fixtures, not large-scale password recovery.
    """
    target = validate_hash(hash_to_crack, algorithm)

    if not charset:
        raise ValueError("charset must not be empty")
    if not isinstance(max_length, int) or isinstance(max_length, bool):
        raise TypeError("max_length must be an integer")
    if not 1 <= max_length <= _MAX_BRUTE_FORCE_LENGTH:
        raise ValueError(f"max_length must be between 1 and {_MAX_BRUTE_FORCE_LENGTH}")

    for length in range(1, max_length + 1):
        for attempt_tuple in itertools.product(charset, repeat=length):
            attempt = "".join(attempt_tuple)
            if hash_string(attempt, algorithm) == target:
                return attempt
    return None


def threaded_brute_force(
    hash_to_crack: str,
    algorithm: str,
    charset: str,
    max_length: int,
    num_threads: int,
) -> str | None:
    """Compatibility wrapper for the historical threaded API.

    The old implementation launched multiple threads that all repeated the same
    complete search. Retaining that behavior wastes CPU without improving
    correctness, so the compatibility wrapper performs one bounded search.
    """
    if not isinstance(num_threads, int) or isinstance(num_threads, bool) or num_threads < 1:
        raise ValueError("num_threads must be a positive integer")
    return brute_force(hash_to_crack, algorithm, charset, max_length)


def dictionary_attack(hash_to_crack: str, algorithm: str, wordlist_file: str | Path) -> str | None:
    """Return the first word in *wordlist_file* whose digest matches the target."""
    target = validate_hash(hash_to_crack, algorithm)
    path = Path(wordlist_file).expanduser()

    if not path.is_file():
        raise FileNotFoundError(f"Wordlist not found: {path}")

    with path.open("r", encoding="utf-8", errors="replace") as wordlist:
        for line in wordlist:
            word = line.rstrip("\r\n")
            if hash_string(word, algorithm) == target:
                return word
    return None


def identify_hash(hash_value: str) -> str:
    """Identify common hexadecimal digest families by length.

    Length alone cannot prove which algorithm created a digest, so the returned
    text is intentionally phrased as a candidate rather than a certainty.
    """
    normalized = hash_value.strip().lower()
    if not normalized:
        return "Unknown hash type"

    try:
        int(normalized, 16)
    except ValueError:
        return "Unknown hash type (not hexadecimal)"

    candidates = {
        32: "MD5 candidate (32 hexadecimal characters)",
        40: "SHA-1 candidate (40 hexadecimal characters)",
        64: "SHA-256 candidate (64 hexadecimal characters)",
        128: "SHA-512 candidate (128 hexadecimal characters)",
    }
    return candidates.get(len(normalized), "Unknown hash type (length does not match common digests)")


def show_banner() -> None:
    print("HashApe - local hash verification and educational search tool")


def show_menu() -> None:
    print("\n1. Bounded brute-force demonstration")
    print("2. Dictionary lookup")
    print("3. Identify hash candidate")
    print("4. Exit")


def _read_int(prompt: str) -> int:
    value = input(prompt).strip()
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"Expected an integer, got {value!r}") from exc


def main() -> None:
    show_banner()

    while True:
        show_menu()
        choice = input("Select an option (1/2/3/4): ").strip()

        try:
            if choice == "1":
                hash_input = input("Enter the hash: ")
                algorithm = input("Enter algorithm (md5/sha256): ")
                max_length = _read_int(f"Maximum length (1-{_MAX_BRUTE_FORCE_LENGTH}): ")
                result = brute_force(hash_input, algorithm, _DEFAULT_CHARSET, max_length)
                print(f"Match: {result}" if result is not None else "No match found in the bounded search space.")
            elif choice == "2":
                hash_input = input("Enter the hash: ")
                algorithm = input("Enter algorithm (md5/sha256): ")
                wordlist = input("Enter path to wordlist file: ")
                result = dictionary_attack(hash_input, algorithm, wordlist)
                print(f"Match: {result}" if result is not None else "No match found in the wordlist.")
            elif choice == "3":
                print(identify_hash(input("Enter the hash to identify: ")))
            elif choice == "4":
                return
            else:
                print("Invalid option. Please select 1, 2, 3, or 4.")
        except (FileNotFoundError, TypeError, ValueError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
