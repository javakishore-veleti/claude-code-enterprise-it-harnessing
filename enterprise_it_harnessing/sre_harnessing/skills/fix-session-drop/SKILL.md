---
name: fix-session-drop
description: FIX session drop
---

FOREX bank FIX layer. Bound to forex-markets.
1. resolve_service fx-fix-gateway
2. observe_health — session drops
3. fetch_logs — disconnect
Do not restart fx-matching-engine at peak.
