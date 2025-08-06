import pika
import time
import json
import argparse

from rag.retriever import RAGModel
from audio_processsing import SpeechToText
from message_queue.publisher import publish_message
from whatsapp_interface.sender.sender import WhatsAppSender


def start_worker(queue_name: str):
    speech_to_text = SpeechToText()
    whatsapp_sender = WhatsAppSender(
        "/Users/theocoelho/Documents/academico/faculdade/TCC/tcc_project/audios/554199941200/20250715/94c6ba92-469c-44e1-8462-acc54b871bdb.ogg"
    )
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    rag_model = RAGModel()

    def callback(ch, method, properties, body):
        if queue_name == "audio_queue":
            text = speech_to_text.process(body.decode())
            number = body.decode().split("/")[1]
            print(f"Audio recebido de {number}: {text}")
            publish_message("text", str({"number": number, "message": text}))
            print(f"mensagem publicada na fila text_queue: {text}")

        if queue_name == "text_queue":
            data = body.decode().replace("'", '"')
            dict_data = json.loads(data)
            sender_number = dict_data.get("number")
            message = dict_data.get("message")
            print(f"mensagem de {dict_data['number']}: {dict_data['message']}")
            response = rag_model.ask(message)
            print(f"resposta pronta: {response}")
            whatsapp_sender.text_sender(str(response), sender_number)
            print(f"resposta enviada para {sender_number}")

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
    if queue_name not in ["audio_queue", "text_queue", "process_llm_message"]:
        raise ValueError("Insert a valid queue name (audio_queue, text_queue)")

    start_worker(args.queue_name)
