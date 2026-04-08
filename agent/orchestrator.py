class AgentOrchestrator:
    """
    Orchestrates between:
    - RAG retriever
    - MCP tools
    - LLM router

    This is the "brain" of the agent layer.
    """

    def __init__(self, router, rag_retriever, tools):
        self.router = router
        self.rag = rag_retriever
        self.tools = tools

    def handle_query(self, query: str) -> str:
        mode = self.router.classify(query)

        if mode == "rag":
            return self._handle_rag(query)

        if mode == "mcp":
            return self._handle_mcp(query)

        if mode == "hybrid":
            return self._handle_hybrid(query)

        return "I’m not sure how to answer that."

    # -------------------------
    # RAG ONLY
    # -------------------------
    def _handle_rag(self, query: str) -> str:
        docs = self.rag.retrieve(query)
        return (
            "[RAG ANSWER]\n"
            f"{docs}"
        )

    # -------------------------
    # MCP ONLY
    # -------------------------
    def _handle_mcp(self, query: str) -> str:
        result = self.tools.call(query)
        return (
            "[MCP ANSWER]\n"
            f"{result}"
        )

    # -------------------------
    # HYBRID (RAG + MCP)
    # -------------------------
    def _handle_hybrid(self, query: str) -> str:
        rag_part = self.rag.retrieve(query)
        mcp_part = self.tools.call(query)

        return (
            "[HYBRID ANSWER]\n\n"
            f"📘 Knowledge (RAG):\n{rag_part}\n\n"
            f"⚙️ Live Data (MCP):\n{mcp_part}"
        )