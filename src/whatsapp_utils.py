import requests
import os
from time_utils import format_time_ist
from main import DEBUG

WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")

if DEBUG:
    print("WHATSAPP_API_TOKEN:", WHATSAPP_API_TOKEN)

def send_whatsapp_message(text, phone_number):
    url = "https://api.ultramsg.com/instance127328/messages/chat"
    payload = {
        "token": WHATSAPP_API_TOKEN,
        "to": phone_number,
        "body": text
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.json())
    return response

def prepare_message(name: str, day: str, time: str, users: list[str], role: str) -> str:
    time_formatted = format_time_ist(time)
    message = ""
    if role.lower() == "student":
        instructor_name = users[0] if users else "assignment pending"
        message = f"""
Hi {name},

📅 You have a class scheduled on upcoming *{day}* at *{time_formatted}*.
👩‍🏫 Instructor: {instructor_name}

Please be ready on time!
        """
    
    elif role.lower() == "instructor":
        student_list = ",\n".join(users) if users else "No students assigned"
        message = f"""
Hi {name},

📅 You are scheduled to take a class on upcoming *{day}* at *{time_formatted}*.
👨‍🎓 Students: \n{student_list}

Kindly ensure you are prepared and notify the students if any changes arise.
"""

    return message
