# SRE harness — command table

Use this profile when the incident is a **microservice SLO**: FOREX matching / FIX, checkout saga, Shopify HMAC webhooks, support tickets.

Folder: `enterprise_it_harnessing/sre_harnessing/`  
Launcher: `./harness-sre.sh <command>` from the repo root (forwards to that folder’s `package.json`). Append `--interactive` on a playbook to keep that session open.

Ten BUs, dedicated accounts. Always `list-units` or `resolve-*` before paging or rolling back. FOREX matching-engine and Shopify HMAC ingress are Sev2 by default.

| Command | What it does | Typical BU / service |
| --- | --- | --- |
| `./harness-sre.sh` | List every SRE npm script | — |
| `./harness-sre.sh repl --interactive` | Empty SRE session | all 10 BUs |
| `./harness-sre.sh identity` | Show cloud principal (`--tool`, no model) | current `CLOUD_PROVIDER` |
| `./harness-sre.sh skills` | List SRE runbooks | incident-response, deploy-rollback |
| `./harness-sre.sh list-units` | Sev2 names, pager, SLO, next observe/incident, blast radius | first page of an incident |
| `./harness-sre.sh list-forex-markets` | 10 FOREX markets services | `eks-forex-markets-prod` |
| `./harness-sre.sh list-forex-settlement` | Risk, CLS, regulatory | `eks-forex-settlement-prod` |
| `./harness-sre.sh list-ecommerce-retail` | Catalog, cart, orders, checkout | `aks-ecom-retail-prod` |
| `./harness-sre.sh list-ecommerce-quote` | B2B quote / contract | `aks-ecom-quote-prod` |
| `./harness-sre.sh list-fulfillment` | WMS, shipping, tracking | `gke-fulfillment-prod` |
| `./harness-sre.sh list-customer-profile` | Identity, consent, loyalty | `eks-customer-profile-prod` |
| `./harness-sre.sh list-customer-support` | Tickets, SLA, chat | `aks-customer-support-prod` |
| `./harness-sre.sh list-customer-advisor` | Advisor desktop / NBA | `aks-customer-advisor-prod` |
| `./harness-sre.sh list-product-research` | Assortment / catalog science | `gke-product-research-prod` |
| `./harness-sre.sh list-shopify-merchants` | Webhooks + legacy bridge | `eks-shopify-merchants-prod` |
| `./harness-sre.sh resolve-fx-matching` | Account/cluster for matching-engine | `fx-matching-engine` |
| `./harness-sre.sh resolve-shopify-webhooks` | Account/cluster for HMAC ingress | `shopify-webhook-ingress` |
| `./harness-sre.sh resolve-orders-api` | Account/cluster for orders | `orders-api` |
| `./harness-sre.sh observe-fx-matching` | Health / alarms for matching-engine | FOREX markets |
| `./harness-sre.sh observe-fx-fix-gateway` | FIX session health | FOREX markets |
| `./harness-sre.sh observe-orders-api` | Orders API health | retail e-com |
| `./harness-sre.sh observe-checkout` | Checkout saga health | `checkout-orchestrator` |
| `./harness-sre.sh observe-shopify-webhooks` | HMAC ingress health | Shopify merchants |
| `./harness-sre.sh observe-shopify-legacy` | On-prem SOAP / AS/400 bridge | `shopify-legacy-bridge` |
| `./harness-sre.sh observe-ticket-api` | Support ticket API | customer-support |
| `./harness-sre.sh logs-fx-matching` | Point at FOREX ELK index | `es-forex-prod` |
| `./harness-sre.sh logs-shopify-webhooks` | Point at Shopify HMAC index | `es-shopify-prod` |
| `./harness-sre.sh incident-forex-matching` | Sev loop for reject spike | matching-engine |
| `./harness-sre.sh incident-shopify-hmac` | Sev loop for HMAC failures | webhook-ingress |
| `./harness-sre.sh incident-orders-saga` | Sev loop for stuck checkout | orders + payments |
| `./harness-sre.sh rollback-fx-matching` | Propose rollback (approval) | `eks-forex-markets-prod` |

Equivalent npm (from `sre_harnessing/`): `npm run observe-fx-matching`.
