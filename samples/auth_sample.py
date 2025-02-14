from oura_py.oura_client import OuraClient
from dotenv import load_dotenv
import os
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    load_dotenv()
    PAT = os.getenv("PERSONAL_ACCESS_TOKEN")
    myClient = OuraClient(personal_access_token=PAT)
    sleep_summary = myClient.get_sleep_summary(start="2025-02-11")
    print(sleep_summary.data[0].day)
