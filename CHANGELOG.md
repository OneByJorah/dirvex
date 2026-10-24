# Changelog

## Unreleased

### Fixed

- Replace static metrics and status claims with validated JSON feed data.
- Reload on every request; report unknown for invalid or stale live feeds.
- Fix failing apt pins with a digest-pinned, non-root image.
- Bind Compose to localhost with read-only runtime permissions.

### Added

- J1 dashboard, demo labels, readiness endpoint and regression tests.
- Enforced lint/test/Compose CI and locked screenshot tooling.


## [0.1.1](https://github.com/OneByJorah/dirvex/compare/v0.1.0...v0.1.1) (2026-10-18)


### Bug Fixes

* **audit:** add standard project files ([7a02fd7](https://github.com/OneByJorah/dirvex/commit/7a02fd7c837de417ac8dc1edc3d13031d3f3ff4a))
* **ci:** sync hardened reusable screenshots workflow; wait for real dashboard render ([#21](https://github.com/OneByJorah/dirvex/issues/21)) ([2865ce5](https://github.com/OneByJorah/dirvex/commit/2865ce56e836bc7acdc444667a5ad5e8b01b2775))
* resolve container boot issues — entrypoint TTY detection, SQLAlchemy URI, non-root permissions ([25d0618](https://github.com/OneByJorah/dirvex/commit/25d0618ebb0524a6302c9bde2e40277ddb8abd88))

## [1.0.0] - 2026-07-07
### Added
- Initial release
- Dockerfile with multi-stage build
- docker-compose.yml with healthchecks
- .env.example with placeholder values
- First-run setup wizard / docker-entrypoint.sh
- Screenshot documentation
- README with deployment instructions
