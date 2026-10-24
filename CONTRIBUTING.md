# Contributing

Use a feature branch and open a PR. Keep changes focused and use synthetic data. Never attach operational feeds, credentials, real addresses or district/client identifiers.

## Checks

Follow the Docker quick start and development commands in [README.md](README.md). Run Ruff, pytest and npm run lint:docs. CI also builds and starts Compose and scans for secrets.

Add regression tests for feed validation, aggregation and freshness changes. Preserve localhost publishing, demo labels, escaping and the fail-closed Unknown state.

For UI changes, capture the running demo and inspect desktop and mobile widths. No mockups or production data in screenshots.

PRs should describe the problem, behavior change, commands run and remaining limitations. Maintainers approve merges and releases. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
