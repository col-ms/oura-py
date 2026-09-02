import logging
import os
from pprint import pprint

from dotenv import load_dotenv

from oura_py.client.oura_client import OuraClient

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
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

    new_result = client.daily_sleep(start_date="2026-08-18", end_date="2026-09-01")
    pprint(new_result.raw())

    validated = new_result.model()

    old_result = client.get_sleep_summary(start="2026-08-18", response_format="raw")
    pprint(old_result)

    log.info("Exiting...")
