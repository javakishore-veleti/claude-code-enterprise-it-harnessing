# How To Use — SRE

`--interactive` is optional. Omit it to print and exit.

| Command | Output | When to use |
| --- | --- | --- |
| `./harness-sre.sh` | npm script list | See every SRE command |
| `./harness-sre.sh repl` | Cloud identity JSON | Confirm who you are; no session |
| `./harness-sre.sh repl --interactive` | `sre >>` prompt | Empty SRE session |
| `./harness-sre.sh identity` | Cloud identity JSON | Same dump, no model |
| `./harness-sre.sh skills` | incident-response, deploy-rollback | See SRE runbooks |
| `./harness-sre.sh list-units` | 10 BUs, accounts, clusters | Estate map |
| `./harness-sre.sh list-forex-markets` | 10 FOREX markets services | FOREX markets inventory |
| `./harness-sre.sh list-forex-settlement` | Risk, CLS, regulatory services | FOREX settlement inventory |
| `./harness-sre.sh list-ecommerce-retail` | Catalog, cart, orders, checkout | Retail e-com inventory |
| `./harness-sre.sh list-ecommerce-quote` | B2B quote / contract services | Quote inventory |
| `./harness-sre.sh list-fulfillment` | WMS, shipping, tracking | Fulfillment inventory |
| `./harness-sre.sh list-customer-profile` | Identity, consent, loyalty | Profile inventory |
| `./harness-sre.sh list-customer-support` | Tickets, SLA, chat | Support inventory |
| `./harness-sre.sh list-customer-advisor` | Advisor desktop / NBA | Advisor inventory |
| `./harness-sre.sh list-product-research` | Assortment / research | Research inventory |
| `./harness-sre.sh list-shopify-merchants` | Webhooks + legacy bridge | Shopify inventory |
| `./harness-sre.sh resolve-fx-matching` | Account/cluster for `fx-matching-engine` | Before observing matching |
| `./harness-sre.sh resolve-shopify-webhooks` | Account/cluster for HMAC ingress | Before observing Shopify |
| `./harness-sre.sh resolve-orders-api` | Account/cluster for `orders-api` | Before observing orders |
| `./harness-sre.sh observe-fx-matching` | Health / alarms for matching-engine | Reject-rate / Sev2 |
| `./harness-sre.sh observe-fx-fix-gateway` | FIX session health | FIX drops |
| `./harness-sre.sh observe-orders-api` | Orders API health | Orders SLO |
| `./harness-sre.sh observe-checkout` | Checkout saga health | Stuck checkout |
| `./harness-sre.sh observe-shopify-webhooks` | HMAC ingress health | HMAC failures |
| `./harness-sre.sh observe-shopify-legacy` | SOAP / AS/400 bridge health | Legacy sync down |
| `./harness-sre.sh observe-ticket-api` | Ticket API health | Support SLO |
| `./harness-sre.sh logs-fx-matching` | Pointer to FOREX ELK index | Matching rejects in logs |
| `./harness-sre.sh logs-shopify-webhooks` | Pointer to Shopify HMAC index | HMAC failures in logs |
| `./harness-sre.sh incident-forex-matching` | Detect / contain matching reject spike | Sev loop; no rollback yet |
| `./harness-sre.sh incident-shopify-hmac` | Detect / contain HMAC failures | Bound to shopify-merchants |
| `./harness-sre.sh incident-orders-saga` | Detect / contain stuck checkout | After payments-adapter |
| `./harness-sre.sh rollback-fx-matching` | Rollback proposal (asks for approval) | After contain, before mutate |
