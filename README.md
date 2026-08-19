## Authentication

Oura no longer accepts Personal Access Tokens. This package uses OAuth2
authorization-code authentication.

### One-time Oura setup

Before using the client, end users need an Oura developer application:

1. Create an OAuth application in the Oura developer portal.
2. Copy its client ID and client secret.
3. Add the callback URL configured for the script. The default is
   `http://localhost:8080/callback`.
4. Grant the scopes required by the application. The client requests Oura's
   standard data scopes by default; custom scopes can be supplied through the
   lower-level `OuraOAuth2Client` API.

The callback URL must match the URL registered with Oura. If a different URL
is registered, pass that URL to `OuraClient` with `redirect_uri`.

### Local setup

Install the package and put only the application credentials in `.env` (or
export them in the shell):

```text
CLIENT_ID=your-oura-client-id
CLIENT_SECRET=your-oura-client-secret
```

Keep `.env` private. It is for static application configuration; OAuth access
and refresh tokens are stored separately.

### First run

The first interactive run opens the Oura consent page in a browser:

```python
import os

from oura_py import OuraClient

client = OuraClient(
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    token_path=".oura_tokens.json",
    redirect_uri="http://localhost:8080/callback",
    interactive=True,
)
```

After consent, Oura redirects the browser to the local callback and the client
saves the resulting token in `.oura_tokens.json`. Later runs reuse that token
and refresh it automatically when necessary. The token file is ignored by
Git; do not commit it or put refresh tokens in `.env`.

For a non-interactive process, perform authorization once and then construct
the client with `interactive=False` (the default). It will use the existing
token store and fail clearly if no usable token is available.

### Custom scopes

For applications that need a scope set different from the default, use
`OuraOAuth2Client` directly. The complete flow is shown in
`examples/custom_scopes.py`; the essential calls are:

```python
from oura_py.auth.oauth_manager import OuraOAuth2Client

oauth_client = OuraOAuth2Client(client_id, client_secret)
authorization_url, state = oauth_client.get_authorization_url(
    scope=["personal", "daily", "heartrate"],
    redirect_uri="http://localhost:8080/callback",
)
# Send the user to authorization_url and validate the returned state.
token = oauth_client.exchange_code(authorization_code)
client = OuraClient(
    client_id=client_id,
    client_secret=client_secret,
    token=token,
)
```

`OuraClient` accepts a custom `TokenStore` through `token_store`. This allows
applications to use an OS keyring, encrypted storage, or a deployment secret
manager without changing the client or request code:

```python
client = OuraClient(
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    token_store=my_keyring_store,
)
```

`JsonTokenStore` is intended for local development and command-line scripts;
use a keyring or secret manager for shared or production environments.

### Webhooks

See `examples/webhook_example.py` for a complete subscription and receiver
example. The script uses ngrok's official Python SDK to expose the local receiver and derives the
public callback URL automatically. An ngrok authtoken may be required; set
`NGROK_AUTHTOKEN` if your ngrok account requires one.

The example expects these environment variables:

```text
CLIENT_ID=your-oura-client-id
CLIENT_SECRET=your-oura-client-secret
WEBHOOK_VERIFICATION_TOKEN=choose-a-secret-value
NGROK_AUTHTOKEN=your-ngrok-authtoken
```

The example uses port `8000`, subscribes to `daily_sleep` updates, and uses
the generated ngrok URL automatically.

It handles Oura's verification challenge, validates the
`x-oura-signature` HMAC, acknowledges the notification quickly, and prints
the event metadata. Production applications should enqueue the event and
fetch the changed resource asynchronously using the event's `object_id`.
