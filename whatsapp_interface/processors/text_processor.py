class TextProcessor:

    def process(self, message_payload: dict) -> str:
        print(message_payload.get("data").get("message").get("conversation"))
        return message_payload.get("data").get("message").get("conversation")
