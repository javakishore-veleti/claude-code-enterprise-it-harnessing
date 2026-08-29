"""Resource isolation: dirty-check, conflict-detect, stale-prune.

Applies exclusive leases to operational targets (cluster, instance,
topic, cache). Parallel mutations on the same target
are refused until the lease is released or pruned.
"""

from __future__ import annotations

import json
import re
import threading
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path

_LOCK = threading.Lock()
_STORE = Path(".harness_isolation")
_SAFE = re.compile(r"[^a-zA-Z0-9._/-]+")
DEFAULT_TTL_SECONDS = 45 * 60


@dataclass
class Lease:
    lease_id: str
    domain: str
    target: str
    operation: str
    created_at: float
    dirty: bool = False
    note: str = ""

    def expired(self, ttl: int = DEFAULT_TTL_SECONDS) -> bool:
        return (time.time() - self.created_at) > ttl


def sanitize(value: str) -> str:
    cleaned = _SAFE.sub("-", value.strip().lower()).strip("-")
    return cleaned[:80] or "unnamed"


def acquire(domain: str, target: str, operation: str) -> str:
    """Take an exclusive lease. Fails on dirty markers or live conflicts."""
    key = sanitize(target)
    with _LOCK:
        prune_stale(domain)
        existing = _load(domain, key)
        if existing:
            if existing.dirty:
                return _fail(f"dirty target {key}: {existing.note or existing.operation}")
            if not existing.expired():
                return _fail(f"conflict: {existing.lease_id} holds {key} for {existing.operation}")
            _delete(domain, key)
        lease = Lease(
            lease_id=uuid.uuid4().hex[:8],
            domain=domain,
            target=key,
            operation=operation,
            created_at=time.time(),
        )
        _save(lease)
        return json.dumps({"ok": True, "lease": asdict(lease)})


def mark_dirty(domain: str, target: str, note: str) -> str:
    key = sanitize(target)
    with _LOCK:
        lease = _load(domain, key)
        if not lease:
            return _fail(f"no lease for {key}")
        lease.dirty = True
        lease.note = note
        _save(lease)
        return json.dumps({"ok": True, "lease": asdict(lease)})


def release(domain: str, target: str) -> str:
    key = sanitize(target)
    with _LOCK:
        path = _path(domain, key)
        if path.exists():
            path.unlink()
        return json.dumps({"ok": True, "released": key})


def prune_stale(domain: str | None = None, ttl: int = DEFAULT_TTL_SECONDS) -> str:
    removed: list[str] = []
    roots = [_STORE / domain] if domain else [p for p in _STORE.glob("*") if p.is_dir()]
    for root in roots:
        if not root.exists():
            continue
        for path in root.glob("*.json"):
            try:
                lease = Lease(**json.loads(path.read_text(encoding="utf-8")))
            except (OSError, TypeError, json.JSONDecodeError):
                path.unlink(missing_ok=True)
                removed.append(path.stem)
                continue
            if lease.expired(ttl) and not lease.dirty:
                path.unlink(missing_ok=True)
                removed.append(lease.target)
    return json.dumps({"ok": True, "pruned": removed})


def _path(domain: str, target: str) -> Path:
    return _STORE / sanitize(domain) / f"{target}.json"


def _load(domain: str, target: str) -> Lease | None:
    path = _path(domain, target)
    if not path.exists():
        return None
    try:
        return Lease(**json.loads(path.read_text(encoding="utf-8")))
    except (OSError, TypeError, json.JSONDecodeError):
        return None


def _save(lease: Lease) -> None:
    path = _path(lease.domain, lease.target)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(lease), indent=2), encoding="utf-8")


def _delete(domain: str, target: str) -> None:
    _path(domain, target).unlink(missing_ok=True)


def _fail(message: str) -> str:
    return json.dumps({"ok": False, "error": message})
