# How To Use — Kubernetes

Catalog / playbooks: `./harness-k8s.sh`. Jobs (15, skill + hooks): `./harness-k8s-job.sh` — [HowToUse_K8s_Jobs.md](HowToUse_K8s_Jobs.md).

`repl` opens a session. Playbooks print and exit unless you add `--interactive`.

| Command | Output | When to use |
| --- | --- | --- |
| `./harness-k8s.sh` | Command names only | See every K8s command |
| `./harness-k8s.sh repl` | `k8s >>` prompt | Empty cluster session |
| `./harness-k8s.sh identity` | Cloud identity JSON | Same dump, no model |
| `./harness-k8s.sh skills` | cluster-context, crashloop | See K8s runbooks |
| `./harness-k8s.sh list-units` | BUs → cluster names | Which kubeconfig |
| `./harness-k8s.sh list-forex-markets` | FOREX markets workloads | FOREX inventory |
| `./harness-k8s.sh list-shopify-merchants` | Shopify workloads | Shopify inventory |
| `./harness-k8s.sh pods-forex-markets` | Pods on `eks-forex-markets-prod` | Matching / FIX not Ready |
| `./harness-k8s.sh pods-forex-settlement` | Pods for risk / CLS | Settlement not Ready |
| `./harness-k8s.sh pods-ecom-retail` | Pods for catalog / orders / checkout | Retail not Ready |
| `./harness-k8s.sh pods-ecom-quote` | Pods for B2B quote | Quote not Ready |
| `./harness-k8s.sh pods-fulfillment` | Pods on `gke-fulfillment-prod` | WMS / shipping not Ready |
| `./harness-k8s.sh pods-customer-profile` | Pods for identity / profile | Profile not Ready |
| `./harness-k8s.sh pods-customer-support` | Pods for tickets / chat | Support not Ready |
| `./harness-k8s.sh pods-customer-advisor` | Pods for advisor desktop | Advisor not Ready |
| `./harness-k8s.sh pods-product-research` | Pods for assortment | Research not Ready |
| `./harness-k8s.sh pods-shopify-merchants` | Pods for webhooks / legacy | Shopify not Ready |
| `./harness-k8s.sh describe-fx-matching` | Deploy describe; crashloop if CrashLoopBackOff | Matching pod bad |
| `./harness-k8s.sh describe-shopify-webhooks` | Deploy describe for HMAC ingress | HMAC pod bad |
| `./harness-k8s.sh describe-orders-api` | Deploy describe for orders-api | Orders pod bad |
| `./harness-k8s.sh logs-fx-matching` | Matching-engine logs (rejects) | Why matching is rejecting |
| `./harness-k8s.sh logs-shopify-webhooks` | HMAC ingress logs | Why HMAC is failing |
| `./harness-k8s.sh logs-legacy-bridge` | SOAP / AS/400 timeouts | Legacy bridge down |
| `./harness-k8s.sh logs-checkout` | Checkout saga logs | Stuck checkout |
| `./harness-k8s.sh creds-forex-markets` | EKS kubeconfig refresh (asks for approval) | Stale FOREX context |
| `./harness-k8s.sh creds-ecom-retail` | AKS kubeconfig refresh (asks for approval) | Stale retail context |
| `./harness-k8s.sh creds-fulfillment` | GKE kubeconfig refresh (asks for approval) | Stale fulfillment context |
| `./harness-k8s.sh creds-shopify` | EKS kubeconfig refresh (asks for approval) | Stale Shopify context |
| `./harness-k8s.sh restart-shopify-retry` | Restart proposal (asks for approval) | Webhook-retry stuck |
| `./harness-k8s.sh restart-fx-session` | Restart proposal (asks for approval) | Session-manager stuck; avoid peak |
