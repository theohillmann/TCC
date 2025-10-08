# Diagrama de Sequência

Este diagrama mostra a interação entre componentes ao longo do tempo para processar uma mensagem.

## Cenário 1: Processamento de Mensagem de Texto

```mermaid
sequenceDiagram
    autonumber
    actor User as Usuário
    participant WA as WhatsApp API
    participant Webhook as Flask Webhook
    participant MP as MessageProcessor
    participant TP as TextProcessor
    participant Pub as Publisher
    participant RMQ as RabbitMQ
    participant Worker as Worker
    participant RAG as RAGModel
    participant VDB as Chroma VectorDB
    participant LLM as Ollama LLM
    participant Sender as WhatsAppSender
    
    User->>WA: Envia mensagem texto
    WA->>Webhook: POST /webhook (JSON)
    Webhook->>MP: process(message_payload)
    MP->>MP: _classify_message()
    MP->>MP: _is_text()
    MP->>TP: process(message_payload)
    TP->>TP: Extrai número e texto
    TP->>Pub: publish_message("text", data)
    Pub->>RMQ: Publica na text_queue
    RMQ-->>Pub: ACK
    Pub-->>TP: Publicado
    TP-->>MP: Processado
    MP-->>Webhook: MessageType
    Webhook-->>WA: 200 OK
    
    Note over RMQ,Worker: Processamento assíncrono
    
    RMQ->>Worker: Consome mensagem text_queue
    Worker->>Worker: Extrai número e mensagem
    Worker->>RAG: ask(question)
    RAG->>RAG: Cria embedding da pergunta
    RAG->>VDB: Busca similar (k=5)
    VDB-->>RAG: Documentos relevantes
    RAG->>RAG: format_docs()
    RAG->>RAG: Monta prompt completo
    RAG->>LLM: invoke(prompt)
    LLM->>LLM: Processa (temp=0.5)
    LLM-->>RAG: Resposta gerada
    RAG-->>Worker: Resposta final
    Worker->>Sender: text_sender(message, number)
    Sender->>Sender: _set_delay()
    Sender->>WA: POST sendText
    WA-->>Sender: 200 OK
    WA->>User: Entrega resposta
```

## Cenário 2: Processamento de Mensagem de Áudio

```mermaid
sequenceDiagram
    autonumber
    actor User as Usuário
    participant WA as WhatsApp API
    participant Webhook as Flask Webhook
    participant MP as MessageProcessor
    participant AP as AudioProcessor
    participant Pub as Publisher
    participant RMQ as RabbitMQ
    participant Worker as Worker (audio)
    participant STT as SpeechToText
    participant AC as AudioConverter
    participant SR as SpeechRecognizer
    participant GCP as Google Speech API
    participant Worker2 as Worker (text)
    participant RAG as RAGModel
    participant Sender as WhatsAppSender
    
    User->>WA: Envia mensagem áudio
    WA->>Webhook: POST /webhook (base64 audio)
    Webhook->>MP: process(message_payload)
    MP->>MP: _classify_message()
    MP->>MP: _is_audio()
    MP->>AP: process(message_payload)
    AP->>AP: _get_base64_message()
    AP->>AP: _get_file_save_path()
    AP->>AP: _save_file() - salva OGG
    AP->>Pub: publish_message("audio", file_path)
    Pub->>RMQ: Publica na audio_queue
    RMQ-->>Pub: ACK
    Pub-->>AP: Publicado
    AP-->>MP: Processado
    MP-->>Webhook: MessageType
    Webhook-->>WA: 200 OK
    
    Note over RMQ,Worker: Processamento assíncrono - Áudio
    
    RMQ->>Worker: Consome audio_queue
    Worker->>STT: process(audio_path, "pt-BR")
    STT->>AC: to_wav(input_path)
    AC->>AC: AudioSegment.from_ogg()
    AC->>AC: export(WAV)
    AC-->>STT: wav_path (temp file)
    STT->>SR: recognize(wav_path, "pt-BR")
    SR->>GCP: recognize_google()
    GCP-->>SR: Texto transcrito
    SR-->>STT: Texto
    STT->>STT: Remove arquivo temp
    STT-->>Worker: Texto transcrito
    Worker->>Pub: publish_message("text", {number, text})
    Pub->>RMQ: Publica na text_queue
    
    Note over RMQ,Worker2: Processamento assíncrono - Texto
    
    RMQ->>Worker2: Consome text_queue
    Worker2->>RAG: ask(question)
    RAG-->>Worker2: Resposta
    Worker2->>Sender: text_sender(response, number)
    Sender->>WA: POST sendText
    WA->>User: Entrega resposta
```

