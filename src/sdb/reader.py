"""Read seriousdb database files."""

import json
from pathlib import Path


def load(filename: str | Path) -> dict[str, str]:
    """Load a seriousdb database file."""
    filename = Path(filename)

    with filename.open("rb") as f:
        db = json.loads(f.read().decode())

    if not isinstance(db, dict):
        raise TypeError(f"expected dict, got {type(db).__name__}")

    if not all(
        isinstance(key, str) and isinstance(value, str) for key, value in db.items()
    ):
        raise TypeError("expected database containing string keys and values")

    return db
