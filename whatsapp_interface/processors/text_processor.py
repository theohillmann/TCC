from message_queue.publisher import publish_message


class TextProcessor:

    def process(self, message_payload: dict) -> str:
        print(message_payload.get("data").get("message").get("conversation"))
        message = message_payload.get("data").get("message").get("conversation")
        number = (
            message_payload.get("data", {})
            .get("key", {})
            .get("remoteJid", "")
            .split("@")[0]
        )
        format_message = {"number": number, "message": message}
        publish_message("text", str(format_message))
        return message
