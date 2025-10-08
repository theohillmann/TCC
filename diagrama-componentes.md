# Diagrama de Componentes

Este diagrama mostra as dependências entre módulos e bibliotecas externas do sistema.

```plantuml
@startuml

!define COMPONENT_FONT_SIZE 12

skinparam component {
    BackgroundColor<<main>> LightGreen
    BackgroundColor<<external>> LightBlue
    BackgroundColor<<library>> LightYellow
    BorderColor Black
    FontSize COMPONENT_FONT_SIZE
}

package "Sistema Principal" <<main>> {
    
    component [main.py] as MAIN
    
    package "whatsapp_interface" {
        component [webhook.py] as WEBHOOK
        component [sender.py] as SENDER
        
        package "processors" {
            component [message_processor.py] as MSG_PROC
            component [audio_processor.py] as AUDIO_PROC
            component [text_processor.py] as TEXT_PROC
        }
        
        package "models" {
            component [message_type.py] as MSG_TYPE
        }
    }
    
    package "message_queue" {
        component [config_queue.py] as CONFIG_Q
        component [worker.py] as WORKER
        
        package "publisher" {
            component [publish_message.py] as PUBLISHER
        }
    }
    
    package "audio_processsing" {
        component [__init__.py] as AUDIO_INIT
        
        package "stt" {
            component [speech_to_text.py] as STT
            component [audio_converter.py] as CONVERTER
            component [speech_recognizer.py] as RECOGNIZER
        }
        
        package "tts" {
            component [text_to_speech.py] as TTS
        }
    }
    
    package "rag" {
        component [retriever.py] as RAG
        
        package "create_database" {
            component [create.py] as VECTOR_CREATE
        }
    }
    
    package "text_processing" {
        package "pre_processing" {
            component [sentence_pre_processing.py] as PREPROC
            component [abreviation_dict.py] as ABBREV
        }
    }
}

package "Bibliotecas Python" <<library>> {
    component [Flask] as FLASK
    component [Pika (RabbitMQ)] as PIKA
    component [LangChain] as LANGCHAIN
    component [Ollama] as OLLAMA
    component [Chroma] as CHROMA
    component [SpeechRecognition] as SR
    component [Pydub] as PYDUB
    component [Coqui TTS] as COQUI
    component [PyTorch] as TORCH
    component [Requests] as REQUESTS
}

package "Serviços Externos" <<external>> {
    component [RabbitMQ Server] as RABBITMQ
    component [Ollama Server] as OLLAMA_SRV
    component [Evolution API] as EVOLUTION
    component [Google Speech API] as GOOGLE_API
    component [WhatsApp] as WHATSAPP
}

database "Armazenamento" {
    folder [chroma_knowledge/] as CHROMA_DB
    folder [audios/] as AUDIO_FILES
    folder [data/ (PDFs)] as PDF_DATA
}

' Dependências Webhook
WEBHOOK --> FLASK
WEBHOOK --> MSG_PROC
MSG_PROC --> AUDIO_PROC
MSG_PROC --> TEXT_PROC
MSG_PROC --> MSG_TYPE

' Dependências Processadores
AUDIO_PROC --> PUBLISHER
TEXT_PROC --> PUBLISHER
PUBLISHER --> PIKA

' Dependências Worker
WORKER --> PIKA
WORKER --> STT
WORKER --> RAG
WORKER --> SENDER

' Dependências Audio Processing
STT --> CONVERTER
STT --> RECOGNIZER
CONVERTER --> PYDUB
RECOGNIZER --> SR
AUDIO_INIT ..> STT

SENDER --> TTS
TTS --> COQUI
TTS --> TORCH
SENDER --> REQUESTS

' Dependências RAG
RAG --> LANGCHAIN
RAG --> OLLAMA
RAG --> CHROMA
VECTOR_CREATE --> LANGCHAIN
VECTOR_CREATE --> OLLAMA
VECTOR_CREATE --> CHROMA

' Dependências Config
CONFIG_Q --> PIKA

' Conexões com Serviços Externos
PIKA ..> RABBITMQ : <<conecta>>
OLLAMA ..> OLLAMA_SRV : <<conecta>>
SENDER ..> EVOLUTION : <<HTTP>>
SR ..> GOOGLE_API : <<API>>
EVOLUTION ..> WHATSAPP : <<conecta>>

' Conexões com Armazenamento
AUDIO_PROC ..> AUDIO_FILES : <<salva>>
STT ..> AUDIO_FILES : <<lê>>
CHROMA ..> CHROMA_DB : <<persiste>>
VECTOR_CREATE ..> PDF_DATA : <<lê>>

note right of WEBHOOK
  Ponto de entrada do sistema
  Recebe POST /webhook
end note

note right of PUBLISHER
  Publica mensagens em:
  - audio_queue
  - text_queue
end note

note right of WORKER
  Processa filas:
  - audio_queue
  - text_queue
  
  Múltiplas instâncias
  podem rodar em paralelo
end note

note right of RAG
  Geração Aumentada por Recuperação
  - Busca contexto no Chroma
  - Gera resposta com Ollama
  - Modelo: llama3.2
  - Embeddings: nomic-embed-text
end note

note bottom of CHROMA_DB
  Base de conhecimento vetorial
  Criada a partir dos PDFs
  sobre diabetes
end note

note right of EVOLUTION
  API intermediária para WhatsApp
  Gerencia instância "bete"
end note

@enduml
```

