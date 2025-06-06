import speech_recognition as sr

def transcrever_audio_microfone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ajustando para ruído ambiente... Aguarde um momento.")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Pode falar agora:")
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Reconhecendo...")
            texto = recognizer.recognize_google(audio, language="pt-BR")
            print("Você disse:", texto)
            return texto
        except sr.WaitTimeoutError:
            print("Tempo de escuta esgotado. Nenhuma fala detectada.")
        except sr.UnknownValueError:
            print("Não foi possível entender o que foi dito.")
        except sr.RequestError as e:
            print(f"Erro ao se conectar com o serviço de reconhecimento: {e}")
    return None


if __name__ == "__main__":
    transcrever_audio_microfone()
