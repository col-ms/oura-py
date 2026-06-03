from oura_py.oura_client import OuraClient
from dotenv import load_dotenv
import os
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    load_dotenv()
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    myClient = OuraClient(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="http://localhost:8080/callback",
    )
    summary = myClient.get_personal_info()
    print(summary)
