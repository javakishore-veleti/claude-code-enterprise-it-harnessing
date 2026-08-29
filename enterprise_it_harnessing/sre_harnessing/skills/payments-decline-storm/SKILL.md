---
name: payments-decline-storm
description: Payments decline storm
---

PSP path. Same blast radius as checkout.
1. resolve payments-adapter
2. observe_health
3. Do not rewind the saga. Do not failover cart Redis without pausing checkout.
