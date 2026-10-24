# Verification

Executed on 2026-10-24 against the upgrade branch:

- Windows local dependency install, Ruff checks and pytest: 15 tests passed.
- Docker Compose image build and startup: healthy on localhost port 5000.
- `/healthz`: `ok`; `/readyz`: `Degraded` for the supplied sample feed.
- Container runtime user: `10001`.
- Real Playwright screenshots of dashboard and summary captured with Chrome.
- Dockerfile lint: hadolint 2.12.0 passed.

The image uses Python 3.13.17 slim-bookworm pinned by verified registry digest.
Local Python tests used 3.12. Final CI results are recorded in the PR.

No live Active Directory, LDAP bind, service action, alert delivery or production
collector was exercised. Demo timestamps are illustrative; live mode enforces
freshness. Readiness tests feed usability, not domain-controller connectivity.

Additional checks: Python 3.13 Linux tests passed (15); mobile viewport 390x844 had two cards, no horizontal overflow and no page errors. Gitleaks tree and reachable Git-history scans found no matches. npm audit and pip-audit found no known dependency vulnerabilities. A fresh Compose restart passed after copying .env.example.
