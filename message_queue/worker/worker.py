import pika
import time
import argparse
from audio_processsing import SpeechToText
from whatsapp_interface.sender.sender import WhatsAppSender


def start_worker(queue_name: str):
    speech_to_text = SpeechToText()
    whatsapp_sender = WhatsAppSender(
        "/Users/theocoelho/Documents/academico/faculdade/TCC/tcc_project/audios/554199941200/20250715/94c6ba92-469c-44e1-8462-acc54b871bdb.ogg"
    )
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        print(f"Mensagem recebida da {queue_name}: {body.decode()}")
        if queue_name == "audio_queue":
            text = speech_to_text.process(body.decode())
            number = body.decode().split("/")[1]
            whatsapp_sender.audio_sender(text, number)

        time.sleep(1)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(f"[*] Aguardando mensagens em {queue_name}. CTRL+C para sair.")
    channel.start_consuming()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Inicia um worker para consumir mensagens de uma fila específica."
    )
    parser.add_argument(
        "queue_name",
        type=str,
        help="Nome da fila para consumir (ex: audio_queue, text_queue)",
    )
    args = parser.parse_args()
    queue_name = args.queue_name
    if queue_name not in ["audio_queue", "text_queue"]:
        raise ValueError("Insert a valid queue name (audio_queue, text_queue)")

    start_worker(args.queue_name)
