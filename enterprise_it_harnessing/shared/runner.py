"""Professional REPL: streaming loop, on-demand skills, cached system prefix, cloud identity."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable

from core import EXTENDED_DISPATCH, EXTENDED_TOOLS, stream_loop
from harness_log import enable_debug, get_logger

from enterprise_it_harnessing.catalog import CATALOG_DISPATCH, CATALOG_TOOLS

from .auth import CloudIdentity, resolve_identity
from .guard import load_rules, wrap_dispatch
from .skills import discover_skills, index_text, load_skill

log = get_logger("runner")

_REPORT_FORMAT = (
    "Default answer structure (use this unless the operator gave a different format):\n"
    "## Input\n"
    "What they asked — job, instance, metric. One or two lines.\n"
    "## What it is doing\n"
    "Skill and tools you ran. One or two lines. Do not dump argv or npm paths.\n"
    "## What it found\n"
    "The measured values. Lead with numbers. Do not recap policy if a number exists.\n"
    "## Final output\n"
    "- bullet: severity\n"
    "- bullet: next action\n"
    "- bullet: any constraint (no failover, approval, etc.)\n"
    "**Summary:** one sentence.\n"
    "Do not invent token counts. The harness prints ## Tokens after your answer."
)


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
    if args.debug:
        enable_debug()

    once = args.once or (" ".join(args.prompt) if args.prompt else "")
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
            log.error("unknown tool: %s", args.tool)
            log.error("available: %s", ", ".join(sorted(dispatch)))
            sys.exit(2)
        result = dispatch[args.tool](payload)
        sys.stdout.write(result + "\n")
        if not args.interactive:
            return
        persona = _system(system, identity, skills)
        history: list[dict[str, Any]] = []
        if args.tool == "load_skill":
            history.append({"role": "user", "content": "Follow this skill:\n\n" + result})
        _repl(prompt, history, tools, dispatch, persona)
        return

    persona = _system(system, identity, skills)
    log.debug("%s provider=%s principal=%s", name, identity.provider, identity.principal or "n/a")

    history: list[dict[str, Any]] = []
    if once:
        if args.with_skill:
            once = (
                f"{load_skill(skills_dir, args.with_skill)}\n\n"
                f"Follow that skill for this job:\n{once}\n\n"
                f"{_REPORT_FORMAT}"
            )
        history.append({"role": "user", "content": once})
        stream_loop(
            messages=history,
            tools=tools,
            dispatch=dispatch,
            system=persona,
            report_usage=True,
        )
        if not args.interactive:
            return
        _repl(prompt, history, tools, dispatch, persona)
        return

    _repl(prompt, history, tools, dispatch, persona)


def _parse_args(name: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog=name, add_help=True)
    parser.add_argument("prompt", nargs="*", help="One-shot operator prompt (skips the REPL)")
    parser.add_argument("--once", "-q", dest="once", help="One-shot prompt (same as positional prompt)")
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Optional. After printing output, keep this session open as a REPL.",
    )
    parser.add_argument("--tool", help="Run a typed tool without the model (catalog dumps, identity)")
    parser.add_argument("--json", help="JSON object passed to --tool (optional; prefer --bu/--service flags)")
    parser.add_argument("--bu", dest="business_unit", help="business_unit for --tool")
    parser.add_argument("--service", help="service for --tool")
    parser.add_argument("--instance", help="database instance for --tool")
    parser.add_argument("--target", help="cache/target for --tool")
    parser.add_argument("--topic", help="kafka topic for --tool")
    parser.add_argument("--domain", help="domain filter for --tool")
    parser.add_argument("--skill", dest="skill_name", help="skill name for --tool load_skill")
    parser.add_argument(
        "--with-skill",
        dest="with_skill",
        help="Inject a skill runbook into a --once job so Claude follows it",
    )
    parser.add_argument("--debug", action="store_true", help="Log tool calls, audit events, and stop reasons")
    return parser.parse_args()


def _repl(
    prompt: str,
    history: list[dict[str, Any]],
    tools: list[dict[str, Any]],
    dispatch: dict[str, Callable[[dict[str, Any]], str]],
    persona: list[dict[str, Any]],
) -> None:
    while True:
        try:
            query = input(f"{prompt} >> ").strip()
        except (EOFError, KeyboardInterrupt):
            log.info("Session closed.")
            return
        if not query or query.lower() in {"q", "exit", "quit"}:
            log.info("Goodbye.")
            return
        history.append({"role": "user", "content": query})
        stream_loop(
            messages=history,
            tools=tools,
            dispatch=dispatch,
            system=persona,
            report_usage=True,
        )


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
    if getattr(args, "skill_name", None):
        payload["name"] = args.skill_name
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
        "Never invent cloud credentials. If a CLI is missing, return the intended argv.\n"
        f"{_REPORT_FORMAT}\n"
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
