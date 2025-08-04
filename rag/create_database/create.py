from pathlib import Path
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class VectorStore:
    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 150
    EMBEDDING_MODEL = "nomic-embed-text"
    PERSIST_DIR = "../chroma_knowledge"
    DATA_DIR = ""

    def __init__(self):
        self.docs = []
        self.chunkd = []

    def create(self):
        self.load_pdfs()
        self.chunk_documents()
        self.create_vector_store()

    def load_pdfs(self):
        pdf_paths = ["../data/Diabetes Mellitus Quick Guide.pdf"]

        for pdf in pdf_paths:
            self.docs.extend(PyPDFLoader(pdf).load())

    def chunk_documents(self):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.CHUNK_SIZE, chunk_overlap=self.CHUNK_OVERLAP
        )
        self.chunks = splitter.split_documents(self.docs)

    def create_vector_store(self):
        embedding = OllamaEmbeddings(model=self.EMBEDDING_MODEL)

        Chroma.from_documents(
            documents=self.chunks,
            embedding=embedding,
            persist_directory=self.PERSIST_DIR,
        )
        print(
            f"Vector store created with {len(self.chunks)} chunks and saved to {self.PERSIST_DIR}"
        )


if __name__ == "__main__":
    VectorStore().create()