## Cenário 3: Criação do Vector Database (Setup Inicial)

```mermaid
sequenceDiagram
    autonumber
    participant Admin as Administrador
    participant VS as VectorStore
    participant Loader as PyPDFLoader
    participant Splitter as RecursiveCharacterTextSplitter
    participant Embed as OllamaEmbeddings
    participant Chroma as Chroma VectorDB
    
    Admin->>VS: python create.py
    VS->>VS: __init__()
    VS->>VS: create()
    VS->>VS: load_pdfs()
    
    loop Para cada PDF em /data
        VS->>Loader: PyPDFLoader(pdf_path)
        Loader->>Loader: load()
        Loader-->>VS: Documentos
    end
    
    VS->>VS: chunk_documents()
    VS->>Splitter: RecursiveCharacterTextSplitter(800, 150)
    Splitter->>Splitter: split_documents()
    Splitter-->>VS: Chunks (fragmentos)
    
    VS->>VS: create_vector_store()
    VS->>Embed: OllamaEmbeddings("nomic-embed-text")
    
    loop Para cada chunk
        VS->>Embed: embed_documents([chunk])
        Embed-->>VS: Vector embedding
    end
    
    VS->>Chroma: from_documents(chunks, embeddings)
    Chroma->>Chroma: Armazena vetores
    Chroma-->>VS: Vector store criado
    VS-->>Admin: Sucesso: N chunks salvos
```

## Cenário 4: Envio de Resposta com Áudio (TTS)

```mermaid
sequenceDiagram
    autonumber
    participant Worker as Worker
    participant Sender as WhatsAppSender
    participant TTS as TextToSpeechGenerator
    participant Coqui as Coqui TTS Model
    participant WA as WhatsApp API
    participant User as Usuário
    
    Worker->>Sender: audio_sender(text, number)
    Sender->>TTS: synthesize(text, output_path)
    TTS->>TTS: Carrega speaker_wav_path
    TTS->>Coqui: tts_to_file(text, speaker_wav)
    Coqui->>Coqui: Clona voz do speaker
    Coqui->>Coqui: Sintetiza fala em PT-BR
    Coqui-->>TTS: Arquivo WAV gerado
    TTS-->>Sender: output_path
    Sender->>Sender: Lê arquivo e converte base64
    Sender->>Sender: _set_delay() - randomiza delay
    Sender->>WA: POST sendWhatsAppAudio (base64)
    WA-->>Sender: 200 OK
    WA->>User: Entrega áudio
    Sender->>Sender: Remove arquivo temp
```

## Descrição dos Cenários

### Cenário 1: Texto
Fluxo completo de processamento de mensagem de texto, desde a recepção até o envio da resposta gerada pelo RAG/LLM.

**Pontos-chave:**
- Processamento síncrono até a fila (passos 1-13)
- Processamento assíncrono via Worker (passos 14-26)
- RAG busca contexto antes de consultar LLM

### Cenário 2: Áudio
Fluxo de processamento de mensagem de áudio, incluindo transcrição e subsequente processamento como texto.

**Pontos-chave:**
- Salva áudio físico antes de publicar na fila
- Conversão OGG→WAV necessária para reconhecimento
- Transcrição via Google Speech API
- Republicação como texto para processamento RAG

### Cenário 3: Setup
Processo de criação inicial do banco de dados vetorial a partir de PDFs sobre diabetes.

**Pontos-chave:**
- Execução única durante setup
- Carrega e fragmenta múltiplos PDFs
- Cria embeddings com modelo Ollama
- Armazena vetores no Chroma DB

### Cenário 4: TTS
Geração e envio de resposta em formato de áudio usando síntese de voz.

**Pontos-chave:**
- Clonagem de voz a partir de amostra
- Sintetização em português do Brasil
- Conversão para base64 para envio via API
- Limpeza de arquivos temporários

## Interações Principais

1. **Assíncronas**: Webhook→Queue→Worker (desacoplamento)
2. **Síncronas**: Worker→RAG→LLM (pipeline sequencial)
3. **Externa**: Google Speech API, WhatsApp API
4. **Persistência**: Chroma VectorDB, Sistema de arquivos (áudios)
