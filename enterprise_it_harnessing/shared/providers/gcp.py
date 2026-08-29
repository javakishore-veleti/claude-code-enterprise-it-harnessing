"""gcloud argv for shared semantic operations."""

from __future__ import annotations


def sql_describe(instance: str) -> list[str]:
    return ["gcloud", "sql", "instances", "describe", instance, "--format=json"]


def sql_backups(instance: str) -> list[str]:
    return ["gcloud", "sql", "backups", "list", "--instance", instance, "--format=json"]


def pubsub_topics() -> list[str]:
    return ["gcloud", "pubsub", "topics", "list", "--format=json"]


def memorystore_describe(instance: str, region: str) -> list[str]:
    argv = ["gcloud", "redis", "instances", "describe", instance, "--format=json"]
    if region:
        argv.extend(["--region", region])
    return argv


def gke_credentials(cluster: str, region: str) -> list[str]:
    argv = ["gcloud", "container", "clusters", "get-credentials", cluster]
    if region:
        argv.extend(["--region", region])
    return argv


def monitoring_uptime(service: str) -> list[str]:
    return ["gcloud", "monitoring", "uptime", "list-configs", "--filter", f"displayName:{service}", "--format=json"]
