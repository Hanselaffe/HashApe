"""Backward-compatible entry point for historical users.

The canonical implementation now lives in ``hashape.py``.
"""

from hashape import *  # noqa: F401,F403
from hashape import main


if __name__ == "__main__":
    main()
