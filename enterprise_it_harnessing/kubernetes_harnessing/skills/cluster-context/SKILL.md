---
name: cluster-context
description: Refresh and verify kubeconfig for on-prem, EKS, AKS, or GKE.
---

The cluster API is the same. Only how you obtain a token changes.

1. `cloud_identity` — confirm the cloud principal matches the cluster you think you are on.
2. `kube_refresh_credentials` for EKS/AKS/GKE. On-prem, do not overwrite kubeconfig.
3. `kube_get nodes` with an explicit context.
4. If nodes do not match the expected pool size or version, stop. You are in the wrong cluster.
