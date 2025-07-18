import os
import base64
import dotenv
import random
import requests
import uuid

try:
    from audio_processsing.tts.text_to_speech import TextToSpeechGenerator
except ImportError:
    print(
        "Erro: Não foi possível importar TextToSpeechGenerator. "
        "Verifique se o módulo 'audio_processsing' está no seu PYTHONPATH."
    )

    class TextToSpeechGenerator:
        def __init__(self, *args, **kwargs):
            raise NotImplementedError("TextToSpeechGenerator não pôde ser importado.")

        def synthesize(self, *args, **kwargs):
            raise NotImplementedError("TextToSpeechGenerator não pôde ser importado.")


dotenv.load_dotenv()
API_KEY = os.getenv("AUTHENTICATION_API_KEY")


class WhatsAppSender:
    INSTANCE = "bete"
    SERVER_URL = "localhost:8080"

    def __init__(self, speaker_wav_path: str):
        self.headers = {"apiKey": API_KEY, "Content-Type": "application/json"}
        self.text_url = f"http://{self.SERVER_URL}/message/sendText/{self.INSTANCE}"
        self.audio_url = (
            f"http://{self.SERVER_URL}/message/sendWhatsAppAudio/{self.INSTANCE}"
        )

        try:
            self.tts_generator = TextToSpeechGenerator(
                speaker_wav_path=speaker_wav_path
            )
        except Exception as e:
            print(f"Falha ao inicializar o TextToSpeechGenerator: {e}")
            self.tts_generator = None

    def text_sender(self, message, number):
        payload = {"number": number, "text": message, "delay": self._set_delay()}
        response = requests.post(url=self.text_url, json=payload, headers=self.headers)
        print(response.json())

    def audio_sender(self, text: str, number: str):
        if not self.tts_generator:

            print(
                "O gerador de TTS não está disponível. Não é possível enviar o áudio."
            )
            return None

        output_path = f"{uuid.uuid4()}.wav"

        try:
            self.tts_generator.synthesize(text=text, output_path=output_path)
            with open(output_path, "rb") as audio_file:
                audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
            payload = {
                "number": number,
                "audio": audio_base64,
                "delay": self._set_delay(),
            }
            response = requests.post(
                url=self.audio_url, json=payload, headers=self.headers
            )
            print(response.json())
            return response

        except Exception as e:
            print(f"Ocorreu um erro ao enviar a mensagem de áudio: {e}")
            return None

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    def _set_delay(self):
        return random.randint(500, 3000)
