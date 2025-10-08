# Diagrama de Fluxo

Este diagrama mostra o fluxo de execução do programa para diferentes cenários.

```plantuml
@startuml

title Fluxo de Execução - Assistente Virtual de Diabetes

|Usuário|
start
:Envia mensagem via WhatsApp;

|Evolution API|
:Recebe mensagem;
:Envia para webhook;

|Webhook Flask|
:Recebe POST /webhook;
:Extrai payload JSON;

|MessageProcessor|
:Classifica tipo de mensagem;

if (É mensagem de áudio?) then (sim)
    |AudioProcessor|
    :Extrai base64 do áudio;
    :Gera caminho de arquivo único;
    :Decodifica e salva arquivo OGG;
    :Publica caminho na audio_queue;
    
    |Worker Audio|
    :Consome mensagem da audio_queue;
    
    |SpeechToText|
    :Recebe caminho do áudio;
    
    |AudioConverter|
    :Converte OGG para WAV;
    
    |SpeechRecognizer|
    :Usa Google Speech API;
    :Reconhece texto em pt-BR;
    
    |Worker Audio|
    :Recebe texto transcrito;
    :Formata {number, message};
    :Publica na text_queue;
    
else (não)
    if (É mensagem de texto?) then (sim)
        |TextProcessor|
        :Extrai texto da mensagem;
        :Extrai número do remetente;
        :Formata {number, message};
        :Publica na text_queue;
    else (não)
        |MessageProcessor|
        :Retorna UNKNOWN;
        stop
    endif
endif

|Worker Text|
:Consome mensagem da text_queue;
:Parse JSON {number, message};

|RAGModel|
:Recebe pergunta do usuário;

partition "Processamento RAG" {
    :Cria embedding da pergunta;
    
    |Chroma VectorStore|
    :Busca top-5 documentos similares;
    :Retorna contexto relevante;
    
    |RAGModel|
    :Formata prompt com contexto;
    :Adiciona instruções do sistema;
    
    |Ollama LLM|
    :Processa com llama3.2;
    :Gera resposta personalizada;
    :Considera contexto médico;
    
    |RAGModel|
    :Valida resposta;
    :Adiciona fontes citadas;
    :Retorna resposta completa;
}

|Worker Text|
:Recebe resposta do RAG;

|WhatsAppSender|
:Prepara envio da resposta;

if (Enviar como áudio?) then (sim)
    |TextToSpeechGenerator|
    :Carrega modelo XTTS v2;
    :Sintetiza voz em português;
    :Salva áudio temporário;
    
    |WhatsAppSender|
    :Codifica áudio em base64;
    :Envia via Evolution API;
else (não)
    |WhatsAppSender|
    :Define delay aleatório (500-3000ms);
    :Envia mensagem de texto;
    :POST para Evolution API;
endif

|Evolution API|
:Envia resposta para WhatsApp;

|Usuário|
:Recebe resposta do assistente;
stop

@enduml
```

## Descrição do Fluxo

### 1. Recebimento da Mensagem
- Usuário envia mensagem (texto ou áudio) via WhatsApp
- Evolution API intercepta e encaminha para webhook Flask
- Webhook recebe POST com payload JSON

### 2. Classificação da Mensagem
- MessageProcessor identifica tipo de mensagem
- Redireciona para processador adequado (Audio/Text)

### 3. Processamento de Áudio (se aplicável)
- AudioProcessor salva arquivo OGG localmente
- Publica caminho na fila audio_queue
- Worker consome e inicia transcrição
- AudioConverter transforma OGG em WAV
- SpeechRecognizer usa Google API para transcrição
- Texto transcrito é publicado na text_queue

### 4. Processamento de Texto
- TextProcessor ou Worker Audio publica na text_queue
- Worker Text consome mensagem

### 5. Geração de Resposta (RAG)
- RAGModel recebe pergunta
- Cria embedding da pergunta (nomic-embed-text)
- Busca documentos similares no Chroma (k=5)
- Formata prompt com contexto e instruções
- Ollama (llama3.2) gera resposta contextualizada
- Resposta inclui fontes e orientações médicas

### 6. Envio da Resposta
- WhatsAppSender recebe resposta
- Opcionalmente converte texto em áudio (TTS)
- Envia via Evolution API
- Usuário recebe resposta no WhatsApp

## Características Importantes

### Processamento Assíncrono
- Uso de RabbitMQ para desacoplar componentes
- Filas separadas para áudio e texto
- Workers independentes e escaláveis

### Tratamento de Erros
- SpeechToText lida com erros de reconhecimento
- RAGModel tem fallbacks e validações
- Sistema continua operacional mesmo com falhas parciais

### Otimizações
- Conversão de áudio usa arquivos temporários
- Delay aleatório simula digitação humana
- Cache de embeddings no Chroma

### Segurança e Privacidade
- Áudios salvos localmente por data
- Processamento local (Ollama)
- Sem envio de dados sensíveis para nuvem
