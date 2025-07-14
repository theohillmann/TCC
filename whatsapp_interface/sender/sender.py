import os
import base64
import dotenv
import random
import requests

dotenv.load_dotenv()
API_KEY = os.getenv("AUTHENTICATION_API_KEY")


class WhatsAppSender:
    INSTANCE = "bete"
    SERVER_URL = "localhost:8080"

    def __init__(self):
        self.headers = {"apiKey": API_KEY, "Content-Type": "application/json"}
        self.text_url = f"http://{self.SERVER_URL}/message/sendText/{self.INSTANCE}"
        self.audio_url = (
            f"http://{self.SERVER_URL}/message/sendWhatsAppAudio/{self.INSTANCE}"
        )

    def text_sender(self, message, number):
        payload = {"number": number, "text": message, "delay": self._set_delay()}
        response = requests.post(url=self.text_url, json=payload, headers=self.headers)
        print(response.json())

    def audio_sender(self, file_path, number):
        with open(file_path, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")

        payload = {
            "number": number,
            "audio": audio_base64,
            "delay": self._set_delay(),
        }
        response = requests.post(url=self.audio_url, json=payload, headers=self.headers)
        print(response.json())
        return response

    def _set_delay(self):
        return random.randint(500, 3000)
