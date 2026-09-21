# Changelog

## Unreleased

### Breaking changes

- Simplified authentication ownership:
  - `OuraClient` now requires an application-supplied OAuth token.
  - Token acquisition, persistence, and user association belong to the consuming application.
  - `token_updater` remains available for persisting refreshed credentials.
- Removed the built-in token lifecycle and interactive authorization helpers:
  - `TokenManager`
  - `TokenStore`
  - `JsonTokenStore`
  - `token_path`
  - `interactive`
  - Browser-based callback handling

### Authentication

- Retained OAuth protocol operations in `OuraOAuth2Client`:
  - Authorization URL generation.
  - Authorization-code exchange.
  - Explicit access-token refresh.
- Kept automatic token refresh in the authenticated request layer through
  `OAuth2Session`.
- Added typed `OAuthToken` and `TokenUpdater` definitions under `oura_py.auth`.

### HTTP and responses

- Simplified `RequestManager` request and response handling.
- Reduced `Result` to the fields used by the client: `status_code` and `data`.
- Removed recursive JSON payload validation from `Result`.
- Preserved request error translation, API error details, empty responses, and
  top-level array handling.

### Examples and documentation

- Updated examples to use application-managed tokens.
- Updated the authentication example to demonstrate the OAuth authorization-code
  flow and a token updater that writes to `.oura_tokens.json`.
- Simplified the webhook example while retaining verification, signature
  validation, subscription management, and event acknowledgement.
- Updated README authentication, token persistence, webhook, and custom-scope
  guidance.
