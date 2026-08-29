"""Azure CLI argv for shared semantic operations."""

from __future__ import annotations


def sql_show(name: str, resource_group: str) -> list[str]:
    return ["az", "sql", "server", "show", "--name", name, "--resource-group", resource_group]


def sql_replica_lag(name: str, resource_group: str) -> list[str]:
    return [
        "az",
        "monitor",
        "metrics",
        "list",
        "--resource-group",
        resource_group,
        "--resource",
        name,
        "--resource-type",
        "Microsoft.Sql/servers",
        "--metric",
        "replica_info",
        "--interval",
        "PT1M",
        "--output",
        "json",
    ]


def sql_list_backups(name: str, resource_group: str) -> list[str]:
    return ["az", "sql", "db", "lts-policy", "show", "--server", name, "--resource-group", resource_group, "--name", "master"]


def eventhubs_list(resource_group: str) -> list[str]:
    return ["az", "eventhubs", "namespace", "list", "--resource-group", resource_group]


def redis_show(name: str, resource_group: str) -> list[str]:
    return ["az", "redis", "show", "--name", name, "--resource-group", resource_group]


def aks_credentials(cluster: str, resource_group: str) -> list[str]:
    return ["az", "aks", "get-credentials", "--name", cluster, "--resource-group", resource_group, "--overwrite-existing"]


def monitor_metrics(resource_id: str) -> list[str]:
    return ["az", "monitor", "metrics", "list", "--resource", resource_id]
