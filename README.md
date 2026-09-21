# Oura-Py

`oura-py`: A python wrapper for interacting with Oura Ring's V2 API.

## Installation

Proper installation documentation to be added upon first production release.

## Authentication

Oura no longer accepts Personal Access Tokens. This package uses OAuth2
authorization-code authentication.

### One-time Oura setup

Before using the client, end users need an Oura developer application:

1. Create an OAuth application in the Oura developer portal.
2. Copy its client ID and client secret.
3. Add the callback URL used by your application.
4. Grant the scopes required by the application. The client requests Oura's
   standard data scopes by default; custom scopes can be supplied through the
   lower-level `OuraOAuth2Client` API.

The callback URL must match the URL registered with Oura. Authorization and
token persistence are application responsibilities; use
`OuraOAuth2Client` to perform the OAuth protocol steps.

### Local setup

Install the package and put only the application credentials in `.env` (or
export them in the shell):

```text
CLIENT_ID=your-oura-client-id
CLIENT_SECRET=your-oura-client-secret
OURA_TOKEN='{"access_token":"...","refresh_token":"..."}'
```

### Using an application-managed token

```python
import json
import os

from oura_py import OuraClient

client = OuraClient(
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    token=json.loads(os.environ["OURA_TOKEN"]),
)
```

The application obtains and stores the token. `OuraClient` refreshes it when
needed and can notify the application when the token changes:

```python
client = OuraClient(
    client_id=client_id,
    client_secret=client_secret,
    token=stored_token,
    token_updater=save_token,
)
```

## Client architecture

`OuraClient` exposes one method for each supported Oura API resource. Resource
methods return an `OuraResponse` rather than a bare dictionary or a Pydantic
model. This keeps the wire response available while allowing callers to opt in
to typed models when they need them.

```python
import os

from oura_py import OuraClient

client = OuraClient(
    client_id=os.environ["CLIENT_ID"],
    token=json.loads(os.environ["OURA_TOKEN"]),
)

response = client.daily_sleep(
    start_date="2025-01-01",
    end_date="2025-01-07",
)

raw_records = response.raw()
sleep_records = response.model()
metadata = response.metadata
```

`raw()` returns the JSON-compatible payload returned by the client. Collection
endpoints return a list of records; direct-object endpoints such as
`personal_info()` return one dictionary. `model()` validates that payload with
the endpoint's Pydantic model. It returns a list of model instances for a
collection and one model instance for a direct object. Model conversion is
cached on the response, so repeated calls do not revalidate the same payload.

`metadata` contains request information such as the endpoint and query
parameters used. It is useful for logging, auditing, and reproducing a
request.

### Collections, pagination, and document IDs

Collection methods follow Oura's `data`/`next_token` pagination envelope
automatically. The client requests subsequent pages and combines their records
into one response:

```python
response = client.workout(start_date="2025-01-01", end_date="2025-01-31")
workouts = response.model()
```

To retrieve one collection record, pass its `document_id`. The client sends the
identifier as a path component (`.../<document_id>`) and returns the direct
object:

```python
response = client.daily_sleep(document_id="sleep-record-id")
sleep = response.model()
```

`document_id` cannot be combined with `next_token`. Date parameters are not
sent for a document-specific request.

Endpoints backed by timestamps, such as `heartrate()` and
`ring_battery_level()`, use `start_datetime` and `end_datetime`. If neither is
provided, the client requests the preceding 24-hour window in UTC. Date-based
collection endpoints default to the preceding UTC day when dates are omitted.

### Webhook subscriptions

Webhook subscription methods also return `OuraResponse` objects:

```python
from oura_py.constants import WebhookDataType

subscriptions = client.list_webhook_subscriptions()
for subscription in subscriptions.raw():
    print(subscription["id"])

created = client.create_webhook_subscription(
    {
        "callback_url": "https://example.test/oura-webhook",
        "verification_token": "your-verification-token",
        "event_type": "update",
        "data_type": WebhookDataType.SESSION,
    }
)
print(created.model())
```

The list method returns a collection response. Get, create, update, and renew
methods return a single `WebhookSubscription` object. Deletion returns `None`
after a successful API request. Webhook management requires the client secret;
the client sends it using the headers required by Oura's webhook API.

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

### Webhooks

See `examples/webhook_example.py` for a complete subscription and receiver
example. The script uses ngrok's official Python SDK to expose the local receiver and derives the
public callback URL automatically. An ngrok authtoken may be required; set
`NGROK_AUTHTOKEN` if your ngrok account requires one.

The example expects these environment variables:

```text
CLIENT_ID=your-oura-client-id
CLIENT_SECRET=your-oura-client-secret
OURA_TOKEN='{"access_token":"...","refresh_token":"..."}'
WEBHOOK_VERIFICATION_TOKEN=choose-a-secret-value
NGROK_AUTHTOKEN=your-ngrok-authtoken
```

The example uses port `8000`, subscribes to `daily_sleep` updates, and uses
the generated ngrok URL automatically.

It handles Oura's verification challenge, validates the
`x-oura-signature` HMAC, acknowledges the notification quickly, and prints
the event metadata. Production applications should enqueue the event and
fetch the changed resource asynchronously using the event's `object_id`.
