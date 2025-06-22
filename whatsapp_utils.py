import requests
import os


def send_whatsapp_message(text):
    url = "https://api.ultramsg.com/instance127328/messages/chat"
    payload = {
        "token": os.getenv("WHATSAPP_API_TOKEN"),
        "to": os.getenv("TO_PHONE_NUMBER"),
        "body": text
    }

    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.json())