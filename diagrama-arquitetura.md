# Diagrama de Arquitetura de Alto Nível

Este diagrama apresenta uma visão geral dos componentes principais do sistema de assistente virtual para diabetes via WhatsApp.

```plantuml
@startuml
!define RECTANGLE class

skinparam component {
    BackgroundColor<<external>> LightBlue
    BackgroundColor<<internal>> LightGreen
    BackgroundColor<<database>> LightYellow
    BorderColor Black
}

package "Interface Externa" {
    [WhatsApp] as whatsapp <<external>>
    [Evolution API] as evo <<external>>
}

package "Camada de Interface" {
    [Webhook Flask] as webhook
    [Message Processor] as msgproc
    [WhatsApp Sender] as sender
}

package "Fila de Mensagens" {
    database "RabbitMQ" as rabbitmq <<database>> {
        queue audio_queue
        queue text_queue
    }
    [Publisher] as pub
    [Workers] as workers
}

package "Processamento de Áudio" {
    [Speech-to-Text] as stt
    [Text-to-Speech] as tts
    component "AudioConverter" as converter
    component "SpeechRecognizer" as recognizer
}

package "Modelo RAG" {
    [RAG Model] as rag
    [LangChain] as langchain
    [Ollama LLM] as ollama
}

package "Base de Conhecimento" {
    database "Chroma Vector Store" as chroma <<database>>
    [Vector Store Creator] as creator
    [PDF Loader] as pdfloader
}

' Fluxo de dados
whatsapp --> evo : mensagens
evo --> webhook : HTTP POST
webhook --> msgproc : processa
msgproc --> pub : publica na fila

pub --> rabbitmq : enfileira mensagens

rabbitmq --> workers : consome mensagens

workers --> stt : áudio
stt --> converter : converte OGG
converter --> recognizer : WAV
recognizer --> workers : texto

workers --> rag : pergunta
rag --> langchain : processa
langchain --> ollama : gera resposta
langchain --> chroma : busca contexto
rag --> workers : resposta

workers --> sender : envia resposta
sender --> tts : gera áudio
sender --> evo : envia mensagem
evo --> whatsapp : entrega

pdfloader --> creator : PDFs
creator --> chroma : cria índice

note right of rabbitmq
  Exchange: message_exchange
  Routing keys: audio, text
end note

note right of ollama
  Modelo: llama3.2
  Embeddings: nomic-embed-text
end note

@enduml
```

## Descrição dos Componentes

### Interface Externa
- **WhatsApp**: Aplicativo de mensagens usado pelos usuários
- **Evolution API**: API intermediária para conexão com WhatsApp

### Camada de Interface
- **Webhook Flask**: Recebe mensagens via HTTP POST
- **Message Processor**: Classifica mensagens (áudio/texto)
- **WhatsApp Sender**: Envia respostas aos usuários

### Fila de Mensagens
- **RabbitMQ**: Sistema de filas para processamento assíncrono
- **Publisher**: Publica mensagens nas filas
- **Workers**: Processa mensagens das filas

### Processamento de Áudio
- **Speech-to-Text**: Converte áudio em texto
- **Text-to-Speech**: Converte texto em áudio
- **AudioConverter**: Converte OGG para WAV
- **SpeechRecognizer**: Reconhece fala usando Google API

### Modelo RAG
- **RAG Model**: Modelo de Geração Aumentada por Recuperação
- **LangChain**: Framework para LLM
- **Ollama LLM**: Modelo de linguagem local (llama3.2)

### Base de Conhecimento
- **Chroma Vector Store**: Banco vetorial para documentos
- **Vector Store Creator**: Cria índice de documentos
- **PDF Loader**: Carrega PDFs com informações sobre diabetes

## Tecnologias Utilizadas
- **Backend**: Python, Flask
- **Fila de Mensagens**: RabbitMQ (Pika)
- **LLM**: Ollama (llama3.2)
- **Embeddings**: nomic-embed-text
- **Vector DB**: Chroma
- **STT**: Google Speech Recognition
- **TTS**: Coqui TTS (XTTS v2)
- **Audio**: Pydub
