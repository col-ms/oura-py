import os
from dotenv import load_dotenv
from oura_py.auth.oauth_manager import OuraOAuth2Client
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)
    load_dotenv()
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    auth_client = OuraOAuth2Client(CLIENT_ID, CLIENT_SECRET)
    auth_url, _ = auth_client.get_authorization_url()
    log.debug(f"Auth url: {auth_url}")
    code = input("Paste auth code: ").strip()
    token_dict = auth_client.exchange_code(code)
    log.info(code)
