"""Cloud identity resolution. Operations stay common; only auth differs (AWS / Azure / GCP)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import asdict, dataclass
from typing import Literal

Provider = Literal["aws", "azure", "gcp", "none"]


@dataclass(frozen=True)
class CloudIdentity:
    provider: Provider
    principal: str
    account: str
    region: str
    method: str

    def as_json(self) -> str:
        return json.dumps(asdict(self))


def detect_provider() -> Provider:
    explicit = os.getenv("CLOUD_PROVIDER", "").strip().lower()
    if explicit in ("aws", "azure", "gcp"):
        return explicit  # type: ignore[return-value]
    if os.getenv("AWS_PROFILE") or os.getenv("AWS_ACCESS_KEY_ID") or os.getenv("AWS_REGION"):
        return "aws"
    if os.getenv("AZURE_SUBSCRIPTION_ID") or os.getenv("ARM_SUBSCRIPTION_ID"):
        return "azure"
    if os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("CLOUDSDK_CORE_PROJECT"):
        return "gcp"
    return "none"


def resolve_identity(provider: Provider | None = None) -> CloudIdentity:
    chosen = provider or detect_provider()
    if chosen == "aws":
        return _aws_identity()
    if chosen == "azure":
        return _azure_identity()
    if chosen == "gcp":
        return _gcp_identity()
    return CloudIdentity("none", "local", "local", "", "env")


def _probe(argv: list[str], timeout: int = 20) -> str:
    if not shutil.which(argv[0]):
        return ""
    try:
        result = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip() if result.returncode == 0 else ""
    except OSError:
        return ""


def _aws_identity() -> CloudIdentity:
    raw = _probe(["aws", "sts", "get-caller-identity", "--output", "json"])
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or ""
    method = "aws-profile" if os.getenv("AWS_PROFILE") else "aws-env"
    if not raw:
        return CloudIdentity("aws", os.getenv("AWS_PROFILE", "unauthenticated"), "", region, method)
    data = json.loads(raw)
    return CloudIdentity("aws", data.get("Arn", ""), data.get("Account", ""), region, method)


def _azure_identity() -> CloudIdentity:
    raw = _probe(["az", "account", "show", "--output", "json"])
    if not raw:
        return CloudIdentity(
            "azure",
            os.getenv("AZURE_CLIENT_ID", "unauthenticated"),
            os.getenv("AZURE_SUBSCRIPTION_ID", ""),
            os.getenv("AZURE_DEFAULT_LOCATION", ""),
            "az-login-or-managed-identity",
        )
    data = json.loads(raw)
    user = (data.get("user") or {}).get("name", "")
    return CloudIdentity("azure", user, data.get("id", ""), data.get("location", "") or "", "az-account")


def _gcp_identity() -> CloudIdentity:
    account = _probe(["gcloud", "config", "get-value", "account"])
    project = (
        os.getenv("GOOGLE_CLOUD_PROJECT")
        or os.getenv("CLOUDSDK_CORE_PROJECT")
        or _probe(["gcloud", "config", "get-value", "project"])
    )
    region = os.getenv("CLOUDSDK_COMPUTE_REGION") or ""
    method = "adc" if os.getenv("GOOGLE_APPLICATION_CREDENTIALS") else "gcloud-adc"
    return CloudIdentity("gcp", account or "unauthenticated", project, region, method)
