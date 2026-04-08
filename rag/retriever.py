from langchain.text_splitter import RecursiveCharacterTextSplitter
from .embedder import Embedder
from .vector_store import VectorStore

class RAGRetriever:
    """
    End-to-end RAG pipeline:
    - split documents
    - embed chunks
    - store in FAISS
    - retrieve top-k chunks
    """

    def __init__(self, chunk_size=300, chunk_overlap=30):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        self.embedder = Embedder()
        self.vectorstore = VectorStore(self.embedder.model)

    def index(self, raw_text: str):
        """Split + embed + store."""
        chunks = self.splitter.create_documents([raw_text])
        self.vectorstore.build(chunks)

    def retrieve(self, query: str) -> str:
        """Return top-k chunks as a single string."""
        docs = self.vectorstore.search(query, k=3)
        return "\n\n".join([doc.page_content for doc in docs])