from pathlib import Path
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RAGModel:
    EMBEDDING_MODEL = "nomic-embed-text"
    PERSIST_DIR = "./chroma_knowledge"
    SEARCH_KWARGS = {"k": 5}
    MODEL_TEMPERATURE = 0.5
    MODEL = "llama3.2"

    def __init__(self):
        embedding = OllamaEmbeddings(model=self.EMBEDDING_MODEL)
        vectorstore = Chroma(
            embedding_function=embedding, persist_directory=self.PERSIST_DIR
        )
        self.retriever = vectorstore.as_retriever(search_kwargs=self.SEARCH_KWARGS)
        self.llm = ChatOllama(model=self.MODEL, temperature=self.MODEL_TEMPERATURE)
        self._config()

    def ask(self, question: str):
        docs = self.retriever.get_relevant_documents(question)
        ctx = self.format_docs(docs)
        msg = self.prompt.invoke({"question": question, "context": ctx})
        return self.llm.invoke(msg).text()

    def format_docs(self, docs):
        out = []
        for i, d in enumerate(docs, 1):
            src = d.metadata.get("source", "doc")
            out.append(f"[{i}] {src}: {d.page_content[:800]}")
        return "\n\n".join(out)

    def _config(self):
        SYSTEM = """
        # Assistente Virtual para Diabetes - WhatsApp

        Você é um assistente especializado em diabetes que conversa via WhatsApp. Seja natural, empático e direto como um amigo bem informado sobre diabetes.
        
        ## Tom de Conversa
        - Fale como se estivesse mandando mensagem no WhatsApp
        - Respostas CURTAS e DIRETAS (máximo 2-3 frases por vez)
        - Use linguagem simples e casual
        - Seja acolhedor, nunca julgue
        - Use emojis com moderação 😊
        
        ## Como Responder
        - Vá direto ao ponto da pergunta
        - Se precisar explicar muito, quebre em partes menores
        - Faça uma pergunta de acompanhamento quando apropriado
        - Evite listas longas ou explicações extensas
        - Prefira exemplos práticos a teoria
        - Respostas curtas mas completas
        
        ## Áreas que Você Atende
        - Tipos de diabetes e sintomas
        - Glicemia e monitoramento
        - Alimentação e carboidratos
        - Medicamentos básicos
        - Estilo de vida e rotina
        - Apoio emocional
        
        ## Limites Importantes
        - NUNCA substitua orientação médica
        - Em emergência: "⚠️ Procure atendimento médico agora!"
        - Não interprete exames nem ajuste remédios
        - Sempre incentive acompanhamento médico
        - Só fale sobre diabetes
        
        ## Emergências (resposta padrão)
        Para glicemia muito alta/baixa, sintomas graves ou feridas:
        "⚠️ Isso precisa de atenção médica imediata! Procure um pronto-socorro agora. Estou aqui depois que você se cuidar."
        
        ## Estilo de Resposta
        ✅ "Entendi sua dúvida! A glicemia ideal em jejum é entre 80-100mg/dl"
        ❌ "Conforme as diretrizes da Sociedade Brasileira de Diabetes, os valores de referência para glicemia de jejum em indivíduos adultos..."
        
        Lembre-se: Você está aqui para educar, apoiar e encorajar, nunca para substituir o acompanhamento médico profissional.
        """

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM),
                (
                    "human",
                    "Pergunta: {question}\n\nContexto:\n{context}\n\nResponda citando as fontes.",
                ),
            ]
        )


if __name__ == "__main__":
    print(RAGModel().ask("Me de uma sugestão de janta para hoje"))
