# Diagrama de Sequência

Este diagrama mostra a interação entre componentes durante o processamento de mensagens.

```plantuml
@startuml

title Diagrama de Sequência - Mensagem de Áudio

actor Usuário
participant "WhatsApp" as WA
participant "Evolution API" as EVO
participant "Webhook Flask" as WH
participant "MessageProcessor" as MP
participant "AudioProcessor" as AP
participant "Publisher" as PUB
participant "RabbitMQ" as MQ
participant "Worker Audio" as WA_WORKER
participant "SpeechToText" as STT
participant "AudioConverter" as AC
participant "SpeechRecognizer" as SR
participant "Worker Text" as WT_WORKER
participant "RAGModel" as RAG
participant "Chroma VectorStore" as CHROMA
participant "Ollama LLM" as LLM
participant "WhatsAppSender" as SENDER
participant "TextToSpeechGenerator" as TTS

== Recebimento e Classificação ==

Usuário -> WA: Envia mensagem de áudio
activate WA

WA -> EVO: Encaminha mensagem
activate EVO

EVO -> WH: POST /webhook (JSON payload)
activate WH

WH -> MP: process(message_payload)
activate MP

MP -> MP: _classify_message(payload)
MP -> MP: _is_audio(payload)
note right: Verifica "audioMessage" no payload

MP -> AP: process(message_payload)
activate AP

== Processamento de Áudio ==

AP -> AP: _get_base64_message(payload)
AP -> AP: _get_file_save_path(payload)
note right: Gera path: audios/{number}/{date}/{uuid}.ogg

AP -> AP: _save_file(base64_str, file_path)
note right: Decodifica base64 e salva OGG

AP -> PUB: publish_message("audio", file_path)
activate PUB

PUB -> MQ: basic_publish(exchange, "audio", file_path)
activate MQ
MQ --> PUB: ACK
deactivate PUB

deactivate AP
MP --> WH: MessageType.UNKNOWN
deactivate MP
WH --> EVO: {"status": "OK"}
deactivate WH
deactivate EVO
deactivate WA

== Transcrição de Áudio ==

MQ -> WA_WORKER: callback(ch, method, properties, body)
activate WA_WORKER
note right: Consome de audio_queue

WA_WORKER -> STT: process(audio_path, "pt-BR")
activate STT

STT -> AC: to_wav(audio_path)
activate AC
AC -> AC: AudioSegment.from_ogg()
AC -> AC: export(tmp_wav, "wav")
AC --> STT: wav_path
deactivate AC

STT -> SR: recognize(wav_path, "pt-BR")
activate SR
SR -> SR: AudioFile(wav_path)
SR -> SR: recognizer.record(source)
SR -> SR: recognize_google(audio, "pt-BR")
note right: Usa Google Speech API
SR --> STT: texto transcrito
deactivate SR

STT -> STT: os.remove(wav_path)
note right: Remove arquivo temporário
STT --> WA_WORKER: texto
deactivate STT

WA_WORKER -> WA_WORKER: Formata {"number": number, "message": texto}

WA_WORKER -> PUB: publish_message("text", str(data))
activate PUB
PUB -> MQ: basic_publish(exchange, "text", data)
MQ --> PUB: ACK
deactivate PUB

deactivate WA_WORKER
deactivate MQ

== Processamento RAG ==

MQ -> WT_WORKER: callback(ch, method, properties, body)
activate MQ
activate WT_WORKER
note right: Consome de text_queue

WT_WORKER -> WT_WORKER: Parse JSON {number, message}

WT_WORKER -> RAG: ask(message)
activate RAG

RAG -> RAG: _config()
note right: Carrega prompt e configurações

RAG -> CHROMA: similarity_search(message, k=5)
activate CHROMA
CHROMA -> CHROMA: Cria embedding da pergunta
note right: Usa nomic-embed-text
CHROMA -> CHROMA: Busca top-5 documentos
CHROMA --> RAG: [doc1, doc2, doc3, doc4, doc5]
deactivate CHROMA

RAG -> RAG: format_docs(docs)
note right: Concatena conteúdo + metadados

RAG -> LLM: invoke(prompt + context + question)
activate LLM
LLM -> LLM: Processa com llama3.2
note right: Temperature: 0.5
LLM -> LLM: Gera resposta sobre diabetes
LLM --> RAG: resposta contextualizada
deactivate LLM

RAG --> WT_WORKER: resposta com fontes
deactivate RAG

== Envio de Resposta ==

WT_WORKER -> SENDER: text_sender(resposta, number)
activate SENDER

SENDER -> SENDER: _set_delay()
note right: Random 500-3000ms

SENDER -> EVO: POST /message/sendText/{instance}
activate EVO
note right: Payload: {number, text, delay}

EVO -> WA: Envia mensagem
activate WA

WA -> Usuário: Recebe resposta
deactivate WA

EVO --> SENDER: {"status": "success"}
deactivate EVO

deactivate SENDER
deactivate WT_WORKER
deactivate MQ

@enduml
```

