# Osolab Auth Integration

This fork is the Taiga client application for Osolab Auth. The goal is to use
Taiga as the portfolio work tracker for human + AI collaboration while
authenticating users through the local OIDC/OAuth foundation.

## Repositories

- Taiga deployment fork: `https://github.com/Takeru-k7a/taiga-docker`
- Taiga OIDC plugin fork: `https://github.com/Takeru-k7a/taiga-contrib-oidc-auth`
- Portfolio/Auth workspace: `../OsolabPortfolio`

## Target Architecture

```text
browser / mobile / CLI / MCP client
        |
        v
   Osolab Auth
   OIDC provider
        |
        | Authorization Code + PKCE
        v
   Taiga client app
   client_id: taiga-portfolio
        |
        v
   Portfolio planning
   backlog / kanban / issues
```

Taiga is a relying party. Osolab Auth remains the issuer and source of truth for
identity, consent, token lifetime, and future agent delegation policy.

## Local Bootstrap

1. Register an OIDC client in Osolab Auth.

   ```text
   client_id: taiga-portfolio
   client_type: web
   redirect_uri: http://localhost:9000/oidc/callback/
   scopes: openid profile email
   grant_types: authorization_code
   response_types: code
   pkce: required
   ```

2. Copy the example environment file.

   ```powershell
   Copy-Item osolab-auth\.env.osolab.example .env.osolab
   ```

3. Fill in `OIDC_RP_CLIENT_ID`, `OIDC_RP_CLIENT_SECRET`, and the issuer URLs.

4. Start Taiga with the overlay compose file.

   ```powershell
   docker compose --env-file .env --env-file .env.osolab -f docker-compose.yml -f docker-compose.osolab-auth.yml up -d --build
   ```

5. Create the first admin user if needed.

   ```powershell
   docker compose --env-file .env --env-file .env.osolab -f docker-compose.yml -f docker-compose.osolab-auth.yml run --rm taiga-manage createsuperuser
   ```

## Current Runtime Decision

The current PC/WSL Docker VM can run this stack for local use. A first
measurement with Taiga and the existing Osolab Auth containers running showed:

```text
Host memory: about 63.7GB total / 30.7GB free
Docker VM limit: about 31.2GB
Taiga stack: about 1.1GB
Existing Auth SQL Server: about 1.4GB
```

For now, prefer this order:

1. Run Taiga locally on `http://localhost:9000`.
2. Expose it through a secure tunnel for mobile/remote access.
3. Move stateless Taiga services to Cloud Run after OIDC login works locally.
4. Keep PostgreSQL and RabbitMQ outside Cloud Run unless a managed replacement
   is chosen.

## Tunnel Plan

For a short-lived working setup, expose local Taiga through one of:

- Cloudflare Tunnel
- Tailscale Funnel
- ngrok

When the public tunnel URL is chosen, register an additional OIDC redirect URI:

```text
https://<taiga-tunnel-host>/oidc/callback/
```

Also update `.env.osolab` and `osolab-auth/front/conf.json` for the public
host:

```text
TAIGA_SCHEME=https
TAIGA_DOMAIN=<taiga-tunnel-host>
WEBSOCKETS_SCHEME=wss
```

```json
{
  "api": "https://<taiga-tunnel-host>/api/v1/",
  "eventsUrl": "wss://<taiga-tunnel-host>/events",
  "baseHref": "/"
}
```

## Cloud Run Split

Cloud Run is a good target for stateless services, but the full docker-compose
stack should not be lifted as-is. Split it like this:

```text
Cloud Run service:
- taiga-front
- taiga-back
- taiga-protected
- taiga-events
- gateway, or direct routing through a load balancer

Cloud Run worker pool:
- taiga-async

External state:
- PostgreSQL: Cloud SQL or a small VM
- RabbitMQ: small VM or managed RabbitMQ
- media files: Cloud Storage or another durable object store
```

Before moving to Cloud Run, resolve these:

- OIDC issuer and redirect URIs must use the final HTTPS host.
- `taiga-back` must connect to external PostgreSQL and RabbitMQ.
- uploaded media must not depend on container-local storage.
- `taiga-events` WebSocket behavior must be checked behind Cloud Run.
- secrets must be moved to Secret Manager or equivalent.

## Auth Boundaries

- Taiga owns project tracking data.
- Osolab Auth owns identities, client registration, sessions, consent, and token
  policy.
- AI agents should eventually be represented as delegated OAuth clients, not as
  human users sharing passwords.
- MCP tools should be mapped to fine-grained scopes before they can mutate Taiga
  or portfolio data.

## First Portfolio Project Shape

- Epic: Auth foundation
- Epic: Portfolio site
- Epic: Taiga integration
- Epic: AI collaboration workflow
- Swimlanes: Human, AI agent, Blocked, Needs decision
- Initial labels: `auth`, `oidc`, `mcp`, `agent`, `portfolio`, `ops`

## Notes

The current OIDC plugin is an older Taiga contrib package. This fork keeps it as
a separate dependency so we can patch claims, username mapping, and callback
behavior without carrying a large Taiga source fork immediately.
