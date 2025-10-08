# Diagrama de Componentes

Este diagrama mostra as dependências entre os módulos e componentes externos do sistema.

```mermaid
graph TB
    subgraph "Aplicação Principal"
        Main[main.py<br/>Entry Point]
    end
    
    subgraph "whatsapp_interface"
        Webhook[webhook.py<br/>Flask App]
        
        subgraph "processors"
            MessageProc[message_processor.py<br/>MessageProcessor]
            AudioProc[audio_processor.py<br/>AudioProcessor]
            TextProc[text_processor.py<br/>TextProcessor]
        end
        
        subgraph "sender"
            WASender[sender.py<br/>WhatsAppSender]
        end
        
        subgraph "models"
            MsgType[message_type.py<br/>MessageType]
        end
    end
    
    subgraph "message_queue"
        subgraph "publisher"
            Publisher[publish_message.py<br/>publish_message()]
        end
        
        subgraph "worker"
            Worker[worker.py<br/>Worker]
        end
        
        ConfigQueue[config_queue.py<br/>Queue Setup]
    end
    
    subgraph "audio_processsing"
        subgraph "stt"
            STT[speech_to_text.py<br/>SpeechToText]
            AudioConv[audio_converter.py<br/>AudioConverter]
            SpeechRec[speech_recognizer.py<br/>SpeechRecognizer]
        end
        
        subgraph "tts"
            TTS[text_to_speech.py<br/>TextToSpeechGenerator]
        end
    end
    
    subgraph "rag"
        RAGRetriever[retriever.py<br/>RAGModel]
        
        subgraph "create_database"
            CreateDB[create.py<br/>VectorStore]
        end
    end
    
    subgraph "text_processing"
        subgraph "pre_processing"
            Abbreviation[abreviation_dict.py<br/>Dicionário]
            SentencePreProc[sentence_pre_processing.py<br/>Pré-processamento]
        end
    end
    
    subgraph "lab - Experimentos"
        LabSTT[lab/stt/main.py<br/>Teste STT]
        LabTTS[lab/tts/main.py<br/>Teste TTS]
    end
    
    subgraph "Dependências Externas - Python"
        Flask[Flask<br/>Web Framework]
        Pika[Pika<br/>RabbitMQ Client]
        SRLib[SpeechRecognition<br/>Google Speech API]
        Pydub[Pydub<br/>Audio Processing]
        TTSLib[TTS/Coqui<br/>Text-to-Speech]
        LangChain[LangChain<br/>LLM Framework]
    end
    
    subgraph "Dependências Externas - Serviços"
        RabbitMQ[RabbitMQ<br/>Message Broker]
        Ollama[Ollama<br/>LLM Server<br/>llama3.2]
        ChromaDB[ChromaDB<br/>Vector Database]
        GoogleAPI[Google Speech API<br/>STT Service]
        WhatsAppAPI[WhatsApp API<br/>Evolution API]
    end
    
    subgraph "Dados"
        PDFs[PDFs sobre Diabetes<br/>rag/data/]
        Audios[Arquivos de Áudio<br/>audios/]
        VectorStore[Vector Store<br/>chroma_knowledge/]
    end
    
    %% Dependências da Aplicação
    Main -.-> Webhook
    Webhook --> Flask
    Webhook --> MessageProc
    MessageProc --> AudioProc
    MessageProc --> TextProc
    MessageProc --> MsgType
    
    AudioProc --> Publisher
    TextProc --> Publisher
    AudioProc -.-> Audios
    
    Publisher --> Pika
    Worker --> Pika
    
    Worker --> STT
    Worker --> RAGRetriever
    Worker --> WASender
    Worker --> Publisher
    
    WASender --> TTS
    WASender --> WhatsAppAPI
    
    STT --> AudioConv
    STT --> SpeechRec
    AudioConv --> Pydub
    SpeechRec --> SRLib
    SpeechRec --> GoogleAPI
    
    TTS --> TTSLib
    
    RAGRetriever --> LangChain
    RAGRetriever --> ChromaDB
    RAGRetriever --> Ollama
    RAGRetriever -.-> VectorStore
    
    CreateDB --> LangChain
    CreateDB --> ChromaDB
    CreateDB -.-> PDFs
    CreateDB -.-> VectorStore
    
    ConfigQueue --> Pika
    ConfigQueue --> RabbitMQ
    
    Pika --> RabbitMQ
    LangChain --> Ollama
    
    %% Lab experiments
    LabSTT -.-> SRLib
    LabTTS -.-> TTSLib
    
    %% Styling
    style Main fill:#FFE5B4
    style Webhook fill:#E6E6FA
    style Worker fill:#DDA0DD
    style RAGRetriever fill:#87CEEB
    style CreateDB fill:#87CEEB
    style RabbitMQ fill:#FF6B6B
    style Ollama fill:#90EE90
    style ChromaDB fill:#90EE90
    style GoogleAPI fill:#FFD700
    style WhatsAppAPI fill:#98FB98
    style PDFs fill:#F0E68C
    style VectorStore fill:#F0E68C
    style Audios fill:#F0E68C
```

## Módulos e Suas Responsabilidades

