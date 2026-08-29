#!/usr/bin/env python3
"""Generate *-job.sh launchers, 15 skills + npm scripts per role. Does not touch existing harness-*.sh."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENT = Path(__file__).resolve().parent

# slug, title, when, prompt, skill body (after frontmatter)
ROLES: dict[str, dict] = {
    "sre": {
        "folder": "sre_harnessing",
        "harness": "enterprise_it_harnessing/sre_harnessing/harness.py",
        "launcher": "harness-sre-job.sh",
        "howto": "HowToUse_SRE_Jobs.md",
        "title": "SRE jobs",
        "prompt_name": "sre-job",
        "jobs": [
            ("matching-reject-spike", "FOREX matching reject spike", "reject-rate up on fx-matching-engine",
             "Sev2 matching-engine reject spike. resolve_service fx-matching-engine, observe_health, fetch_logs. Contain. Do not rollback yet.",
             "Sev2. Bound to forex-markets / eks-forex-markets-prod.\n1. resolve_service fx-matching-engine\n2. observe_health\n3. fetch_logs\n4. Contain. page_oncall and rollback_deploy need approval.\nDo not page CLS. Do not touch shopify-merchants."),
            ("fix-session-drop", "FIX session drop", "FIX 4.4/5.0 drops on fx-fix-gateway",
             "FIX session drops on fx-fix-gateway. resolve + observe_health. Report session resets. Do not restart matching at peak.",
             "FOREX bank FIX layer. Bound to forex-markets.\n1. resolve_service fx-fix-gateway\n2. observe_health — session drops\n3. fetch_logs — disconnect\nDo not restart fx-matching-engine at peak."),
            ("cls-halt", "CLS / settlement halt", "CLS adapter or netting stuck",
             "FOREX settlement / CLS at risk. Observe fx-cls-adapter and fx-risk-limits. Pause CLS before any failover. Do not touch matching-engine.",
             "forex-settlement only. CLS before risk-DB or cache failover.\n1. resolve fx-cls-adapter, fx-risk-limits\n2. observe_health\n3. Do not page matching-engine unless rejects are also up."),
            ("checkout-saga-stuck", "Checkout saga stuck", "saga stuck after payments-adapter",
             "Checkout saga stuck after payments-adapter. Observe checkout-orchestrator and orders-api. Do not rewind the saga.",
             "ecommerce-retail. Double-charge if you rewind ecom.checkout.saga.\n1. resolve checkout-orchestrator, orders-api, payments-adapter\n2. observe_health\n3. Contain. No saga rewind."),
            ("payments-decline-storm", "Payments decline storm", "PSP declines spike",
             "payments-adapter decline storm. Observe checkout-orchestrator. Do not rewind ecom.checkout.saga. Bound to ecommerce-retail.",
             "PSP path. Same blast radius as checkout.\n1. resolve payments-adapter\n2. observe_health\n3. Do not rewind the saga. Do not failover cart Redis without pausing checkout."),
            ("hmac-failure-storm", "Shopify HMAC failure storm", "hmac_failed on webhook ingress",
             "Shopify HMAC failures Sev2. resolve shopify-webhook-ingress. Bound blast to shopify-merchants. Do not silence HMAC alerts.",
             "Sev2. shopify-merchants / eks-shopify-merchants-prod only.\n1. resolve shopify-webhook-ingress\n2. observe_health, fetch_logs hmac_failed\n3. Do not page FOREX. Do not silence HMAC Grafana rules."),
            ("legacy-as400-timeout", "Shopify AS/400 / SOAP timeout", "legacy bridge SOAP timeouts",
             "shopify-legacy-bridge SOAP/AS400 timeouts. Observe bridge. Bound to shopify-merchants. Do not restart matching.",
             "On-prem SOAP / AS400. shopify-merchants only.\n1. resolve shopify-legacy-bridge\n2. observe_health, fetch_logs soap/as400\n3. Do not FLUSHALL idempotency Redis."),
            ("ticket-sla-breach", "Support ticket SLA breach", "ticket-api / sla-watchdog",
             "ticket-api SLA breach. Observe ticket-api. Bound to customer-support. Not a FOREX Sev2 unless matching is also down.",
             "customer-support. SLA clocks on azurecache-support.\n1. resolve ticket-api, sla-watchdog\n2. observe_health\n3. Do not page forex-markets-sre."),
            ("quote-to-order-break", "B2B quote-to-order break", "accepted quote not becoming an order",
             "quote-to-order broken. Observe quote-api and quote-to-order. Bound to ecommerce-quote.",
             "B2B quote path. aks-ecom-quote-prod.\n1. resolve quote-api, quote-to-order\n2. observe_health\n3. Do not mutate FOREX or Shopify."),
            ("fulfillment-allocation-stall", "Fulfillment allocation stall", "WMS / allocation-engine not allocating",
             "allocation-engine stall on gke-fulfillment-prod. Observe allocation-engine and tracking-api. Bound to fulfillment.",
             "GCP fulfillment. Dedicated GKE.\n1. resolve allocation-engine, tracking-api\n2. observe_health\n3. Do not drain FOREX EKS."),
            ("consent-write-fail", "Consent ledger write fail", "GDPR / consent-ledger writes failing",
             "consent-ledger write failures. Observe identity-service and consent-ledger. Bound to customer-profile.",
             "GDPR writes. customer-profile only.\n1. resolve consent-ledger, identity-service\n2. observe_health\n3. Do not DROP or TRUNCATE. DBA harness for the instance."),
            ("matching-rollback", "Matching-engine rollback", "error stepped at a FOREX release",
             "Propose rollback_deploy of fx-matching-engine on eks-forex-markets-prod. Wait for approval. Re-observe after.",
             "Use only after contain. Approval required.\n1. Confirm revision / last-known-good\n2. rollback_deploy only after operator yes\n3. observe_health after. Do not fix-forward from this harness."),
            ("page-forex-oncall", "Page FOREX markets on-call", "need forex-markets-sre paged",
             "Page forex-markets-sre for fx-matching-engine. page_oncall needs approval. Do not page shopify-merchants-sre.",
             "Pager is {bu}-sre. Wrong pager is a failed job.\n1. resolve_service first\n2. page_oncall severity=sev2 after approval\n3. Matching and HMAC are Sev2 by default."),
            ("bound-shopify-blast", "Bound Shopify blast radius", "Shopify incident must not leave that account",
             "Shopify incident. Stay on aws-shopify-merchants-prod / eks-shopify-merchants-prod. Do not rollback or page FOREX.",
             "Dedicated account. HMAC + legacy only.\n1. resolve shopify-webhook-ingress\n2. Observe, contain inside shopify-merchants\n3. Never kubectl or rollback eks-forex-markets-prod."),
            ("idempotency-replay", "Shopify idempotency replay", "duplicate webhooks / idemp keys",
             "Duplicate Shopify webhooks. Observe shopify-idempotency and webhook-ingress. Freeze ingress before any Redis failover. Ask Redis harness for the cache.",
             "shopify:idemp:* keys. Replay = dual order write.\n1. resolve shopify-idempotency, shopify-webhook-ingress\n2. Observe. Freeze ingress before cache failover\n3. FLUSHALL is denied."),
        ],
    },
    "db": {
        "folder": "db_admin_harnessing",
        "harness": "enterprise_it_harnessing/db_admin_harnessing/harness.py",
        "launcher": "harness-db-job.sh",
        "howto": "HowToUse_DB_Jobs.md",
        "title": "DB jobs",
        "jobs": [
            ("trades-replica-lag", "FOREX trades replica lag", "rds-fx-trades-prod lag > 5s Sev2",
             "replication_lag rds-fx-trades-prod. Sev2 if > 5s. Trade capture / FIX / audit.",
             "Aurora trades. Lag hurts FIX audit.\n1. resolve_database rds-fx-trades-prod\n2. replication_lag\n3. Do not failover without a snapshot job."),
            ("risk-failover-pause-cls", "Risk DB failover after CLS pause", "rds-fx-risk-prod emergency",
             "Propose failover rds-fx-risk-prod. Pause fx-cls-adapter first. Approval required.",
             "CLS first, then promote.\n1. Confirm replica lag near zero\n2. Pause CLS\n3. failover only after approval. DROP DATABASE denied."),
            ("orders-snapshot-checkout", "Orders snapshot before checkout deploy", "azsql-orders-prod pre-release",
             "Load backup-restore. Propose create_snapshot azsql-orders-prod before checkout deploy. Approval required.",
             "Azure SQL orders. Snapshot before checkout train.\n1. list_backups\n2. create_snapshot after approval\n3. Do not snapshot during a stuck saga without the SRE."),
            ("shopify-sync-drain", "Shopify sync DB drain + failover", "rds-shopify-sync-prod",
             "Drain shopify-webhook-ingress, then propose failover rds-shopify-sync-prod. Approval required.",
             "Webhook inbox. Dual-write if you fail over hot.\n1. Drain ingress (SRE)\n2. list_backups\n3. failover after approval."),
            ("consent-ledger-check", "Consent ledger integrity", "rds-profile-prod consent writes",
             "describe_instance rds-profile-prod including consent-ledger. No DROP/TRUNCATE.",
             "GDPR ledger. Read-only describe.\n1. resolve rds-profile-prod\n2. describe_instance\n3. Mutations denied."),
            ("quotes-blocking", "B2B quotes blocking sessions", "azsql-quotes-prod locks",
             "describe_instance azsql-quotes-prod. Look for blocking on quote-to-order. No kill without approval.",
             "Contract pricing DB.\n1. describe_instance\n2. Report blockers\n3. No session kill from this harness without ask."),
            ("fulfillment-slow-query", "Fulfillment Cloud SQL slow query", "cloudsql-fulfillment-prod",
             "describe_instance cloudsql-fulfillment-prod. Allocation / WMS / tracking.",
             "GCP Cloud SQL. WMS path.\n1. describe_instance\n2. Do not vacuum/reindex without approval."),
            ("advisor-pii-access", "Advisor notes PII access check", "azsql-advisor-prod",
             "describe_instance azsql-advisor-prod (compliance notes). Do not dump note bodies.",
             "Regulated notes. Describe only.\n1. describe_instance\n2. Never SELECT * notes into the model."),
            ("support-ticket-db-lag", "Support tickets replica lag", "azsql-support-prod",
             "replication_lag azsql-support-prod. Ticket / SLA store.",
             "Support DB lag → SLA false breach.\n1. replication_lag\n2. Do not failover during a ticket flood without SRE."),
            ("research-restore-lab", "Research DB restore (lab)", "cloudsql-research-prod only",
             "Load backup-restore. Research only. Propose restore path for cloudsql-research-prod. FOREX/Shopify restore denied here.",
             "product-research only. FOREX and Shopify restores are out of this job.\n1. list_backups\n2. Propose restore after approval."),
            ("profile-backup-verify", "Profile / consent backup verify", "rds-profile-prod snapshots",
             "list_backups rds-profile-prod. Verify consent-ledger is in the snapshot set.",
             "Identity + consent.\n1. list_backups\n2. Report latest snapshot age."),
            ("trades-pre-fix-snapshot", "Trades snapshot before FIX release", "rds-fx-trades-prod pre-FIX",
             "Propose create_snapshot rds-fx-trades-prod before FIX release. Approval required.",
             "FIX release window.\n1. list_backups\n2. create_snapshot after approval\n3. Do not run during matching Sev2 without SRE."),
            ("orders-failover", "Orders DB failover", "azsql-orders-prod",
             "Propose failover azsql-orders-prod. Pause checkout-orchestrator first. Approval required.",
             "Checkout depends on this DB.\n1. Pause checkout (SRE)\n2. Confirm lag\n3. failover after approval."),
            ("shopify-inbox-bloat", "Shopify webhook inbox bloat", "rds-shopify-sync-prod growth",
             "describe_instance rds-shopify-sync-prod. Inbox / mapping growth. No DELETE of webhook rows.",
             "Inbox bloat ≠ TRUNCATE.\n1. describe_instance\n2. Report size\n3. DELETE/TRUNCATE denied."),
            ("netting-lock", "FOREX netting lock / risk DB", "rds-fx-risk-prod netting",
             "describe_instance rds-fx-risk-prod (limits, netting, CLS). Report lock notes. No failover in this job.",
             "Netting locks. Observe only in this job.\n1. describe_instance\n2. Use risk-failover-pause-cls to promote."),
        ],
    },
    "k8s": {
        "folder": "kubernetes_harnessing",
        "harness": "enterprise_it_harnessing/kubernetes_harnessing/harness.py",
        "launcher": "harness-k8s-job.sh",
        "howto": "HowToUse_K8s_Jobs.md",
        "title": "Kubernetes jobs",
        "jobs": [
            ("crashloop-matching", "CrashLoop matching-engine", "fx-matching-engine CrashLoopBackOff",
             "kube_describe fx-matching-engine. Load crashloop. Bound to eks-forex-markets-prod.",
             "FOREX matching pods.\n1. kube_describe service=fx-matching-engine\n2. If CrashLoopBackOff follow crashloop skill\n3. Do not delete the namespace."),
            ("crashloop-hmac", "CrashLoop HMAC ingress", "shopify-webhook-ingress looping",
             "kube_describe shopify-webhook-ingress. HMAC pod bad. Bound to eks-shopify-merchants-prod.",
             "Shopify ingress.\n1. kube_describe shopify-webhook-ingress\n2. crashloop if looping\n3. Do not restart matching."),
            ("oom-checkout", "OOM checkout-orchestrator", "checkout pods OOMKilled",
             "kube_describe checkout-orchestrator. Summarize OOM. Bound to aks-ecom-retail-prod.",
             "Checkout saga pods.\n1. kube_describe checkout-orchestrator\n2. Report OOM / restarts\n3. Scale requires approval."),
            ("imagepull-shopify", "ImagePullBackOff Shopify", "webhook or retry cannot pull",
             "kube_get / kube_describe shopify-webhook-retry ImagePullBackOff. Bound to shopify-merchants.",
             "Pull failures.\n1. kube_get pods shopify-merchants\n2. describe retry/ingress\n3. creds job if kubeconfig stale."),
            ("pending-fulfillment", "Pending pods fulfillment", "gke-fulfillment-prod Pending",
             "kube_get pods business_unit=fulfillment. Report Pending / unschedulable.",
             "GKE WMS.\n1. kube_get pods fulfillment\n2. Do not drain nodes without approval."),
            ("creds-eks-forex", "Refresh EKS FOREX kubeconfig", "stale eks-forex-markets-prod",
             "kube_refresh_credentials forex-markets (EKS). Approval required.",
             "cluster-context. EKS FOREX.\n1. Refresh after approval\n2. Then crashloop-matching if still needed."),
            ("creds-aks-retail", "Refresh AKS retail kubeconfig", "stale aks-ecom-retail-prod",
             "kube_refresh_credentials ecommerce-retail (AKS). Approval required.",
             "AKS retail.\n1. Refresh after approval\n2. Then oom-checkout / describe-orders-api."),
            ("creds-gke-fulfillment", "Refresh GKE fulfillment kubeconfig", "stale gke-fulfillment-prod",
             "kube_refresh_credentials fulfillment (GKE). Approval required.",
             "GKE fulfillment.\n1. Refresh after approval\n2. Then pending-fulfillment."),
            ("restart-webhook-retry", "Restart Shopify webhook-retry", "retry deploy stuck",
             "Propose kube_rollout_restart shopify-webhook-retry. Approval required.",
             "Shopify retry only.\n1. Describe first\n2. Restart after approval\n3. Avoid matching-engine."),
            ("restart-session-mgr", "Restart FX session-manager", "session-manager stuck",
             "Propose kube_rollout_restart fx-session-manager. Avoid matching-engine peak. Approval required.",
             "FOREX sessions. Not matching-engine.\n1. Avoid peak\n2. Restart after approval."),
            ("logs-matching-rejects", "Matching-engine reject logs", "why matching is rejecting",
             "kube_logs fx-matching-engine tail=200. Summarize rejects.",
             "Pod logs, then ELK for the index.\n1. kube_logs fx-matching-engine\n2. Point SRE/ELK for forex-trades."),
            ("logs-hmac", "HMAC ingress logs", "why HMAC is failing",
             "kube_logs shopify-webhook-ingress. Summarize hmac_failed.",
             "Shopify ingress logs.\n1. kube_logs shopify-webhook-ingress\n2. ELK alias shopify-webhooks."),
            ("logs-as400", "Legacy bridge SOAP/AS400 logs", "on-prem timeouts",
             "kube_logs shopify-legacy-bridge. SOAP/AS400 timeouts.",
             "Legacy bridge.\n1. kube_logs shopify-legacy-bridge\n2. Do not restart matching."),
            ("pods-settlement-cls", "Settlement / CLS pods", "forex-settlement not Ready",
             "kube_get pods business_unit=forex-settlement. CLS / risk / netting.",
             "Settlement cluster.\n1. kube_get forex-settlement\n2. Do not restart matching from here."),
            ("describe-orders-api", "Describe orders-api", "orders pod bad",
             "kube_describe service=orders-api. Retail e-com.",
             "orders-api on AKS retail.\n1. kube_describe orders-api\n2. crashloop if looping."),
        ],
    },
    "redis": {
        "folder": "redis_harnessing",
        "harness": "enterprise_it_harnessing/redis_harnessing/harness.py",
        "launcher": "harness-redis-job.sh",
        "howto": "HowToUse_Redis_Jobs.md",
        "title": "Redis jobs",
        "jobs": [
            ("fx-book-lag", "FX book replica lag", "elasticache-forex-quotes fx:book:*",
             "redis_info elasticache-forex-quotes section=replication. Stale book if lag > 2s.",
             "FOREX books. Stale book = bad fills.\n1. redis_info replication\n2. Sev if lag > 2s\n3. Failover is a different job."),
            ("fx-book-failover", "FX book failover", "promote FX quotes cache",
             "Propose redis_failover elasticache-forex-quotes. Matching-engine stale-book risk. Approval required.",
             "Replication skill. Approval.\n1. Confirm replica\n2. Failover after approval\n3. FLUSHALL denied."),
            ("cart-eviction", "Cart eviction storm", "azurecache-ecom-cart cart:*",
             "Load eviction. Cart memory pressure. Pause checkout if evicting cart:*.",
             "Checkout depends on carts.\n1. redis_info memory\n2. Pause checkout if evicting\n3. FLUSHALL denied."),
            ("cart-failover-pause", "Cart failover after checkout pause", "azurecache-ecom-cart",
             "Propose redis_failover azurecache-ecom-cart after pausing checkout-orchestrator. Approval required.",
             "Pause checkout first.\n1. SRE pause checkout\n2. Failover after approval."),
            ("shopify-idemp-freeze", "Freeze Shopify idemp before failover", "shopify:idemp:*",
             "redis_info elasticache-shopify-idempotency. Freeze webhook-ingress before any failover.",
             "Replay = dual orders.\n1. INFO keys\n2. Freeze ingress (SRE)\n3. Then shopify-idemp-failover."),
            ("shopify-idemp-failover", "Shopify idempotency failover", "elasticache-shopify-idempotency",
             "Propose redis_failover after freezing webhook-ingress. Approval required.",
             "Ingress frozen first.\n1. Confirm freeze\n2. Failover after approval."),
            ("risk-limits-memory", "FX risk limits memory", "elasticache-forex-risk fx:limit:*",
             "redis_info elasticache-forex-risk section=memory.",
             "Limit cache. Settlement path.\n1. redis_info memory\n2. Do not FLUSHALL."),
            ("quote-cache-hot", "B2B quote cache hot keys", "azurecache-ecom-quote quote:*",
             "redis_info azurecache-ecom-quote. Hot quote:* keys.",
             "Quote cache.\n1. redis_info\n2. Eviction skill if pressure."),
            ("fulfillment-lock-pileup", "Fulfillment alloc lock pile-up", "memorystore-fulfillment alloc:*",
             "redis_info memorystore-fulfillment section=clients. Allocation locks.",
             "GKE Memorystore.\n1. INFO clients\n2. Do not FLUSHALL locks."),
            ("session-clients", "Profile session client pile-up", "elasticache-profile-session sess:*",
             "redis_info elasticache-profile-session section=clients.",
             "Login sessions.\n1. INFO clients\n2. No FLUSHALL."),
            ("support-sla-clock", "Support SLA clock cache", "azurecache-support sla:*",
             "redis_info azurecache-support. SLA clocks.",
             "SLA false-breach if cache wrong.\n1. redis_info\n2. Coordinate ticket-sla SRE job."),
            ("advisor-presence", "Advisor presence cache", "azurecache-advisor adv:*",
             "redis_info azurecache-advisor.",
             "Advisor desktop presence.\n1. redis_info."),
            ("slowlog-fx", "SLOWLOG FX books", "slow FX Redis commands",
             "redis_slowlog elasticache-forex-quotes. Load eviction if needed.",
             "Slow book commands.\n1. redis_slowlog\n2. eviction if memory."),
            ("slowlog-cart", "SLOWLOG carts", "slow cart commands",
             "redis_slowlog azurecache-ecom-cart.",
             "Slow cart path.\n1. redis_slowlog\n2. Pause checkout if evicting."),
            ("slowlog-idemp", "SLOWLOG Shopify idemp", "slow idempotency commands",
             "redis_slowlog elasticache-shopify-idempotency.",
             "Slow idemp.\n1. redis_slowlog\n2. Do not FLUSHALL."),
        ],
    },
    "kafka": {
        "folder": "kafka_harnessing",
        "harness": "enterprise_it_harnessing/kafka_harnessing/harness.py",
        "launcher": "harness-kafka-job.sh",
        "howto": "HowToUse_Kafka_Jobs.md",
        "title": "Kafka / Event Bus jobs",
        "jobs": [
            ("lag-matching", "Matching-engine consumer lag", "fx.orders.routed / fx-matching-engine",
             "kafka_consumer_lag group=fx-matching-engine topic=fx.orders.routed.",
             "Matching input. Lag = rejects later.\n1. describe topic if needed\n2. consumer_lag\n3. Do not rewind FOREX."),
            ("lag-stp", "Bank STP consumer lag", "fx.trades.captured / fx-stp-adapter",
             "kafka_consumer_lag group=fx-stp-adapter topic=fx.trades.captured.",
             "STP to banks.\n1. consumer_lag\n2. Do not create FOREX topics."),
            ("lag-checkout-no-rewind", "Checkout saga lag — no rewind", "ecom.checkout.saga / payments-adapter",
             "kafka_consumer_lag group=payments-adapter topic=ecom.checkout.saga. Do not rewind.",
             "Rewind = double charge.\n1. consumer_lag\n2. Never rewind this topic."),
            ("lag-shopify-orders", "Shopify order webhook lag", "shopify.webhooks.orders",
             "kafka_consumer_lag group=shopify-order-sync topic=shopify.webhooks.orders.",
             "HMAC path lag → retry pile-up.\n1. consumer_lag\n2. Check shopify-idempotency Redis."),
            ("lag-shopify-products", "Shopify product webhook lag", "shopify.webhooks.products",
             "kafka_consumer_lag group=shopify-product-sync topic=shopify.webhooks.products.",
             "Product sync lag.\n1. consumer_lag."),
            ("lag-legacy-outbound", "Legacy outbound lag", "shopify.legacy.outbound",
             "kafka_consumer_lag group=shopify-fulfillment-push topic=shopify.legacy.outbound.",
             "AS400 / fulfillment push.\n1. consumer_lag."),
            ("describe-fx-trades", "Describe fx.trades.captured", "under-replicated FOREX trades",
             "kafka_describe_topic fx.trades.captured on msk-forex-markets.",
             "Trade capture topic.\n1. describe\n2. Under-replicated first."),
            ("describe-checkout-saga", "Describe checkout saga topic", "ecom.checkout.saga",
             "kafka_describe_topic ecom.checkout.saga.",
             "Saga bus. Do not rewind.\n1. describe."),
            ("ur-partitions-forex", "Under-replicated FOREX partitions", "MSK forex-markets URPs",
             "kafka_describe_topic fx.orders.routed. Report under-replicated partitions.",
             "URP on matching input.\n1. describe fx.orders.routed\n2. Do not delete topic."),
            ("poison-shopify-hmac", "Poison HMAC / order webhook", "bad record on shopify.webhooks.orders",
             "Describe shopify.webhooks.orders. Do not skip-offset without approval. Bound to shopify-merchants.",
             "Poison pill. Approval to skip.\n1. describe topic\n2. Do not delete.\n3. FOREX offset skip is not this job."),
            ("create-research-topic", "Create research lab topic", "research.samples.lab only",
             "Propose kafka_create_topic research.samples.lab on product-research. FOREX/Shopify creates denied. Approval required.",
             "Research only.\n1. topic-lifecycle\n2. FOREX and Shopify creates denied."),
            ("lag-orders-workflow", "Orders workflow lag", "ecom.orders.created",
             "kafka_consumer_lag group=orders-workflow topic=ecom.orders.created.",
             "Order state machine.\n1. consumer_lag."),
            ("describe-settlement", "Describe settlement instructions", "fx.settlement.instructions",
             "kafka_describe_topic fx.settlement.instructions on msk-forex-settlement.",
             "CLS / SSI topic.\n1. describe\n2. Do not create/delete."),
            ("lag-fx-orders", "Describe + lag fx.orders.routed", "matching input topic health",
             "kafka_describe_topic fx.orders.routed then consumer_lag fx-matching-engine.",
             "Matching input end-to-end.\n1. describe\n2. lag."),
            ("shopify-retry-pileup", "Shopify retry pile-up on the bus", "ingress retries + lag",
             "consumer_lag shopify-order-sync on shopify.webhooks.orders. Correlate HMAC retries. Do not rewind.",
             "Retry + lag. Idempotency Redis next.\n1. lag\n2. No rewind\n3. No topic delete."),
        ],
    },
    "elk": {
        "folder": "elk_harnessing",
        "harness": "enterprise_it_harnessing/elk_harnessing/harness.py",
        "launcher": "harness-elk-job.sh",
        "howto": "HowToUse_ELK_Jobs.md",
        "title": "ELK / Search jobs",
        "jobs": [
            ("search-matching-rejects", "Search matching rejects", "fx-matching-engine reject",
             "es_search_index service=fx-matching-engine query=reject size=20.",
             "Sev2 rejects. alias/service matching.\n1. elasticsearch-query\n2. size=20\n3. Do not wipe the index."),
            ("search-fix-disconnect", "Search FIX disconnects", "forex-fix disconnect",
             "es_search_index alias=forex-fix query=disconnect size=20.",
             "FIX session index.\n1. search disconnect."),
            ("search-hmac-failed", "Search HMAC failures", "shopify-webhooks hmac_failed",
             "es_search_index alias=shopify-webhooks query=hmac_failed size=20.",
             "HMAC Sev2. Do not silence this alert.\n1. search hmac_failed."),
            ("search-saga-failed", "Search checkout saga_failed", "orders alias",
             "es_search_index alias=orders query=saga_failed size=20.",
             "Checkout saga failures.\n1. search saga_failed."),
            ("search-as400", "Search SOAP / AS400", "shopify-legacy",
             "es_search_index alias=shopify-legacy query=as400 OR soap size=20.",
             "Legacy bridge errors.\n1. search as400/soap."),
            ("search-sla-breach", "Search support SLA breach", "support alias",
             "es_search_index alias=support query=sla_breach size=20.",
             "Ticket SLA.\n1. search sla_breach."),
            ("search-carrier-timeout", "Search carrier timeouts", "shipping alias",
             "es_search_index alias=shipping query=carrier_timeout size=20.",
             "Fulfillment tracking.\n1. search carrier_timeout."),
            ("es-health-forex", "ES health FOREX stack", "es-forex-prod",
             "es_cluster_health business_unit=forex-markets (es-forex-prod).",
             "FOREX ES.\n1. cluster health\n2. Yellow/red before search jobs."),
            ("es-health-shopify", "ES health Shopify stack", "es-shopify-prod",
             "es_cluster_health business_unit=shopify-merchants (es-shopify-prod).",
             "Shopify ES.\n1. cluster health."),
            ("alerts-forex", "FOREX Grafana alerts", "grafana-forex-prod",
             "grafana_list_alerts business_unit=forex-markets.",
             "FOREX alert rules.\n1. list alerts\n2. Do not silence matching-engine."),
            ("alerts-hmac-keep-firing", "Shopify alerts — keep HMAC firing", "HMAC rules must stay firing",
             "grafana_list_alerts shopify-merchants. HMAC rules must stay firing.",
             "Never silence HMAC.\n1. list alerts\n2. silence-orders-only is the other job."),
            ("silence-orders-only", "Silence noisy orders warning only", "never matching / HMAC",
             "Propose grafana_silence_alert for a noisy orders-api warning. Never silence matching-engine or HMAC. Approval required.",
             "Dual-control silence.\n1. Propose silence\n2. Matching and HMAC stay firing."),
            ("pipeline-forex", "FOREX trade-capture ingest pipeline", "forex-trades into es-forex-prod",
             "Check fx-trade-capture pipeline into es-forex-prod. Alias forex-trades.",
             "Ingest lag.\n1. search + health\n2. Index wipe denied."),
            ("pipeline-shopify", "Shopify HMAC ingest pipeline", "events reaching es-shopify-prod",
             "Check shopify-webhook-ingress reaching es-shopify-prod. hmac_failed and ingest_lag.",
             "HMAC pipeline.\n1. search hmac_failed\n2. health es-shopify-prod."),
            ("dashboards-forex", "FOREX Grafana dashboards", "grafana-forex-prod folder",
             "grafana_list_dashboards business_unit=forex-markets (grafana-forex-prod).",
             "Find FOREX dashboards.\n1. list dashboards."),
        ],
    },
}


def skill_md(slug: str, title: str, body: str) -> str:
    return (
        f"---\nname: {slug}\ndescription: {title}\n---\n\n"
        f"{body.strip()}\n"
    )


def write_role(key: str, spec: dict) -> None:
    folder = ENT / spec["folder"]
    jobs_pkg = folder / "jobs"
    jobs_pkg.mkdir(parents=True, exist_ok=True)
    scripts: dict[str, str] = {}
    rows: list[tuple[str, str, str]] = []
    harness = spec["harness"]
    rel = f"../../../run.sh {harness}"
    for slug, title, when, prompt, body in spec["jobs"]:
        skill_dir = folder / "skills" / slug
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(skill_md(slug, title, body), encoding="utf-8")
        escaped = prompt.replace('"', '\\"')
        scripts[slug] = f'{rel} --with-skill {slug} --once "{escaped}"'
        rows.append((f"./harness-{key}-job.sh {slug}" if key != "k8s" else f"./harness-k8s-job.sh {slug}", title, when))

    # fix launcher names in table
    launcher = spec["launcher"]
    rows = [(f"./{launcher} {slug}", title, when) for slug, title, when, *_ in spec["jobs"]]

    (jobs_pkg / "package.json").write_text(
        json.dumps({"name": f"enterprise-{key}-jobs", "private": True, "scripts": scripts}, indent=2)
        + "\n",
        encoding="utf-8",
    )

    howto = [
        f"# How To Use — {spec['title']}",
        "",
        f"`./{launcher}` is the **job** launcher. `./{launcher.replace('-job.sh', '.sh')}` stays the catalog / playbook launcher. Existing commands are unchanged.",
        "",
        "Each job injects its skill into Claude (`--with-skill`). Hooks stay in that role’s `permissions.yaml` (deny / allow / ask).",
        "",
        "| Command | Job (what Claude follows) | When to use |",
        "| --- | --- | --- |",
        f"| `./{launcher}` | Lists the 15 jobs | See every job |",
    ]
    for cmd, title, when in rows:
        howto.append(f"| `{cmd}` | {title} | {when} |")
    howto.append("")
    (ROOT / spec["howto"]).write_text("\n".join(howto) + "\n", encoding="utf-8")

    sh = ROOT / launcher
    profile = f"{spec['folder']}/jobs"
    sh.write_text(
        "#!/usr/bin/env bash\n"
        f"# {spec['title']} — 15 industry jobs. Does not replace ./{launcher.replace('-job.sh', '.sh')}\n"
        f"# Usage: ./{launcher}                 # list jobs\n"
        f"#        ./{launcher} <job>\n"
        "set -euo pipefail\n"
        'ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"\n'
        f'exec "$ROOT/enterprise_it_harnessing/_invoke.sh" {profile} "$@"\n',
        encoding="utf-8",
    )
    sh.chmod(0o755)


def main() -> None:
    for key, spec in ROLES.items():
        write_role(key, spec)
    print("generated 6 job launchers, 90 skills, 6 jobs/package.json, 6 HowToUse_*_Jobs.md")


if __name__ == "__main__":
    main()
