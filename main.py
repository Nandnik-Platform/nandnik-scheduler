from notion_utils import get_scheduled_tasks
from whatsapp_utils import send_whatsapp_message
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

def main():
    now = datetime.now(timezone.utc)
    tasks = get_scheduled_tasks()

    for task in tasks:
        start_time = task['start_time']
        if abs((start_time - now).total_seconds()) < 60:
            send_whatsapp_message(task['message'])

if __name__ == "__main__":
    main()
