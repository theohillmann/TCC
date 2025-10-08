# Índice de Diagramas UML

Este documento lista todos os diagramas UML criados para o projeto TCC - Assistente Virtual de Diabetes via WhatsApp.

## Diagramas Disponíveis

### 1. [Diagrama de Arquitetura de Alto Nível](diagrama-arquitetura.md)
**Arquivo:** `diagrama-arquitetura.md`

Visão geral dos componentes principais do sistema, incluindo:
- Interface Externa (WhatsApp, Evolution API)
- Camada de Interface (Webhook, Processadores, Sender)
- Fila de Mensagens (RabbitMQ)
- Processamento de Áudio (STT, TTS)
- Modelo RAG (LangChain, Ollama)
- Base de Conhecimento (Chroma Vector Store)

### 2. [Diagrama de Classes UML](diagrama-classes.md)
**Arquivo:** `diagrama-classes.md`

Estrutura detalhada das classes e seus relacionamentos:
- Classes da interface WhatsApp
- Classes de processamento de mensagens
- Classes de áudio (STT/TTS)
- Classes do modelo RAG
- Enumerações e tipos
- Padrões de design utilizados

### 3. [Diagrama de Fluxo](diagrama-fluxo.md)
**Arquivo:** `diagrama-fluxo.md`

Fluxo de execução completo do programa:
- Recebimento de mensagens (áudio e texto)
- Classificação e roteamento
- Processamento de áudio (transcrição)
- Processamento RAG (busca + geração)
- Envio de respostas
- Tratamento de erros

### 4. [Diagrama de Sequência](diagrama-sequencia.md)
**Arquivo:** `diagrama-sequencia.md`

Interação entre componentes ao longo do tempo:
- Sequência completa: Mensagem de áudio
- Sequência simplificada: Mensagem de texto
- Sequência de criação da base de conhecimento
- Comunicação entre componentes e serviços externos

### 5. [Diagrama de Componentes](diagrama-componentes.md)
**Arquivo:** `diagrama-componentes.md`

Dependências entre módulos e bibliotecas:
- Módulos internos e suas relações
- Bibliotecas Python utilizadas
- Serviços externos (APIs, servidores)
- Armazenamento (arquivos e banco de dados)
- Fluxo de dependências por caso de uso

## Como Visualizar os Diagramas

Os diagramas foram criados usando **PlantUML**, uma linguagem de modelagem UML baseada em texto.

### Opção 1: Extensão VS Code
1. Instale a extensão "PlantUML" no VS Code
2. Abra qualquer arquivo `.md` com diagramas
3. Use `Alt+D` para visualizar o diagrama

### Opção 2: PlantUML Online
1. Acesse [PlantUML Web Server](http://www.plantuml.com/plantuml/uml/)
2. Copie o código entre ` ```plantuml` e ` ``` `
3. Cole no servidor para visualizar

### Opção 3: Linha de Comando
```bash
# Instalar PlantUML
sudo apt-get install plantuml

# Gerar imagem PNG de um diagrama
plantuml diagrama-arquitetura.md
```

### Opção 4: Plugin Markdown
Muitos visualizadores de Markdown (GitHub, GitLab, etc.) suportam renderização automática de diagramas PlantUML.

## Estrutura do Projeto

```
TCC/
├── diagrama-arquitetura.md      # Arquitetura de alto nível
├── diagrama-classes.md          # Classes UML
├── diagrama-fluxo.md            # Fluxo de execução
├── diagrama-sequencia.md        # Sequências de interação
├── diagrama-componentes.md      # Dependências de componentes
├── DIAGRAMAS.md                 # Este arquivo (índice)
├── whatsapp_interface/          # Interface com WhatsApp
├── message_queue/               # Sistema de filas
├── audio_processsing/           # Processamento de áudio
├── rag/                         # Modelo RAG
└── text_processing/             # Pré-processamento de texto
```

## Sobre o Projeto

**Nome:** TCC - Assistente Virtual de Diabetes via WhatsApp

**Descrição:** Sistema de assistente virtual para orientação sobre diabetes, utilizando:
- WhatsApp como interface de comunicação
- RAG (Retrieval-Augmented Generation) para respostas contextualizadas
- Processamento de áudio bidirecional (STT e TTS)
- Base de conhecimento criada a partir de documentos sobre diabetes
- Arquitetura assíncrona com filas de mensagens

**Tecnologias Principais:**
- Python, Flask, RabbitMQ
- LangChain, Ollama (llama3.2)
- Chroma Vector Database
- Google Speech Recognition
- Coqui TTS (XTTS v2)

## Observações

- Todos os diagramas foram criados seguindo o padrão UML 2.0
- Os diagramas são mantidos em arquivos separados para facilitar a manutenção
- Cada diagrama inclui descrições e notas explicativas
- Os diagramas refletem a estrutura atual do código (2025)