## Dependências Detalhadas

### Módulo: whatsapp_interface

**Dependências Internas:**
- `webhook.py` → `message_processor.py`
- `message_processor.py` → `audio_processor.py`, `text_processor.py`, `message_type.py`
- `audio_processor.py` → `message_queue.publisher`
- `text_processor.py` → `message_queue.publisher`
- `sender.py` → `audio_processsing.tts`

**Dependências Externas:**
- Flask (servidor web)
- Requests (chamadas HTTP)
- Evolution API (serviço)

**Propósito:**
Interface com WhatsApp, recebendo e enviando mensagens

---

### Módulo: message_queue

**Dependências Internas:**
- `worker.py` → `audio_processsing.stt`, `rag.retriever`, `whatsapp_interface.sender`
- `publish_message.py` → Pika

**Dependências Externas:**
- Pika (cliente RabbitMQ)
- RabbitMQ Server (serviço)

**Propósito:**
Sistema de filas para processamento assíncrono e desacoplado

**Configuração:**
- Exchange: `message_exchange` (tipo: direct)
- Filas: `audio_queue`, `text_queue`
- Routing keys: `audio`, `text`

---

### Módulo: audio_processsing

**Dependências Internas:**
- `speech_to_text.py` → `audio_converter.py`, `speech_recognizer.py`

**Dependências Externas:**
- Pydub (manipulação de áudio)
- SpeechRecognition (reconhecimento de fala)
- Coqui TTS (síntese de voz)
- PyTorch (backend para TTS)
- Google Speech API (serviço)
- FFmpeg (dependência do Pydub)

**Propósito:**
Conversão bidirecional entre áudio e texto

**Formatos:**
- Entrada: OGG (WhatsApp)
- Intermediário: WAV (processamento)
- Saída TTS: WAV

---

### Módulo: rag

**Dependências Internas:**
- `retriever.py` → LangChain, Ollama, Chroma
- `create_database/create.py` → LangChain, Ollama, Chroma

**Dependências Externas:**
- LangChain (orquestração LLM)
- langchain_ollama (integração Ollama)
- langchain_chroma (integração Chroma)
- langchain_community (loaders)
- Ollama Server (serviço)

**Propósito:**
Sistema RAG para respostas contextualizadas sobre diabetes

**Configurações:**
- Modelo LLM: llama3.2
- Embeddings: nomic-embed-text
- Vector DB: Chroma
- Top-K: 5 documentos
- Temperature: 0.5

---

### Módulo: text_processing

**Dependências Internas:**
- `sentence_pre_processing.py` → `abreviation_dict.py`

**Dependências Externas:**
- Nenhuma

**Propósito:**
Pré-processamento de texto (normalização, abreviações)

---

## Fluxo de Dependências por Caso de Uso

### Caso 1: Mensagem de Áudio Recebida
```
WhatsApp → Evolution API → webhook.py (Flask)
  → message_processor.py → audio_processor.py
  → publish_message.py (Pika) → RabbitMQ
  → worker.py → speech_to_text.py
  → audio_converter.py (Pydub)
  → speech_recognizer.py (SpeechRecognition + Google API)
  → publish_message.py → RabbitMQ
  → worker.py → retriever.py (RAG)
  → Chroma + Ollama
  → sender.py → Evolution API → WhatsApp
```

### Caso 2: Mensagem de Texto Recebida
```
WhatsApp → Evolution API → webhook.py
  → message_processor.py → text_processor.py
  → publish_message.py → RabbitMQ
  → worker.py → retriever.py (RAG)
  → Chroma + Ollama
  → sender.py → Evolution API → WhatsApp
```

### Caso 3: Criação da Base de Conhecimento
```
create.py → PyPDFLoader → RecursiveCharacterTextSplitter
  → OllamaEmbeddings (nomic-embed-text)
  → Chroma.from_documents
  → chroma_knowledge/
```

## Interfaces Externas

### HTTP APIs
- **Evolution API**: Envio/recebimento de mensagens WhatsApp
- **Google Speech API**: Transcrição de áudio

### Serviços de Rede
- **RabbitMQ**: Message broker (localhost:5672)
- **Ollama**: LLM server (localhost:11434)
- **Evolution API**: WhatsApp gateway (localhost:8080)

### Sistema de Arquivos
- **audios/**: Mensagens de áudio recebidas
- **data/**: PDFs fonte para base de conhecimento
- **chroma_knowledge/**: Base vetorial persistida

## Requisitos de Instalação

### Python Packages (pyproject.toml)
```toml
[dependencies]
flask
pika
langchain
langchain-ollama
langchain-chroma
langchain-community
speechrecognition
pydub
TTS
torch
requests
```

### Serviços Externos Necessários
1. **RabbitMQ**: `docker run -d -p 5672:5672 rabbitmq`
2. **Ollama**: `ollama serve` + `ollama pull llama3.2`
3. **Evolution API**: Servidor WhatsApp
4. **FFmpeg**: Para Pydub funcionar

### Configuração
- Variáveis de ambiente (.env): `AUTHENTICATION_API_KEY`
- Arquivos de configuração: Prompts do RAG em retriever.py
- Estrutura de pastas: audios/, data/, chroma_knowledge/