### 1. whatsapp_interface
**Responsabilidade**: Interface com WhatsApp e processamento inicial de mensagens

**Componentes:**
- `webhook.py`: Servidor Flask que recebe webhooks do WhatsApp
- `message_processor.py`: Classifica mensagens (texto/áudio)
- `audio_processor.py`: Processa mensagens de áudio (decodifica, salva)
- `text_processor.py`: Processa mensagens de texto
- `sender.py`: Envia respostas via WhatsApp API

**Dependências:**
- Flask (web framework)
- message_queue.publisher (publicar mensagens)
- audio_processsing.tts (gerar áudio)
- WhatsApp API externa

### 2. message_queue
**Responsabilidade**: Gerenciamento de filas assíncronas

**Componentes:**
- `publish_message.py`: Publica mensagens nas filas
- `worker.py`: Consome e processa mensagens das filas
- `config_queue.py`: Configura filas e exchanges no RabbitMQ

**Dependências:**
- Pika (cliente RabbitMQ)
- RabbitMQ (servidor de filas)
- rag.retriever (processar perguntas)
- audio_processsing.stt (transcrever áudio)
- whatsapp_interface.sender (enviar respostas)

### 3. audio_processsing
**Responsabilidade**: Processamento de áudio (STT e TTS)

**Componentes STT:**
- `speech_to_text.py`: Orquestra conversão de áudio para texto
- `audio_converter.py`: Converte OGG para WAV
- `speech_recognizer.py`: Reconhece fala usando Google API

**Componentes TTS:**
- `text_to_speech.py`: Gera áudio a partir de texto com clonagem de voz

**Dependências:**
- SpeechRecognition (biblioteca STT)
- Pydub (manipulação de áudio)
- TTS/Coqui (síntese de fala)
- Google Speech API (reconhecimento)

### 4. rag
**Responsabilidade**: Sistema RAG (Retrieval-Augmented Generation)

**Componentes:**
- `retriever.py`: Modelo RAG que busca contexto e gera respostas
- `create_database/create.py`: Cria vector store a partir de PDFs

**Dependências:**
- LangChain (framework LLM)
- Ollama (servidor LLM - llama3.2)
- ChromaDB (banco de dados vetorial)
- PDFs de conhecimento sobre diabetes

### 5. text_processing
**Responsabilidade**: Pré-processamento de texto (módulo auxiliar)

**Componentes:**
- `abreviation_dict.py`: Dicionário de abreviações
- `sentence_pre_processing.py`: Normalização de sentenças

**Dependências:** Nenhuma externa (módulo interno)

### 6. lab
**Responsabilidade**: Experimentos e testes isolados

**Componentes:**
- `lab/stt/main.py`: Teste de transcrição de áudio
- `lab/tts/main.py`: Teste de síntese de voz

**Dependências:** Mesmas dos módulos testados

## Dependências Externas

### Bibliotecas Python
1. **Flask**: Framework web para webhook
2. **Pika**: Cliente RabbitMQ para filas
3. **SpeechRecognition**: API de reconhecimento de fala
4. **Pydub**: Manipulação de arquivos de áudio
5. **TTS (Coqui)**: Síntese de voz com clonagem
6. **LangChain**: Framework para aplicações LLM
7. **PyPDF**: Leitura de PDFs

### Serviços Externos
1. **RabbitMQ**: Message broker para processamento assíncrono
2. **Ollama**: Servidor LLM local (modelo llama3.2)
3. **ChromaDB**: Banco de dados vetorial para embeddings
4. **Google Speech API**: Transcrição de áudio
5. **WhatsApp API (Evolution)**: Interface com WhatsApp

### Dados Persistentes
1. **PDFs sobre Diabetes**: Base de conhecimento (`rag/data/`)
2. **Vector Store**: Embeddings dos PDFs (`chroma_knowledge/`)
3. **Arquivos de Áudio**: Mensagens de voz salvas (`audios/`)

## Fluxo de Dependências

### Camada 1 - Interface
- WhatsApp API → Webhook → MessageProcessor

### Camada 2 - Roteamento
- Processors → Publisher → RabbitMQ

### Camada 3 - Processamento
- Worker consome de RabbitMQ
- Worker coordena: STT, RAG, Sender

### Camada 4 - Inteligência
- RAG → Vector DB (busca)
- RAG → LLM (geração)

### Camada 5 - Resposta
- Sender → TTS (opcional)
- Sender → WhatsApp API

## Acoplamento e Desacoplamento

**Baixo Acoplamento (Desacoplado via Filas):**
- Webhook ↔ Worker (via RabbitMQ)
- AudioProcessor ↔ SpeechToText (via fila audio_queue)
- TextProcessor ↔ RAGModel (via fila text_queue)

**Alto Acoplamento (Dependência Direta):**
- Worker → RAGModel (síncrono)
- RAGModel → LLM (síncrono)
- SpeechToText → Google API (síncrono)

**Componentes Reutilizáveis:**
- Publisher (usado por múltiplos processadores)
- Worker (processa múltiplas filas)
- RAGModel (pode ser usado standalone)
- STT/TTS (módulos independentes)
