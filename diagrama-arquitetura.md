# Diagrama de Arquitetura de Alto Nível

Este diagrama apresenta uma visão geral dos componentes principais do sistema de telemedicina via WhatsApp com foco em diabetes.

```mermaid
graph TB
    subgraph "Interface Externa"
        WA[WhatsApp API]
        User[Usuário]
    end
    
    subgraph "Camada de Entrada"
        Webhook[Flask Webhook<br/>whatsapp_interface/webhook.py]
        MP[Message Processor<br/>processors/message_processor.py]
    end
    
    subgraph "Processadores de Mensagem"
        TP[Text Processor<br/>processors/text_processor.py]
        AP[Audio Processor<br/>processors/audio_processor.py]
    end
    
    subgraph "Message Queue - RabbitMQ"
        Publisher[Publisher<br/>message_queue/publisher]
        Exchange[Message Exchange<br/>Direct]
        TQ[Text Queue]
        AQ[Audio Queue]
        Worker[Worker<br/>message_queue/worker]
    end
    
    subgraph "Processamento de Áudio"
        STT[Speech-to-Text<br/>audio_processsing/stt]
        AC[Audio Converter<br/>OGG → WAV]
        SR[Speech Recognizer<br/>Google API]
    end
    
    subgraph "Inteligência Artificial"
        RAG[RAG Model<br/>rag/retriever.py]
        LLM[LLM Ollama<br/>llama3.2]
        VectorDB[Vector Database<br/>Chroma DB]
        Embed[Embeddings<br/>nomic-embed-text]
    end
    
    subgraph "Geração de Resposta"
        TTS[Text-to-Speech<br/>audio_processsing/tts]
        Sender[WhatsApp Sender<br/>sender/sender.py]
    end
    
    subgraph "Base de Conhecimento"
        PDF[PDFs sobre Diabetes<br/>rag/data/]
        VSCR[Vector Store Creator<br/>create_database/create.py]
    end
    
    User -->|Mensagem| WA
    WA -->|Webhook POST| Webhook
    Webhook --> MP
    MP -->|Classifica| TP
    MP -->|Classifica| AP
    
    TP -->|Publica| Publisher
    AP -->|Salva áudio<br/>e publica| Publisher
    
    Publisher -->|routing_key: text| Exchange
    Publisher -->|routing_key: audio| Exchange
    Exchange --> TQ
    Exchange --> AQ
    
    AQ -->|Consome| Worker
    TQ -->|Consome| Worker
    
    Worker -->|Áudio| STT
    STT --> AC
    AC --> SR
    SR -->|Texto transcrito| Worker
    Worker -->|Publica texto| Publisher
    
    Worker -->|Pergunta| RAG
    RAG -->|Busca contexto| VectorDB
    VectorDB -->|Documentos relevantes| RAG
    RAG -->|Consulta| LLM
    RAG -->|Usa| Embed
    LLM -->|Resposta| RAG
    RAG -->|Resposta| Worker
    
    Worker -->|Resposta| Sender
    Sender -->|Texto/Áudio| WA
    WA -->|Resposta| User
    
    PDF -->|Carrega e<br/>processa| VSCR
    VSCR -->|Cria embeddings| VectorDB
    
    style RAG fill:#e1f5ff
    style LLM fill:#e1f5ff
    style VectorDB fill:#e1f5ff
    style Embed fill:#e1f5ff
    style Webhook fill:#fff4e1
    style Worker fill:#f0e1ff
    style STT fill:#e1ffe1
    style TTS fill:#e1ffe1
```

## Componentes Principais

1. **Interface Externa**: WhatsApp API para comunicação com usuários
2. **Camada de Entrada**: Flask webhook que recebe e classifica mensagens
3. **Processadores**: Processam mensagens de texto e áudio
4. **Message Queue**: RabbitMQ gerencia filas assíncronas (audio_queue e text_queue)
5. **Processamento de Áudio**: Converte áudio OGG para WAV e transcreve usando Google Speech API
6. **Inteligência Artificial**: RAG (Retrieval-Augmented Generation) com LLM Llama3.2 e Chroma DB
7. **Geração de Resposta**: Converte texto em áudio e envia via WhatsApp
8. **Base de Conhecimento**: PDFs processados e armazenados como embeddings no Chroma DB

## Fluxo de Dados

1. Usuário envia mensagem (texto ou áudio) via WhatsApp
2. Webhook recebe e classifica a mensagem
3. Mensagem é publicada na fila apropriada (text_queue ou audio_queue)
4. Worker consome a mensagem
5. Se áudio, converte e transcreve para texto
6. RAG busca contexto relevante no Vector DB
7. LLM gera resposta baseada no contexto
8. Resposta é enviada de volta ao usuário via WhatsApp
