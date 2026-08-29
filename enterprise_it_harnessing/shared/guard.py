"""Guarded dispatch (s15) plus isolation leases (s12/s23) and audit events (s16)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import yaml

from core import check_permission

from .events import EventBus, audit_to_stdout
from .isolation import acquire, release


def load_rules(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"always_deny": [], "always_allow": [], "ask_user": []}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def wrap_dispatch(
    domain: str,
    dispatch: dict[str, Callable[[dict[str, Any]], str]],
    rules: dict[str, Any],
    mutating: set[str],
    bus: EventBus | None = None,
) -> dict[str, Callable[[dict[str, Any]], str]]:
    bus = bus or EventBus()
    bus.on("pre_tool_use", audit_to_stdout)
    bus.on("post_tool_use", audit_to_stdout)

    guarded: dict[str, Callable[[dict[str, Any]], str]] = {}
    for name, handler in dispatch.items():
        guarded[name] = _guard(domain, name, handler, rules, mutating, bus)
    return guarded


def _guard(
    domain: str,
    tool_name: str,
    handler: Callable[[dict[str, Any]], str],
    rules: dict[str, Any],
    mutating: set[str],
    bus: EventBus,
) -> Callable[[dict[str, Any]], str]:
    def run(inp: dict[str, Any]) -> str:
        check_str = str(next(iter(inp.values()), tool_name))
        target = str(inp.get("target") or inp.get("instance") or inp.get("cluster") or inp.get("topic") or check_str)
        bus.emit("pre_tool_use", tool=tool_name, target=target)
        allowed, reason = check_permission(tool_name, check_str, rules)
        if not allowed:
            return f"Blocked by policy: {reason}"
        lease_needed = tool_name in mutating
        if lease_needed:
            lease = acquire(domain, target, tool_name)
            try:
                parsed = json.loads(lease)
            except ValueError:
                parsed = {"ok": False, "error": lease}
            if not parsed.get("ok"):
                return lease
        try:
            output = handler(inp)
        except Exception as exc:
            bus.emit("tool_error", tool=tool_name, target=target, error=str(exc))
            return f"Error: {exc}"
        finally:
            if lease_needed:
                release(domain, target)
        bus.emit("post_tool_use", tool=tool_name, target=target)
        return output

    return run
