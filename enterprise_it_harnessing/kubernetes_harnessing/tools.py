"""Kubernetes tools. kubectl is common; cloud CLIs only refresh kubeconfig."""

from __future__ import annotations

from typing import Any

from enterprise_it_harnessing.shared.auth import detect_provider, resolve_identity
from enterprise_it_harnessing.shared.cli import run_argv
from enterprise_it_harnessing.shared.providers import aws, azure, gcp

MUTATING = {"kube_refresh_credentials", "kube_rollout_restart"}


def kube_get(inp: dict[str, Any]) -> str:
    argv = ["kubectl", "get", inp["resource"]]
    if inp.get("namespace"):
        argv.extend(["-n", inp["namespace"]])
    if inp.get("context"):
        argv.extend(["--context", inp["context"]])
    argv.extend(["-o", inp.get("output", "wide")])
    return run_argv(argv)


def kube_describe(inp: dict[str, Any]) -> str:
    argv = ["kubectl", "describe", inp["resource"], inp.get("name", "")]
    argv = [part for part in argv if part]
    if inp.get("namespace"):
        argv.extend(["-n", inp["namespace"]])
    if inp.get("context"):
        argv.extend(["--context", inp["context"]])
    return run_argv(argv)


def kube_logs(inp: dict[str, Any]) -> str:
    argv = ["kubectl", "logs", inp["name"], "--tail", str(inp.get("tail", 200))]
    if inp.get("namespace"):
        argv.extend(["-n", inp["namespace"]])
    if inp.get("context"):
        argv.extend(["--context", inp["context"]])
    return run_argv(argv)


def kube_refresh_credentials(inp: dict[str, Any]) -> str:
    cluster = inp["cluster"]
    identity = resolve_identity()
    provider = detect_provider()
    if provider == "aws":
        return run_argv(aws.eks_update_kubeconfig(cluster, identity.region))
    if provider == "azure":
        return run_argv(azure.aks_credentials(cluster, inp.get("resource_group", "")))
    if provider == "gcp":
        return run_argv(gcp.gke_credentials(cluster, inp.get("region") or identity.region))
    return run_argv(["echo", f"on-prem: use existing kubeconfig context for {cluster}"])


def kube_rollout_restart(inp: dict[str, Any]) -> str:
    argv = ["kubectl", "rollout", "restart", inp["resource"]]
    if inp.get("namespace"):
        argv.extend(["-n", inp["namespace"]])
    if inp.get("context"):
        argv.extend(["--context", inp["context"]])
    return run_argv(argv)


TOOLS = [
    {
        "name": "kube_get",
        "description": "Read-only kubectl get. Always pass context for prod clusters.",
        "input_schema": {
            "type": "object",
            "properties": {
                "resource": {"type": "string"},
                "namespace": {"type": "string"},
                "context": {"type": "string"},
                "output": {"type": "string"},
            },
            "required": ["resource"],
        },
    },
    {
        "name": "kube_describe",
        "description": "kubectl describe a named object.",
        "input_schema": {
            "type": "object",
            "properties": {
                "resource": {"type": "string"},
                "name": {"type": "string"},
                "namespace": {"type": "string"},
                "context": {"type": "string"},
            },
            "required": ["resource"],
        },
    },
    {
        "name": "kube_logs",
        "description": "Fetch pod logs. Use a subagent mentally: return a summary, not a novel.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "namespace": {"type": "string"},
                "context": {"type": "string"},
                "tail": {"type": "integer"},
            },
            "required": ["name"],
        },
    },
    {
        "name": "kube_refresh_credentials",
        "description": "Refresh kubeconfig via EKS, AKS, GKE, or leave on-prem context as-is.",
        "input_schema": {
            "type": "object",
            "properties": {
                "cluster": {"type": "string"},
                "resource_group": {"type": "string"},
                "region": {"type": "string"},
            },
            "required": ["cluster"],
        },
    },
    {
        "name": "kube_rollout_restart",
        "description": "Rollout restart a workload. Requires approval.",
        "input_schema": {
            "type": "object",
            "properties": {
                "resource": {"type": "string"},
                "namespace": {"type": "string"},
                "context": {"type": "string"},
            },
            "required": ["resource"],
        },
    },
]

DISPATCH = {
    "kube_get": kube_get,
    "kube_describe": kube_describe,
    "kube_logs": kube_logs,
    "kube_refresh_credentials": kube_refresh_credentials,
    "kube_rollout_restart": kube_rollout_restart,
}
