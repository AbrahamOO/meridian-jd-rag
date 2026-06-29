"""Secret resolution (contracts section 1.6).

Order: environment variable, then mounted secret file /run/secrets/<name>,
then None. Never logs the secret value. The local and mock adapters never call
this resolver.
"""

from __future__ import annotations

import os
from pathlib import Path

SECRETS_DIR = Path("/run/secrets")


def resolve_secret(name: str) -> str | None:
    """Resolve a named secret. Returns the value, or None if not found.

    Lookup order:
      1. environment variable ``name``
      2. mounted secret file ``/run/secrets/<name>``
      3. None
    """
    env_value = os.environ.get(name)
    if env_value:
        return env_value

    secret_file = SECRETS_DIR / name
    try:
        if secret_file.is_file():
            content = secret_file.read_text(encoding="utf-8").strip()
            return content or None
    except OSError:
        return None

    return None
