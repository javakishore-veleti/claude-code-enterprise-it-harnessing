"""AWS CLI argv for shared semantic operations."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone


def rds_describe(instance: str) -> list[str]:
    return ["aws", "rds", "describe-db-instances", "--db-instance-identifier", instance]


def rds_replica_lag(instance: str) -> list[str]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=10)
    return [
        "aws",
        "cloudwatch",
        "get-metric-statistics",
        "--namespace",
        "AWS/RDS",
        "--metric-name",
        "ReplicaLag",
        "--dimensions",
        f"Name=DBInstanceIdentifier,Value={instance}",
        "--start-time",
        start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "--end-time",
        end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "--period",
        "60",
        "--statistics",
        "Maximum",
        "Average",
        "--output",
        "json",
    ]


def rds_snapshots(instance: str) -> list[str]:
    return ["aws", "rds", "describe-db-snapshots", "--db-instance-identifier", instance]


def rds_snapshot(instance: str, snapshot_id: str) -> list[str]:
    return ["aws", "rds", "create-db-snapshot", "--db-instance-identifier", instance, "--db-snapshot-identifier", snapshot_id]


def msk_clusters() -> list[str]:
    return ["aws", "kafka", "list-clusters", "--output", "json"]


def elasticache_describe(cache_id: str) -> list[str]:
    return ["aws", "elasticache", "describe-cache-clusters", "--cache-cluster-id", cache_id, "--show-cache-node-info"]


def eks_update_kubeconfig(cluster: str, region: str) -> list[str]:
    argv = ["aws", "eks", "update-kubeconfig", "--name", cluster]
    if region:
        argv.extend(["--region", region])
    return argv


def cloudwatch_alarms(service: str) -> list[str]:
    return ["aws", "cloudwatch", "describe-alarms", "--alarm-name-prefix", service]
