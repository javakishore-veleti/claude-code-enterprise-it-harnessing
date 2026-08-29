---
name: grafana-alerts
description: Grafana dashboards and silences per business-unit folder.
---

Folders follow the catalog: `grafana-forex-prod`, `grafana-ecom-prod`, `grafana-customer-prod`, `grafana-shopify-prod`.

1. `grafana_list_dashboards` with the business unit before searching by name.
2. `grafana_list_alerts` next. Name the firing rule and the microservice.
3. `grafana_silence_alert` requires approval and a reason.
4. Never silence:
   - `fx-matching-engine` reject-rate
   - `fx-cls-adapter` settlement failures
   - `shopify-webhook-ingress` HMAC failures
   unless a named incident commander is on the call.
