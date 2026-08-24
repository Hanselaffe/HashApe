"""Backward-compatible entry point for historical users.

The canonical implementation now lives in ``hashape_core.py``.
"""

from hashape_core import *  # noqa: F401,F403
from hashape_core import main


if __name__ == "__main__":
    main()
