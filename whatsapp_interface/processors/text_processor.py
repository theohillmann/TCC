from message_queue.publisher import publish_message


class TextProcessor:

    def process(self, message_payload: dict) -> str:
        print(message_payload.get("data").get("message").get("conversation"))
        message = message_payload.get("data").get("message").get("conversation")
        publish_message("text", message)
        return message
