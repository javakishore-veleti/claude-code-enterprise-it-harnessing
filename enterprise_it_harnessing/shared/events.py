"""Minimal event bus for audit hooks."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Callable


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable[..., Any]]] = defaultdict(list)

    def on(self, event: str, handler: Callable[..., Any]) -> None:
        self._handlers[event].append(handler)

    def emit(self, event: str, **payload: Any) -> list[Any]:
        results: list[Any] = []
        stamped = {"ts": datetime.now(timezone.utc).isoformat(), "event": event, **payload}
        for handler in self._handlers.get(event, []):
            try:
                results.append(handler(**stamped))
            except Exception as exc:  # hooks must never break the loop
                results.append(exc)
        return results


def audit_to_stdout(event: str, **payload: Any) -> None:
    tool = payload.get("tool", "")
    target = str(payload.get("target", ""))[:80]
    print(f"\033[90m  [audit] {event} {tool} {target}\033[0m")
