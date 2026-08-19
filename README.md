## Authentication

Oura uses OAuth2. Configure the application credentials in environment
variables, then let `OuraClient` load and refresh the user token:

```python
import os

from oura_py import OuraClient

client = OuraClient(
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    token_path=".oura_tokens.json",
    interactive=True,
)
```

The first interactive run opens the Oura authorization page. The resulting
OAuth token is stored in the standalone JSON token file and refreshed on later
runs. The token file is ignored by Git; do not commit it or put refresh tokens
in `.env`.

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
