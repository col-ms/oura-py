import json
import os

from dotenv import load_dotenv

from oura_py.client.oura_client import OuraClient

if __name__ == "__main__":
    load_dotenv()

    client_id = os.environ["CLIENT_ID"]
    token = json.loads(os.environ["OURA_TOKEN"])
    client = OuraClient(
        client_id=client_id,
        token=token,
    )

    raw_result = client.daily_sleep(start_date="2026-09-01").raw()

    if len(raw_result) > 0:
        doc_id = raw_result[0]["id"]
        doc_result = client.daily_sleep(document_id=doc_id).raw()
        print("Results identical? %s", (raw_result[0] == doc_result))
    else:
        raise ValueError("No results returned from initial call")

    print("Exiting...")
