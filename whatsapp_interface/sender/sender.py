import os
import dotenv
import requests
import random

dotenv.load_dotenv()
API_KEY = os.getenv("AUTHENTICATION_API_KEY")


class WhatsAppSender:
    INSTANCE = "bete"
    SERVER_URL = "localhost:8080"

    def __init__(self):
        self.headers = {"apiKey": API_KEY, "Content-Type": "application/json"}
        self.url = f"http://{self.SERVER_URL}/message/sendText/{self.INSTANCE}"

    def text_sender(self, message, number):
        payload = {"number": number, "text": message, "delay": self._set_delay()}
        response = requests.post(url=self.url, json=payload, headers=self.headers)
        print(response.json())

    def audio_sender(self):
        pass

    def _set_delay(self):
        return random.randint(500, 3000)
