from typing import Optional
import speech_recognition as sr


class SpeechRecognizer:
    def __init__(self, recognizer: Optional[sr.Recognizer] = None):
        self.recognizer = recognizer or sr.Recognizer()

    def recognize(self, wav_path: str, language: str = "pt-BR") -> str:
        with sr.AudioFile(wav_path) as source:
            audio = self.recognizer.record(source)
        return self.recognizer.recognize_google(audio, language=language)