## Sequência Alternativa: Mensagem de Texto

```plantuml
@startuml

title Diagrama de Sequência - Mensagem de Texto (Fluxo Simplificado)

actor Usuário
participant "WhatsApp" as WA
participant "Evolution API" as EVO
participant "Webhook Flask" as WH
participant "MessageProcessor" as MP
participant "TextProcessor" as TP
participant "Publisher" as PUB
participant "RabbitMQ" as MQ

Usuário -> WA: Envia mensagem de texto
WA -> EVO: Encaminha mensagem
EVO -> WH: POST /webhook
WH -> MP: process(message_payload)
MP -> MP: _classify_message()
MP -> MP: _is_text(payload)
note right: Verifica "conversation" no payload

MP -> TP: process(message_payload)
activate TP

TP -> TP: Extrai conversation
TP -> TP: Extrai remoteJid (número)
TP -> TP: Formata {"number": number, "message": message}

TP -> PUB: publish_message("text", str(data))
activate PUB
PUB -> MQ: basic_publish(exchange, "text", data)
deactivate PUB

deactivate TP
MP --> WH: MessageType.UNKNOWN
WH --> EVO: {"status": "OK"}

note over MQ: A partir daqui, segue o mesmo\nfluxo de processamento RAG\ndo diagrama anterior

@enduml
```

## Sequência: Criação da Base de Conhecimento

```plantuml
@startuml

title Diagrama de Sequência - Criação do Vector Store

participant "VectorStore" as VS
participant "PyPDFLoader" as PDF
participant "RecursiveCharacterTextSplitter" as SPLITTER
participant "OllamaEmbeddings" as EMB
participant "Chroma" as CHROMA
database "chroma_knowledge/" as DB

-> VS: create()
activate VS

VS -> VS: load_pdfs()
activate VS

loop Para cada arquivo PDF em ../data/
    VS -> PDF: PyPDFLoader(pdf_path).load()
    activate PDF
    PDF --> VS: [page1, page2, ..., pageN]
    deactivate PDF
    VS -> VS: docs.extend(pages)
end

deactivate VS

VS -> VS: chunk_documents()
activate VS

VS -> SPLITTER: RecursiveCharacterTextSplitter(800, 150)
activate SPLITTER
SPLITTER --> VS: splitter
deactivate SPLITTER

VS -> SPLITTER: split_documents(docs)
activate SPLITTER
SPLITTER -> SPLITTER: Divide em chunks de 800 chars
SPLITTER -> SPLITTER: Overlap de 150 chars
SPLITTER --> VS: chunks[]
deactivate SPLITTER

deactivate VS

VS -> VS: create_vector_store()
activate VS

VS -> EMB: OllamaEmbeddings("nomic-embed-text")
activate EMB
EMB --> VS: embedding
deactivate EMB

VS -> CHROMA: from_documents(chunks, embedding, persist_dir)
activate CHROMA

loop Para cada chunk
    CHROMA -> EMB: embed_documents([chunk.text])
    activate EMB
    EMB --> CHROMA: vector[]
    deactivate EMB
    CHROMA -> CHROMA: Adiciona (vector, metadata) ao índice
end

CHROMA -> DB: Persiste índice
CHROMA --> VS: Vector store criado
deactivate CHROMA

VS --> : "Vector store created with N chunks"
deactivate VS

@enduml
```

## Pontos-Chave das Sequências

### Mensagem de Áudio
1. **Recepção**: WhatsApp → Evolution API → Webhook Flask
2. **Salvamento**: Base64 decodificado e salvo como .ogg
3. **Enfileiramento**: Caminho do arquivo publicado na audio_queue
4. **Transcrição**: OGG → WAV → Google Speech API → Texto
5. **Reprocessamento**: Texto publicado na text_queue
6. **RAG**: Busca contexto + LLM gera resposta
7. **Resposta**: Enviada via Evolution API

### Mensagem de Texto
- Pula etapas de transcrição
- Vai direto para text_queue
- Segue mesmo fluxo RAG

### Criação do Vector Store
- Carrega PDFs da pasta ../data/
- Divide em chunks (800 chars, overlap 150)
- Gera embeddings com nomic-embed-text
- Persiste em Chroma

### Características do Sistema
- **Assíncrono**: Filas desacoplam processamento
- **Resiliente**: Erros não param todo sistema
- **Escalável**: Workers podem ser multiplicados
- **Contextual**: RAG fornece respostas precisas sobre diabetes
