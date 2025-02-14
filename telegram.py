import requests
import logging

def send_telegram_message(bot_token: str, chat_id: list, message: str):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    for id in chat_id:
        payload = {
            "chat_id": id,
            "text": message
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            logging.info("TELEGRAM: Message sent successfully!")
        else:
            logging.error(f"TELEGRAM: Failed to send message: {response.text}")