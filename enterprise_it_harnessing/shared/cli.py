"""Safe argv execution. Prefer typed tools over raw bash (s14)."""

from __future__ import annotations

import json
import shutil
import subprocess
from typing import Any


def run_argv(argv: list[str], timeout: int = 45) -> str:
    """Run a command as an argument list. Never interpolates into a shell."""
    if not argv:
        return _payload(ok=False, error="empty command")
    if not shutil.which(argv[0]):
        return _payload(ok=False, error=f"{argv[0]} is not on PATH", argv=argv)
    try:
        result = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return _payload(
            ok=result.returncode == 0,
            code=result.returncode,
            stdout=(result.stdout or "")[-20_000:],
            stderr=(result.stderr or "")[-4_000:],
            argv=argv,
        )
    except subprocess.TimeoutExpired:
        return _payload(ok=False, error=f"timeout after {timeout}s", argv=argv)
    except OSError as exc:
        return _payload(ok=False, error=str(exc), argv=argv)


def _payload(**fields: Any) -> str:
    return json.dumps(fields, default=str)
