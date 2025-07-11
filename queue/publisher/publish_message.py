import pika


def publish_message(routing_key: str, body: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.basic_publish(
        exchange="message_exchange", routing_key=routing_key, body=body.encode("utf-8")
    )

    connection.close()
