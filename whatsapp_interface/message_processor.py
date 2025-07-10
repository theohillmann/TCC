from message_type import MessageType
from mocks import messages_upsert_audio, messages_upsert_text


class MessageProcessor:

    def process(self, message_payload: dict) -> MessageType:
        message_type = self._classify_message(message_payload)
        return message_type

    def _classify_message(self, payload: dict) -> MessageType:
        if self._is_audio(payload):
            return MessageType.AUDIO
        if self._is_text(payload):
            return MessageType.TEXT
        return MessageType.UNKNOWN

    def _is_audio(self, payload: dict) -> bool:
        return "audioMessage" in payload["data"]["message"]

    def _is_text(self, payload: dict) -> bool:
        return "conversation" in payload["data"]["message"]
