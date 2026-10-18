<div align="center">

![dirvex banner](docs/assets/banner.svg)

# dirvex

**A lightweight, self-hosted dashboard for monitoring Active Directory domain controller health — replication, SYSVOL, LDAP bind, and service status at a glance.**

*Formerly DirWatch.*

<a href="https://github.com/OneByJorah/dirvex/stargazers"><img src="https://img.shields.io/github/stars/OneByJorah/dirvex?style=flat-square" alt="Stars"></a>
<a href="https://github.com/OneByJorah/dirvex/commits"><img src="https://img.shields.io/github/last-commit/OneByJorah/dirvex?style=flat-square" alt="Last commit"></a>
<a href="https://github.com/OneByJorah/dirvex/releases"><img src="https://img.shields.io/github/v/release/OneByJorah/dirvex?style=flat-square" alt="Release"></a>
<img src="https://img.shields.io/github/license/OneByJorah/dirvex?style=flat-square" alt="License">
<img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.11">
<img src="https://img.shields.io/badge/Flask-3-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask 3">
<img src="https://img.shields.io/badge/PowerShell-5.1-5391FE?style=flat-square&logo=powershell&logoColor=white" alt="PowerShell">
<a href="https://ghcr.io/onebyjorah/dirvex"><img src="https://img.shields.io/badge/GHCR-ghcr.io%2Fonebyjorah%2Fdirvex-blue?style=flat-square&logo=docker&logoColor=white" alt="GHCR image"></a>

</div>

![dirvex dashboard](docs/screenshots/dashboard.png)

## Why this exists

dirvex surfaces the health of your Active Directory domain controllers in a single dark-theme dashboard. A PowerShell collector emits a normalized JSON status file (replication state, SYSVOL, LDAP bind, DHCP scope, and service status) and the Flask app renders it as status cards, DC detail, alerts, and trends.

It is aimed at Windows admins who want a quick, dependency-light DC health view without standing up SCOM or a full monitoring stack. The default stack runs entirely from mock data, so you can try it, demo it, and screenshot it without touching a real domain controller.

## Quick start

```bash
git clone https://github.com/OneByJorah/dirvex.git
cd dirvex
cp .env.example .env
sg docker -c 'docker compose up -d --build'
curl -s http://127.0.0.1:5000/healthz   # should print: ok
```

Open **<http://127.0.0.1:5000>**. If port `5000` is already in use, set `HOST_PORT` first:

```bash
HOST_PORT=5010 sg docker -c 'docker compose up -d --build'
curl -s "http://127.0.0.1:${HOST_PORT:-5000}/healthz"
```

> [!NOTE]
> The app reads `mock_dc_status.json` at startup. Swap in your own collector output by mounting a real file at the same path. The included `collectors/mock_dc_collector.ps1` generates sample data.

To capture the README screenshots locally:

```bash
npm install --no-save playwright
npx playwright install chromium
BASE_URL=http://127.0.0.1:5000 node scripts/screenshots.mjs
```

## Features

- **Domain controller overview** — per-DC status cards with health, replication, SYSVOL, and LDAP bind state.
- **Replication monitoring** — track replication health between controllers.
- **Service status** — DNS, DHCP, and ADWS service state per DC.
- **Alerts** — severity-coded alert feed (critical / warning / info) in the dashboard.
- **Public status endpoint** — `/public` returns a simple "all systems operational" health page.
- **Dark NOC UI** — responsive sidebar layout with stats grid and DC detail pages.
- **Collector scripts** — PowerShell collectors for DC status, with Teams/Telegram notification placeholders.
- **Docker & gunicorn** — production image runs gunicorn as a non-root user.

## Architecture

```mermaid
flowchart LR
    A[PowerShell collector] -->|mock_dc_status.json| B[Flask app :5000]
    C[Live AD collector output] -->|mount JSON| B
    B --> D[Dashboard /]
    B --> E[Public status /public]
    B --> F[Health check /healthz]
```

The app loads the JSON status file once at startup and renders it through Jinja2 templates. DC data can be refreshed by regenerating the file with a collector.

## Configuration

Basic operation needs no environment variables — the app reads `mock_dc_status.json` from its working directory. The Compose/entrypoint flow accepts:

| Variable | Default | Description |
| ---------- | --------- | ------------- |
| `FLASK_ENV` | `production` | Flask environment |
| `MOCK_MODE` | `true` | Use mock DC data (no live AD required) |
| `PORT` | `5000` | App port used by the entrypoint |
| `AD_DOMAIN` | — | AD domain (live mode) |
| `AD_SERVER` | — | DC hostname (live mode) |
| `AD_USERNAME` / `AD_PASSWORD` | — | AD bind credentials (live mode) |
| `LOG_LEVEL` | `INFO` | Log verbosity |

## API / Routes

| Endpoint | Method | Description |
| ---------- | -------- | ------------- |
| `/` | GET | DC status dashboard |
| `/public` | GET | Public status page |
| `/healthz` | GET | Health check — returns `ok` with HTTP 200 |

## Dashboard panels

| Panel | Description |
| ------- | ------------- |
| **DC Overview** | Status of all domain controllers |
| **Replication** | Inter-DC replication health |
| **Services** | DNS / DHCP / ADWS service state |
| **Alerts** | Recent severity-coded alerts |

## Use cases

1. **Windows admins** — a fast DC health check without SCOM.
2. **Homelab AD labs** — monitor test domain controllers.
3. **Pre-maintenance checks** — confirm replication and services before a change window.

## Tech stack

Python 3.11, Flask 3, Jinja2, PowerShell 5.1 collectors, gunicorn, Docker Compose.

## Screenshots

| Dashboard | Public status |
| --------- | ------------- |
| ![Dashboard](docs/screenshots/dashboard.png) | ![Public status](docs/screenshots/public.png) |

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). [Open an issue](https://github.com/OneByJorah/dirvex/issues) to report a bug or request a feature.

## Security

See [SECURITY.md](SECURITY.md) for reporting guidelines.

## License

MIT — see [LICENSE](LICENSE).

## Connect

- [jorahone.com](https://jorahone.com)
- [GitHub Org](https://github.com/OneByJorah)
- [info@jorahone.com](mailto:info@jorahone.com)
