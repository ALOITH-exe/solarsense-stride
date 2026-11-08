# SolarSense Smart Home Energy Monitor

**STRIDE Threat Modeling**

A deliberately vulnerable Flask API for a smart-home energy monitor, scanned with a
custom Semgrep STRIDE ruleset, remediated, and rescanned to **zero findings**.
This repository contains the full evidence trail: vulnerable baseline, DFD,
threat ranking, controls mapping, the security fix, and five manual
vulnerability demonstrations.

| Metric | Baseline | After fix |
|---|---|---|
| Semgrep findings | **13** (10 ERROR + 3 WARNING) | **0** |
| STRIDE categories populated | 6 / 6 | — |
| Manual tests demonstrating exploit | 5 / 5 | 5 / 5 blocked |

---

## System and scope

**Scenario 2:** A Flask service that:

- ingests smart-meter readings (`POST /api/reading`, header `X-Key`)
- shows per-home consumption (`GET /dashboard?home_id=`)
- serves firmware (`GET /firmware`)
- updates tariff rates (`POST /tariff`)
- exports files (`GET /export?file=`)
- exposes an unauthenticated health probe (`GET /health`)

**Trust boundaries (B1–B4):**

| ID | Boundary | Trust |
|---|---|---|
| B1 | Internet (homeowners, admins, attacker) | Untrusted |
| B2 | Home WLAN (smart meters) | Semi-trusted |
| B3 | Server (Flask app, SQLite, exports dir) | Trusted |
| B4 | Third-party firmware host (`updates.example.com`) | Untrusted |

---
