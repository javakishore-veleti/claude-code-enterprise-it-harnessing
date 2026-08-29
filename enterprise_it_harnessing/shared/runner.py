"""Professional REPL: streaming loop, on-demand skills, cached system prefix, cloud identity."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable

from core import EXTENDED_DISPATCH, EXTENDED_TOOLS, stream_loop

from enterprise_it_harnessing.catalog import CATALOG_DISPATCH, CATALOG_TOOLS

from .auth import CloudIdentity, resolve_identity
from .guard import load_rules, wrap_dispatch
from .skills import discover_skills, index_text, load_skill


def run_harness(
    *,
    name: str,
    prompt: str,
    domain_dir: Path,
    extra_tools: list[dict[str, Any]],
    extra_dispatch: dict[str, Callable[[dict[str, Any]], str]],
    mutating: set[str],
    system: str,
) -> None:
    root = Path(__file__).resolve().parents[2]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    args = _parse_args(name)
    identity = resolve_identity()
    skills_dir = domain_dir / "skills"
    skills = discover_skills(skills_dir)
    rules = load_rules(domain_dir / "permissions.yaml")

    def list_skills(_: dict[str, Any]) -> str:
        return index_text(skills)

    def load_named(inp: dict[str, Any]) -> str:
        return load_skill(skills_dir, inp["name"])

    def show_identity(_: dict[str, Any]) -> str:
        return identity.as_json()

    dispatch = wrap_dispatch(
        name,
        {
            **EXTENDED_DISPATCH,
            **CATALOG_DISPATCH,
            **extra_dispatch,
            "list_skills": list_skills,
            "load_skill": load_named,
            "cloud_identity": show_identity,
        },
        rules,
        mutating,
    )
    tools = EXTENDED_TOOLS + CATALOG_TOOLS + extra_tools + _meta_tools()
    _mark_cacheable(tools)

    if args.tool:
        payload = _tool_payload(args)
        if args.tool not in dispatch:
            print(f"unknown tool: {args.tool}", file=sys.stderr)
            print("available:", ", ".join(sorted(dispatch)), file=sys.stderr)
            sys.exit(2)
        print(dispatch[args.tool](payload))
        return

    persona = _system(system, identity, skills)
    print(f"\033[90m{name} | provider={identity.provider} | principal={identity.principal or 'n/a'}\033[0m")
    print("\033[90m  skills via list_skills / load_skill · mutations leased · policy from permissions.yaml\033[0m\n")

    once = args.once or (" ".join(args.prompt) if args.prompt else "")
    if once:
        history: list[dict[str, Any]] = [{"role": "user", "content": once}]
        stream_loop(messages=history, tools=tools, dispatch=dispatch, system=persona)
        print()
        return

    history = []
    while True:
        try:
            query = input(f"\033[36m{prompt} >> \033[0m").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSession closed.")
            return
        if not query or query.lower() in {"q", "exit", "quit"}:
            print("Goodbye.")
            return
        history.append({"role": "user", "content": query})
        stream_loop(messages=history, tools=tools, dispatch=dispatch, system=persona)
        print()


def _parse_args(name: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog=name, add_help=True)
    parser.add_argument("prompt", nargs="*", help="One-shot operator prompt (skips the REPL)")
    parser.add_argument("--once", "-q", dest="once", help="One-shot prompt (same as positional prompt)")
    parser.add_argument("--tool", help="Run a typed tool without the model (catalog dumps, identity)")
    parser.add_argument("--json", help="JSON object passed to --tool (optional; prefer --bu/--service flags)")
    parser.add_argument("--bu", dest="business_unit", help="business_unit for --tool")
    parser.add_argument("--service", help="service for --tool")
    parser.add_argument("--instance", help="database instance for --tool")
    parser.add_argument("--target", help="cache/target for --tool")
    parser.add_argument("--topic", help="kafka topic for --tool")
    parser.add_argument("--domain", help="domain filter for --tool")
    return parser.parse_args()


def _tool_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if args.json:
        try:
            payload.update(json.loads(args.json))
        except json.JSONDecodeError:
            # npm often strips the quotes from {\"k\":\"v\"}; flags below still apply.
            pass
    for key in ("business_unit", "service", "instance", "target", "topic", "domain"):
        val = getattr(args, key, None)
        if val:
            payload[key] = val
    return payload


def _system(base: str, identity: CloudIdentity, skills: dict[str, str]) -> list[dict[str, Any]]:
    text = (
        f"{base}\n\n"
        f"Cloud identity: {identity.as_json()}\n"
        "This enterprise runs FOREX trade-processing middleware for banks, "
        "e-commerce middleware (catalog, quote, orders, shipping, fulfillment, "
        "customer profile, support, advisor, product research), and Shopify headless "
        "merchant integration (webhooks plus legacy / on-prem sync). "
        "There are 10 business units and about 100 microservices. "
        "Call list_business_units / list_services / resolve_service before guessing a cluster or account. "
        "Prefer typed domain tools over raw bash. Load a skill before following a runbook. "
        "Mutating tools take an isolation lease; if a target is dirty or conflicted, stop and report. "
        "Never invent cloud credentials. If a CLI is missing, return the intended argv.\n\n"
        f"Available skills:\n{index_text(skills)}"
    )
    return [
        {
            "type": "text",
            "text": text,
            "cache_control": {"type": "ephemeral"},
        }
    ]


def _meta_tools() -> list[dict[str, Any]]:
    return [
        {
            "name": "list_skills",
            "description": "List domain runbook skills available to this harness.",
            "input_schema": {"type": "object", "properties": {}},
        },
        {
            "name": "load_skill",
            "description": "Load a skill runbook into context before applying it.",
            "input_schema": {
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
            },
        },
        {
            "name": "cloud_identity",
            "description": "Show the resolved AWS, Azure, GCP, or local identity. Auth differs; operations do not.",
            "input_schema": {"type": "object", "properties": {}},
        },
    ]


def _mark_cacheable(tools: list[dict[str, Any]]) -> None:
    if not tools:
        return
    tools[-1] = {**tools[-1], "cache_control": {"type": "ephemeral"}}
