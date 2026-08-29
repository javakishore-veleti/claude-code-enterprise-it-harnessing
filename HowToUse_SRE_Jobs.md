# How To Use — SRE jobs

`./harness-sre-job.sh` is the **job** launcher. `./harness-sre.sh` stays the catalog / playbook launcher. Existing commands are unchanged.

Each job injects its skill into Claude (`--with-skill`). Hooks stay in that role’s `permissions.yaml` (deny / allow / ask).
Answers use **Input / What it is doing / What it found / Final output** (bullets + Summary). Token cost is printed from `model_costs.json`.

| Command | Job (what Claude follows) | When to use |
| --- | --- | --- |
| `./harness-sre-job.sh` | Lists the 15 jobs | See every job |
| `./harness-sre-job.sh matching-reject-spike` | FOREX matching reject spike | reject-rate up on fx-matching-engine |
| `./harness-sre-job.sh fix-session-drop` | FIX session drop | FIX 4.4/5.0 drops on fx-fix-gateway |
| `./harness-sre-job.sh cls-halt` | CLS / settlement halt | CLS adapter or netting stuck |
| `./harness-sre-job.sh checkout-saga-stuck` | Checkout saga stuck | saga stuck after payments-adapter |
| `./harness-sre-job.sh payments-decline-storm` | Payments decline storm | PSP declines spike |
| `./harness-sre-job.sh hmac-failure-storm` | Shopify HMAC failure storm | hmac_failed on webhook ingress |
| `./harness-sre-job.sh legacy-as400-timeout` | Shopify AS/400 / SOAP timeout | legacy bridge SOAP timeouts |
| `./harness-sre-job.sh ticket-sla-breach` | Support ticket SLA breach | ticket-api / sla-watchdog |
| `./harness-sre-job.sh quote-to-order-break` | B2B quote-to-order break | accepted quote not becoming an order |
| `./harness-sre-job.sh fulfillment-allocation-stall` | Fulfillment allocation stall | WMS / allocation-engine not allocating |
| `./harness-sre-job.sh consent-write-fail` | Consent ledger write fail | GDPR / consent-ledger writes failing |
| `./harness-sre-job.sh matching-rollback` | Matching-engine rollback | error stepped at a FOREX release |
| `./harness-sre-job.sh page-forex-oncall` | Page FOREX markets on-call | need forex-markets-sre paged |
| `./harness-sre-job.sh bound-shopify-blast` | Bound Shopify blast radius | Shopify incident must not leave that account |
| `./harness-sre-job.sh idempotency-replay` | Shopify idempotency replay | duplicate webhooks / idemp keys |

