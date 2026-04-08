from langchain_community.embeddings import HuggingFaceEmbeddings

class Embedder:
    """
    Thin wrapper around HuggingFace embeddings.
    Easy to swap out later.
    """

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = HuggingFaceEmbeddings(model_name=model_name)

    def embed(self, texts):
        return self.model.embed_documents(texts)

    def embed_query(self, text):
        return self.model.embed_query(text)