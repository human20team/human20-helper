# Team GitHub Access

Use this workflow when the user asks the agent to inspect or change code in repositories shared through a Human20 team.

## Two independent links

1. **Human20 profile link** associates the member with a GitHub identity so Human20 can reconcile organization and team access after an eligible purchase. It does not give the agent GitHub credentials.
2. **Agent-runtime GitHub connection** authorizes the user's agent through an installed GitHub MCP connector, OAuth integration, or equivalent provider-backed API. This is the only connection the agent may use for repository operations.

The Human20 bearer token and the `Human20 Environment Access` organization app are not repository credentials. The organization app is access automation with organization `Members: write`; do not try to use or repurpose it to read or modify code.

## Discovery and proof

1. Discover the GitHub tools already exposed by the current agent runtime. Do not assume a particular connector name or installation path.
2. If no GitHub integration is available, explain that the user must connect their own GitHub account in the agent's profile/integration settings. Never ask the user to paste a password, access token, private key, or OAuth code into chat.
3. Through the connected GitHub surface, read the authenticated GitHub login. Do not trust a login supplied in chat or copied from Human20 profile metadata as proof of the active connector identity.
4. Read the repositories visible to that identity and the effective permission for the exact target repository. Do not hard-code repository names: team grants can change.
5. Treat organization invitations, organization membership, team membership, and repository permission as separate states. An invitation must be accepted before ordinary team repository access can become effective.
6. Before a write, re-read the exact repository permission and repository rules. A reported `write` permission does not bypass protected branches, required reviews, or other repository policy.

## Decision matrix

- **GitHub connector missing:** no repository operation is possible. Guide the user to connect their GitHub account in the agent runtime; do not claim team access is absent.
- **Connector identity available, target repository not visible:** report that access is not yet proven. Ask the user to check for and accept the organization invitation, then retry the live read. Do not infer the cause if GitHub does not expose it.
- **Repository visible, read permission:** the agent may inspect it but must not claim write capability.
- **Repository visible, write permission:** the agent may create branches, commits, and pull requests when the user authorizes that work. Follow live repository rules; do not push or merge directly to a protected default branch.
- **Permission denied or provider error:** report the exact provider denial/error and stop; payment status is not a substitute for GitHub proof.

## Reporting contract

State:

- the authenticated GitHub login returned by the connected provider;
- the exact owner/repository checked;
- the effective permission actually read (`read`, `triage`, `write`, `maintain`, or `admin`, when the provider exposes it);
- whether the result is only identity/membership evidence or proven repository access;
- any pending invitation, missing connector, denied operation, or incomplete readback.

Do not include access tokens, OAuth secrets, private keys, or unrelated private repository names in output.
