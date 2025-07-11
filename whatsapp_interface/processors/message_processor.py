from models import MessageType
from .text_processor import TextProcessor
from .audio_processor import AudioProcessor


class MessageProcessor:

    def __init__(self):
        self.audio_processor = AudioProcessor()
        self.text_processor = TextProcessor()

    def process(self, message_payload: dict) -> MessageType:
        message_type = self._classify_message(message_payload)
        return message_type

    def _classify_message(self, payload: dict) -> MessageType:
        if self._is_audio(payload):
            self.audio_processor.process(payload)
        if self._is_text(payload):
            self.text_processor.process(payload)
        return MessageType.UNKNOWN

    def _is_audio(self, payload: dict) -> bool:
        return "audioMessage" in payload["data"]["message"]

    def _is_text(self, payload: dict) -> bool:
        return "conversation" in payload["data"]["message"]
