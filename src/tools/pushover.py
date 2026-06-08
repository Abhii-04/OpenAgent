import os
import requests
from dotenv import load_dotenv
from agents import function_tool

load_dotenv(override=True)

pushover_token = os.getenv('PUSHOVER_TOKEN')
pushover_url = "https://api.pushover.net/1/messages.json"
pushover_user = os.getenv('PUSHOVER_USER')


def send_push_notification(message: str) -> str:
    if not pushover_user or not pushover_token:
        raise RuntimeError("PUSHOVER_USER and PUSHOVER_TOKEN must be set")

    payload = {"user": pushover_user, "token": pushover_token, "message": message}
    response = requests.post(pushover_url, data=payload, timeout=10)
    response.raise_for_status()
    return "Notification sent"


@function_tool
def push(message: str) -> str:
    """Send a push notification to the user's phone."""
    return send_push_notification(message)
