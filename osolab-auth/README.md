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
