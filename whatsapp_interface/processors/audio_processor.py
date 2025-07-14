import os
import uuid
import base64
from datetime import datetime
from message_queue.publisher import publish_message


class AudioProcessor:
    BASE_FOLDER = "audios"

    def process(self, message_payload: dict):
        base64_message = self._get_base64_message(message_payload)
        file_path = self._get_file_save_path(message_payload)
        self._save_file(base64_message, file_path)
        publish_message("audio", file_path)

    def _get_base64_message(self, message_payload: dict) -> str | None:
        data = message_payload.get("data", {})
        message = data.get("message", {})
        return message.get("base64", None)

    def _get_file_save_path(self, message_payload: dict) -> str:
        save_folder = os.path.join(
            self.BASE_FOLDER,
            self._get_user_number(message_payload),
            self._get_datetime(message_payload),
        )
        return f"{save_folder}/{uuid.uuid4()}.ogg"

    def _get_user_number(self, message_payload: dict) -> str:
        return message_payload.get("data").get("key").get("remoteJid").split("@")[0]

    def _get_datetime(self, message_payload: dict) -> str:
        timestamp_str = message_payload.get("date_time")
        raw_datetime = datetime.fromisoformat(timestamp_str)
        return raw_datetime.strftime("%Y%m%d")

    def _save_file(self, base64_str: str, file_path: str):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        raw = base64.b64decode(base64_str)
        with open(file_path, "wb") as file:
            file.write(raw)
