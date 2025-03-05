from oura_py.oura_client import OuraClient
from dotenv import load_dotenv
import os
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    load_dotenv()
    PAT = os.getenv("PERSONAL_ACCESS_TOKEN")
    myClient = OuraClient(personal_access_token=PAT)
    summary = myClient.get_session_data(start="2023-09-01")
    print(
        summary.data[0].type,
        type(summary.next_token),
    )
