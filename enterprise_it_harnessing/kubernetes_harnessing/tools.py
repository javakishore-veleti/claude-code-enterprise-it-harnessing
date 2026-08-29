"""Kubernetes tools scoped to each business unit's dedicated cluster and namespace."""

from __future__ import annotations

import json
from typing import Any

from enterprise_it_harnessing.catalog import BUSINESS_UNITS, SERVICES
from enterprise_it_harnessing.shared.auth import resolve_identity
from enterprise_it_harnessing.shared.cli import run_argv
from enterprise_it_harnessing.shared.providers import aws, azure, gcp

MUTATING = {"kube_refresh_credentials", "kube_rollout_restart"}


def _scope(inp: dict[str, Any]) -> dict[str, str]:
    if inp.get("service") and inp["service"] in SERVICES:
        svc = SERVICES[inp["service"]]
        return {
            "context": svc["cluster"],
            "namespace": svc["business_unit"],
            "cloud": svc["cloud"],
            "account": svc["account"],
            "workload": f"deploy/{svc['service']}",
            "service": svc["service"],
        }
    if inp.get("business_unit") and inp["business_unit"] in BUSINESS_UNITS:
        u = BUSINESS_UNITS[inp["business_unit"]]
        return {
            "context": u["cluster"],
            "namespace": inp["business_unit"],
            "cloud": u["cloud"],
            "account": u["account"],
            "workload": inp.get("resource", "deploy"),
            "service": "",
        }
    return {
        "context": inp.get("context") or "",
        "namespace": inp.get("namespace") or "",
        "cloud": "",
        "account": "",
        "workload": inp.get("resource", "pods"),
        "service": "",
    }


def kube_get(inp: dict[str, Any]) -> str:
    scope = _scope(inp)
    resource = inp.get("resource") or ("pods" if not scope["service"] else f"deploy/{scope['service']}")
    argv = ["kubectl", "get", resource, "-o", inp.get("output", "wide")]
    if scope["namespace"]:
        argv.extend(["-n", scope["namespace"]])
    if scope["context"]:
        argv.extend(["--context", scope["context"]])
    return json.dumps({"scope": scope, "result": run_argv(argv)}, default=str)


def kube_describe(inp: dict[str, Any]) -> str:
    scope = _scope(inp)
    resource = inp.get("resource") or "deploy"
    name = inp.get("name") or scope["service"]
    argv = ["kubectl", "describe", resource]
    if name:
        argv.append(name)
    if scope["namespace"]:
        argv.extend(["-n", scope["namespace"]])
    if scope["context"]:
        argv.extend(["--context", scope["context"]])
    return json.dumps({"scope": scope, "result": run_argv(argv)}, default=str)


def kube_logs(inp: dict[str, Any]) -> str:
    scope = _scope(inp)
    name = inp.get("name") or scope["service"]
    argv = ["kubectl", "logs", f"deploy/{name}", "--tail", str(inp.get("tail", 200))]
    if scope["namespace"]:
        argv.extend(["-n", scope["namespace"]])
    if scope["context"]:
        argv.extend(["--context", scope["context"]])
    return json.dumps({"scope": scope, "result": run_argv(argv)}, default=str)


def kube_refresh_credentials(inp: dict[str, Any]) -> str:
    scope = _scope(inp)
    cluster = inp.get("cluster") or scope["context"]
    identity = resolve_identity()
    cloud = scope["cloud"] or identity.provider
    if cloud == "aws":
        raw = run_argv(aws.eks_update_kubeconfig(cluster, identity.region))
    elif cloud == "azure":
        raw = run_argv(azure.aks_credentials(cluster, inp.get("resource_group", scope.get("namespace", ""))))
    elif cloud == "gcp":
        raw = run_argv(gcp.gke_credentials(cluster, inp.get("region") or identity.region))
    else:
        raw = run_argv(["echo", f"on-prem kubeconfig context for {cluster}"])
    return json.dumps({"scope": scope, "cluster": cluster, "result": raw}, default=str)


def kube_rollout_restart(inp: dict[str, Any]) -> str:
    scope = _scope(inp)
    resource = inp.get("resource") or scope["workload"]
    argv = ["kubectl", "rollout", "restart", resource]
    if scope["namespace"]:
        argv.extend(["-n", scope["namespace"]])
    if scope["context"]:
        argv.extend(["--context", scope["context"]])
    return json.dumps({"scope": scope, "result": run_argv(argv)}, default=str)


TOOLS = [
    {
        "name": "kube_get",
        "description": "kubectl get on a catalogued service or business unit (auto-fills context/namespace: eks-forex-markets-prod / forex-markets).",
        "input_schema": {
            "type": "object",
            "properties": {
                "service": {"type": "string"},
                "business_unit": {"type": "string"},
                "resource": {"type": "string"},
                "namespace": {"type": "string"},
                "context": {"type": "string"},
                "output": {"type": "string"},
            },
        },
    },
    {
        "name": "kube_describe",
        "description": "Describe a workload. Pass service=fx-matching-engine or shopify-webhook-ingress.",
        "input_schema": {
            "type": "object",
            "properties": {
                "service": {"type": "string"},
                "business_unit": {"type": "string"},
                "resource": {"type": "string"},
                "name": {"type": "string"},
                "namespace": {"type": "string"},
                "context": {"type": "string"},
            },
        },
    },
    {
        "name": "kube_logs",
        "description": "Pod logs for a catalogued microservice. Summarize; do not dump novels.",
        "input_schema": {
            "type": "object",
            "properties": {
                "service": {"type": "string"},
                "name": {"type": "string"},
                "business_unit": {"type": "string"},
                "namespace": {"type": "string"},
                "context": {"type": "string"},
                "tail": {"type": "integer"},
            },
        },
    },
    {
        "name": "kube_refresh_credentials",
        "description": "Refresh kubeconfig for a BU cluster (EKS forex/Shopify, AKS e-com/support, GKE fulfillment/research).",
        "input_schema": {
            "type": "object",
            "properties": {
                "business_unit": {"type": "string"},
                "cluster": {"type": "string"},
                "resource_group": {"type": "string"},
                "region": {"type": "string"},
            },
        },
    },
    {
        "name": "kube_rollout_restart",
        "description": "Rollout restart a named microservice. Requires approval. Avoid during FOREX matching-engine peak or Shopify flash sales.",
        "input_schema": {
            "type": "object",
            "properties": {
                "service": {"type": "string"},
                "business_unit": {"type": "string"},
                "resource": {"type": "string"},
                "namespace": {"type": "string"},
                "context": {"type": "string"},
            },
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
