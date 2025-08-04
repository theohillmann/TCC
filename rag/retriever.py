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
    MODEL_TEMPERATURE = 0
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
        return self.llm.invoke(msg)

    def format_docs(self, docs):
        out = []
        for i, d in enumerate(docs, 1):
            src = d.metadata.get("source", "doc")
            out.append(f"[{i}] {src}: {d.page_content[:800]}")
        return "\n\n".join(out)

    def _config(self):
        SYSTEM = """Você é um assistente que responde APENAS com base no contexto fornecido.
        Se a resposta não estiver no contexto, diga que não encontrou. Cite as fontes."""

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
    print(RAGModel().ask("Qual é o tratamento para Diabetes Mellitus tipo 2?"))
