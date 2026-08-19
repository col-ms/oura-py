import logging
import os

from dotenv import load_dotenv

from oura_py.oura_client import OuraClient

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)
    load_dotenv()
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]

    # On the first run this opens the Oura consent page. Subsequent runs use
    # the cached token and refresh it automatically when necessary.
    oura_client = OuraClient(
        client_id=client_id,
        client_secret=client_secret,
        token_path=".oura_tokens.json",
        interactive=True,
    )

    personal_info = oura_client.get_personal_info()
    print("Authenticated Oura user: %s", personal_info)
