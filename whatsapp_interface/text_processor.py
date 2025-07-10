from mocks import messages_upsert_text


class TextProcessor:

    def process(self, message_payload: dict) -> str:
        return messages_upsert_text.get("data").get("message").get("conversation")
