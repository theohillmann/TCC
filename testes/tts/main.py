from TTS.api import TTS


def sintetizar_texto(texto, nome_arquivo='output.wav'):
    tts = TTS(model_name="tts_models/pt-br/cv/vits", progress_bar=False, gpu=False)

    tts.tts_to_file(text=texto, file_path=nome_arquivo)
    print(f"Áudio salvo em: {nome_arquivo}")


if __name__ == "__main__":
    texto = "Olá! Esta é uma demonstração do módulo de conversão de texto em voz do nosso projeto de telemedicina."
    sintetizar_texto(texto)
