import os
from typing import Optional
import speech_recognition as sr
from audio_processsing.stt.audio_converter import AudioConverter
from audio_processsing.stt.speech_recognizer import SpeechRecognizer


class SpeechToText:
    def __init__(
        self,
        audio_converter: Optional[AudioConverter] = None,
        speech_recognizer: Optional[SpeechRecognizer] = None,
    ):
        self.audio_converter = audio_converter or AudioConverter()
        self.speech_recognizer = speech_recognizer or SpeechRecognizer()

    def process(self, audio_path: str, language: str = "pt-BR") -> Optional[str]:
        wav_path = None
        try:
            wav_path = self.audio_converter.to_wav(audio_path)
            text = self.speech_recognizer.recognize(wav_path, language=language)
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            raise RuntimeError(f"Erro na API do Google: {e}")
        finally:
            if wav_path and os.path.exists(wav_path):
                os.remove(wav_path)


if __name__ == "__main__":
    audio_path = "/Users/theocoelho/Documents/academico/faculdade/TCC/tcc_project/audios/554199941200/20250714/d4c11dd6-6f22-4d77-9aea-3cd748cfb9c8.ogg"
    stt = SpeechToText()
    result = stt.process(audio_path)
    if result:
        print(result)
    else:
        print("Não foi possível entender o áudio.")
