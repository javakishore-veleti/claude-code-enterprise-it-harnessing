"""SRE semantic tools. Observe first; mutate only with a lease and policy."""

from __future__ import annotations

from typing import Any

from enterprise_it_harnessing.shared.auth import detect_provider
from enterprise_it_harnessing.shared.cli import run_argv
from enterprise_it_harnessing.shared.providers import aws, azure, gcp

MUTATING = {"rollback_deploy", "page_oncall"}


def observe_health(inp: dict[str, Any]) -> str:
    service = inp["service"]
    provider = detect_provider()
    if provider == "aws":
        return run_argv(aws.cloudwatch_alarms(service))
    if provider == "azure":
        resource = inp.get("resource_id") or service
        return run_argv(azure.monitor_metrics(resource))
    if provider == "gcp":
        return run_argv(gcp.monitoring_uptime(service))
    return run_argv(["echo", f"no cloud provider; inspect local process/systemd for {service}"])


def fetch_logs(inp: dict[str, Any]) -> str:
    service = inp["service"]
    since = inp.get("since", "1h")
    return run_argv(["echo", f"fetch logs for {service} since {since} via your log backend"])


def rollback_deploy(inp: dict[str, Any]) -> str:
    return run_argv(["echo", f"rollback {inp['service']} to {inp.get('revision', 'previous')}"])


def page_oncall(inp: dict[str, Any]) -> str:
    return run_argv(["echo", f"page {inp.get('severity', 'sev2')}: {inp['summary']}"])


TOOLS = [
    {
        "name": "observe_health",
        "description": "Read current health/alarms for a service. Provider CLI is selected from identity.",
        "input_schema": {
            "type": "object",
            "properties": {
                "service": {"type": "string"},
                "resource_id": {"type": "string", "description": "Azure resource id when needed"},
            },
            "required": ["service"],
        },
    },
    {
        "name": "fetch_logs",
        "description": "Fetch recent logs for a service. Prefer this over raw bash curl to log stores.",
        "input_schema": {
            "type": "object",
            "properties": {"service": {"type": "string"}, "since": {"type": "string"}},
            "required": ["service"],
        },
    },
    {
        "name": "rollback_deploy",
        "description": "Roll a service back to a prior revision. Requires approval.",
        "input_schema": {
            "type": "object",
            "properties": {"service": {"type": "string"}, "revision": {"type": "string"}},
            "required": ["service"],
        },
    },
    {
        "name": "page_oncall",
        "description": "Open an incident page. Requires approval.",
        "input_schema": {
            "type": "object",
            "properties": {"summary": {"type": "string"}, "severity": {"type": "string"}},
            "required": ["summary"],
        },
    },
]

DISPATCH = {
    "observe_health": observe_health,
    "fetch_logs": fetch_logs,
    "rollback_deploy": rollback_deploy,
    "page_oncall": page_oncall,
}
