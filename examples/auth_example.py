import logging
import os
from pprint import pprint

from dotenv import load_dotenv

from oura_py.client.oura_client import OuraClient

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)
    load_dotenv()
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]

    # On the first run this opens the Oura consent page. Subsequent runs use
    # the cached token and refresh it automatically when necessary.
    client = OuraClient(
        client_id=client_id,
        client_secret=client_secret,
        interactive=True,
        response_format="models",
    )

    result = client.get_personal_info()
    pprint(result)
