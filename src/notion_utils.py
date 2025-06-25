import requests
from datetime import datetime
import os
from main import DEBUG

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_VERSION = "2022-06-28"

if DEBUG:
    print("NOTION_TOKEN:", NOTION_TOKEN)
    print("NOTION_VERSION:", NOTION_VERSION)

def get_database(ID, log=False):
    url = f"https://api.notion.com/v1/databases/{ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }
    res = requests.post(url, headers=headers).json()
    if log:
        print("Notion Version", NOTION_VERSION)
        print("Database ID", ID)
        print(res.keys())
    if "status" not in res.keys():
        return res
    else:
        raise Exception(res)