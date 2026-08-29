---
name: cls-halt
description: CLS / settlement halt
---

forex-settlement only. CLS before risk-DB or cache failover.
1. resolve fx-cls-adapter, fx-risk-limits
2. observe_health
3. Do not page matching-engine unless rejects are also up.
