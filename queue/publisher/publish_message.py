import pika
import time


def publish_message(routing_key: str, body: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.basic_publish(
        exchange="message_exchange", routing_key=routing_key, body=body.encode("utf-8")
    )

    connection.close()


for i in range(10):
    print(1)
    publish_message("audio", f"{i}")
    time.sleep(0.5)
