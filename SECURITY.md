# Security Policy

JorahOne projects are self-hosted infrastructure tools. Security matters.

## Supported versions

We patch security issues in the latest release of the default branch. Older releases are best-effort.

## Reporting a vulnerability

Please **do not** open a public issue for security vulnerabilities.

Instead, email `security@jorahone.com` with:

- Affected repository and version/branch.
- Steps to reproduce or proof-of-concept.
- Possible impact.
- Suggested fix (optional).

We will respond within 72 hours and coordinate disclosure.

## Security practices for self-hosters

- Use Tailscale-only access; keep Compose on loopback.
- Never publish /public to the internet, open inbound ports or use Tailscale Funnel.
- Rotate secrets and API keys regularly.
- Bind services to localhost unless a reverse proxy handles TLS.

## Data boundary

Use a dedicated read-only collector-output mount. Feed contents may identify infrastructure; keep them out of issues, screenshots and source control. Credentials belong in Passbolt and are not consumed by this app. Liveness does not certify feed readiness or AD health.
