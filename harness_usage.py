"""Token usage and cost from the API response + repo-root model_costs.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
COSTS_PATH = ROOT / "model_costs.json"


def add_usage(totals: dict[str, int], usage: Any) -> None:
    if usage is None:
        return
    for key in (
        "input_tokens",
        "output_tokens",
        "cache_creation_input_tokens",
        "cache_read_input_tokens",
    ):
        totals[key] = totals.get(key, 0) + int(getattr(usage, key, 0) or 0)


def empty_totals() -> dict[str, int]:
    return {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
    }


def load_costs() -> list[dict[str, Any]]:
    if not COSTS_PATH.is_file():
        return []
    data = json.loads(COSTS_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        return []
    return [row for row in data if isinstance(row, dict)]


def match_cost(model: str, rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    needle = (model or "").lower()
    for row in rows:
        names = [str(row.get("model", ""))] + [str(a) for a in row.get("aliases") or []]
        for name in names:
            key = name.lower()
            if not key:
                continue
            if needle == key or needle.startswith(key) or key.startswith(needle):
                return row
    return None


def _usd(tokens: int, per_million: float) -> float:
    return (tokens / 1_000_000) * per_million


def format_usage(model: str, totals: dict[str, int]) -> str:
    rows = load_costs()
    rate = match_cost(model, rows)
    inp = totals.get("input_tokens", 0)
    out = totals.get("output_tokens", 0)
    cache_w = totals.get("cache_creation_input_tokens", 0)
    cache_r = totals.get("cache_read_input_tokens", 0)
    lines = [
        "## Tokens",
        f"- model: `{model}`",
        f"- source: `{COSTS_PATH.name}`",
    ]
    if not rate:
        lines.extend(
            [
                f"- input: {inp} tokens (no unit cost for this model in {COSTS_PATH.name})",
                f"- output: {out} tokens",
                "- overall: n/a",
            ]
        )
        return "\n".join(lines)

    currency = rate.get("currency", "USD")
    unit = rate.get("unit", "per_1m_tokens")
    in_rate = float(rate["input"])
    out_rate = float(rate["output"])
    cw_rate = float(rate.get("cache_write", 0) or 0)
    cr_rate = float(rate.get("cache_read", 0) or 0)
    in_cost = _usd(inp, in_rate)
    out_cost = _usd(out, out_rate)
    cw_cost = _usd(cache_w, cw_rate)
    cr_cost = _usd(cache_r, cr_rate)
    overall = in_cost + out_cost + cw_cost + cr_cost
    lines.extend(
        [
            f"- unit: {currency} {unit}",
            f"- input: {inp} tokens @ ${in_rate:.2f}/1M = ${in_cost:.6f}",
            f"- output: {out} tokens @ ${out_rate:.2f}/1M = ${out_cost:.6f}",
        ]
    )
    if cache_w:
        lines.append(f"- cache write: {cache_w} tokens @ ${cw_rate:.2f}/1M = ${cw_cost:.6f}")
    if cache_r:
        lines.append(f"- cache read: {cache_r} tokens @ ${cr_rate:.2f}/1M = ${cr_cost:.6f}")
    lines.append(f"- overall: ${overall:.6f} {currency}")
    return "\n".join(lines)


def print_usage(model: str, totals: dict[str, int]) -> None:
    text = format_usage(model, totals)
    sys.stdout.write("\n" + text + "\n")
    sys.stdout.flush()
