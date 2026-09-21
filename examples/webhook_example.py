"""Create an Oura webhook subscription and handle incoming notifications.

The callback URL is exposed automatically via ngrok.
"""

import hashlib
import hmac
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from urllib.parse import parse_qs, urlparse

import ngrok
from dotenv import load_dotenv

from oura_py.client.oura_client import OuraClient
from oura_py.constants import WebhookDataType


class OuraWebhookHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, body: dict) -> None:
        encoded = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:
        # Oura verifies the callback URL with this challenge request.
        query = parse_qs(urlparse(self.path).query)
        received_token = query.get("verification_token", [None])[0]
        expected_token = os.environ["WEBHOOK_VERIFICATION_TOKEN"]
        challenge = query.get("challenge", [None])[0]
        token_matches = received_token == expected_token
        if not token_matches:
            self._send_json(401, {"error": "invalid verification token"})
            return
        self._send_json(200, {"challenge": challenge})

    def do_POST(self) -> None:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)
        timestamp = self.headers.get("x-oura-timestamp", "")
        signature = self.headers.get("x-oura-signature", "")
        secret = os.environ["CLIENT_SECRET"].encode("utf-8")
        expected = (
            hmac.new(secret, timestamp.encode("utf-8") + raw_body, hashlib.sha256)
            .hexdigest()
            .upper()
        )

        if not timestamp or not hmac.compare_digest(expected, signature.upper()):
            self._send_json(401, {"error": "invalid signature"})
            return

        try:
            event = json.loads(raw_body)
        except json.JSONDecodeError:
            self._send_json(400, {"error": "invalid JSON"})
            return

        print(
            "Webhook event:",
            event.get("event_type"),
            event.get("data_type"),
            event.get("object_id"),
        )
        # Fetch the changed resource asynchronously in a real
        # application using object_id and the user's stored OAuth token.
        self._send_json(200, {"status": "ok"})


if __name__ == "__main__":
    load_dotenv()
    port = 8000

    server = ThreadingHTTPServer(("127.0.0.1", port), OuraWebhookHandler)
    Thread(target=server.serve_forever, daemon=True).start()
    listener = ngrok.forward(f"127.0.0.1:{port}", authtoken_from_env=True)

    public_url = listener.url()
    callback_url = f"{public_url}/oura-webhook"

    client = OuraClient(
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        token=json.loads(os.environ["OURA_TOKEN"]),
    )

    event_type = "update"
    data_type = WebhookDataType.SESSION

    matching = next(
        (
            item
            for item in client.list_webhook_subscriptions().raw()
            if isinstance(item, dict)
            and item.get("callback_url") == callback_url
            and item.get("event_type") == event_type
            and item.get("data_type") == data_type.value
        ),
        None,
    )
    if matching:
        client.delete_webhook_subscription(subscription_id=matching["id"])

    subscription = client.create_webhook_subscription(
        {
            "callback_url": callback_url,
            "verification_token": os.environ["WEBHOOK_VERIFICATION_TOKEN"],
            "event_type": event_type,
            "data_type": data_type,
        }
    )
    print("Created subscription:", subscription.raw())
    print(f"Listening for webhook events on http://0.0.0.0:{port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
    finally:
        ngrok.disconnect(listener.url())
