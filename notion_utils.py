import requests
from datetime import datetime
import os

NOTION_DB_ID = os.getenv("NOTION_DB_ID")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_VERSION = "2022-06-28"

def get_scheduled_tasks():
    url = f"https://api.notion.com/v1/databases/{NOTION_DB_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)
    data = response.json()

    tasks = []
    for row in data["results"]:
        props = row["properties"]
        start_time = props["Start Time"]["date"]["start"]
        message = props["Message"]["rich_text"][0]["text"]["content"]

        tasks.append({
            "start_time": datetime.fromisoformat(start_time),
            "message": message
        })

    return tasks
