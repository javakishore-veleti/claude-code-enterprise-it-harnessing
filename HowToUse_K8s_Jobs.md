# How To Use — Kubernetes jobs

`./harness-k8s-job.sh` is the **job** launcher. `./harness-k8s.sh` stays the catalog / playbook launcher. Existing commands are unchanged.

Each job injects its skill into Claude (`--with-skill`). Hooks stay in that role’s `permissions.yaml` (deny / allow / ask).

| Command | Job (what Claude follows) | When to use |
| --- | --- | --- |
| `./harness-k8s-job.sh` | Lists the 15 jobs | See every job |
| `./harness-k8s-job.sh crashloop-matching` | CrashLoop matching-engine | fx-matching-engine CrashLoopBackOff |
| `./harness-k8s-job.sh crashloop-hmac` | CrashLoop HMAC ingress | shopify-webhook-ingress looping |
| `./harness-k8s-job.sh oom-checkout` | OOM checkout-orchestrator | checkout pods OOMKilled |
| `./harness-k8s-job.sh imagepull-shopify` | ImagePullBackOff Shopify | webhook or retry cannot pull |
| `./harness-k8s-job.sh pending-fulfillment` | Pending pods fulfillment | gke-fulfillment-prod Pending |
| `./harness-k8s-job.sh creds-eks-forex` | Refresh EKS FOREX kubeconfig | stale eks-forex-markets-prod |
| `./harness-k8s-job.sh creds-aks-retail` | Refresh AKS retail kubeconfig | stale aks-ecom-retail-prod |
| `./harness-k8s-job.sh creds-gke-fulfillment` | Refresh GKE fulfillment kubeconfig | stale gke-fulfillment-prod |
| `./harness-k8s-job.sh restart-webhook-retry` | Restart Shopify webhook-retry | retry deploy stuck |
| `./harness-k8s-job.sh restart-session-mgr` | Restart FX session-manager | session-manager stuck |
| `./harness-k8s-job.sh logs-matching-rejects` | Matching-engine reject logs | why matching is rejecting |
| `./harness-k8s-job.sh logs-hmac` | HMAC ingress logs | why HMAC is failing |
| `./harness-k8s-job.sh logs-as400` | Legacy bridge SOAP/AS400 logs | on-prem timeouts |
| `./harness-k8s-job.sh pods-settlement-cls` | Settlement / CLS pods | forex-settlement not Ready |
| `./harness-k8s-job.sh describe-orders-api` | Describe orders-api | orders pod bad |

