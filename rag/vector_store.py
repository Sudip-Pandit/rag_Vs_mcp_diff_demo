from langchain_community.vectorstores import FAISS

class VectorStore:
    """
    Simple FAISS wrapper.
    Stores (chunk, embedding) pairs and supports similarity search.
    """

    def __init__(self, embeddings):
        self.embeddings = embeddings
        self.store = None

    def build(self, documents):
        self.store = FAISS.from_documents(documents, self.embeddings)

    def search(self, query, k=3):
        if not self.store:
            raise ValueError("Vector store not built yet.")
        return self.store.similarity_search(query, k=k)