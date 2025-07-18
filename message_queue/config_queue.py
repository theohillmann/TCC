import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.exchange_declare(exchange="message_exchange", exchange_type="direct")

channel.queue_declare(queue="text_queue")
channel.queue_declare(queue="audio_queue")
channel.queue_declare(queue="text_to_audio")

channel.queue_bind(exchange="message_exchange", queue="text_queue", routing_key="text")
channel.queue_bind(
    exchange="message_exchange", queue="audio_queue", routing_key="audio"
)

print("RabbitMQ configurado com sucesso.")
connection.close()
