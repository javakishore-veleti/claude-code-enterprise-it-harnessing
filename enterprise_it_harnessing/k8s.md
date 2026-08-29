# Kubernetes harness — command table

Use this profile on the **ten dedicated clusters**. Namespace equals the business-unit slug. Pass `service=` or `business_unit=` so context is filled (EKS FOREX/Shopify, AKS e-com/support/advisor, GKE fulfillment/research).

Folder: `enterprise_it_harnessing/kubernetes_harnessing/`  
Launcher: `./harness-k8s.sh <command>` from the repo root. Append `--interactive` on a playbook to keep that session open.

| Command | What it does | Cluster / namespace |
| --- | --- | --- |
| `./harness-k8s.sh` | List every K8s npm script | — |
| `./harness-k8s.sh repl --interactive` | Empty cluster-admin session | all 10 clusters |
| `./harness-k8s.sh identity` | Cloud principal (`--tool`) | current provider |
| `./harness-k8s.sh skills` | cluster-context, crashloop | — |
| `./harness-k8s.sh list-units` | BUs → cluster names | catalog |
| `./harness-k8s.sh list-forex-markets` | FOREX markets workloads | `eks-forex-markets-prod` |
| `./harness-k8s.sh list-shopify-merchants` | Shopify workloads | `eks-shopify-merchants-prod` |
| `./harness-k8s.sh pods-forex-markets` | `kubectl get pods` FOREX markets | `forex-markets` |
| `./harness-k8s.sh pods-forex-settlement` | Pods for risk / CLS | `forex-settlement` |
| `./harness-k8s.sh pods-ecom-retail` | Pods for catalog / orders / checkout | `ecommerce-retail` |
| `./harness-k8s.sh pods-ecom-quote` | Pods for B2B quote | `ecommerce-quote` |
| `./harness-k8s.sh pods-fulfillment` | Pods for WMS / shipping | `gke-fulfillment-prod` |
| `./harness-k8s.sh pods-customer-profile` | Pods for identity / profile | `customer-profile` |
| `./harness-k8s.sh pods-customer-support` | Pods for tickets / chat | `customer-support` |
| `./harness-k8s.sh pods-customer-advisor` | Pods for advisor desktop | `customer-advisor` |
| `./harness-k8s.sh pods-product-research` | Pods for assortment / research | `product-research` |
| `./harness-k8s.sh pods-shopify-merchants` | Pods for webhooks / legacy | `shopify-merchants` |
| `./harness-k8s.sh describe-fx-matching` | Describe matching-engine deploy | FOREX markets |
| `./harness-k8s.sh describe-shopify-webhooks` | Describe HMAC ingress | Shopify |
| `./harness-k8s.sh describe-orders-api` | Describe orders-api | retail e-com |
| `./harness-k8s.sh logs-fx-matching` | Matching-engine logs (summarize rejects) | FOREX |
| `./harness-k8s.sh logs-shopify-webhooks` | HMAC ingress logs | Shopify |
| `./harness-k8s.sh logs-legacy-bridge` | SOAP / AS/400 timeouts | `shopify-legacy-bridge` |
| `./harness-k8s.sh logs-checkout` | Checkout saga logs | `checkout-orchestrator` |
| `./harness-k8s.sh creds-forex-markets` | Refresh EKS kubeconfig (approval) | FOREX markets |
| `./harness-k8s.sh creds-ecom-retail` | Refresh AKS kubeconfig (approval) | retail e-com |
| `./harness-k8s.sh creds-fulfillment` | Refresh GKE kubeconfig (approval) | fulfillment |
| `./harness-k8s.sh creds-shopify` | Refresh EKS kubeconfig (approval) | Shopify |
| `./harness-k8s.sh restart-shopify-retry` | Propose restart of webhook-retry (approval) | Shopify |
| `./harness-k8s.sh restart-fx-session` | Propose restart of session-manager (approval) | FOREX |

Namespace / volume / node delete is denied. Avoid matching-engine restarts at peak.
