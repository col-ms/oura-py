from oura_py.oura_client import OuraClient
from dotenv import load_dotenv
import os
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    load_dotenv()
    PAT = os.getenv("PERSONAL_ACCESS_TOKEN")
    myClient = OuraClient(personal_access_token=PAT)
    summary = myClient.get_rest_mode_periods(start="2025-01-01")
    print(
        summary.data[0].end_day,
        type(summary.next_token),
    )
