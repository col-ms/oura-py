from oura_py.oura_client import OuraClient
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    PAT = os.getenv("PERSONAL_ACCESS_TOKEN")
    myClient = OuraClient(personal_access_token=PAT)
    print(myClient.get_personal_info())
