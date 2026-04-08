import re

class LLMRouter:
    """
    A lightweight classifier that decides whether a query needs:
    - RAG (knowledge retrieval)
    - MCP (live tool call)
    - HYBRID (both)
    """

    def classify(self, query: str) -> str:
        q = query.lower()

        # Keywords that imply live system checks (MCP)
        mcp_keywords = [
            "status", "failed", "running", "breach",
            "row count", "records", "live", "today",
            "last night", "trigger", "restart", "job"
        ]

        # Keywords that imply knowledge lookup (RAG)
        rag_keywords = [
            "what is", "explain", "policy", "runbook",
            "sla", "documentation", "standard", "definition"
        ]

        needs_mcp = any(k in q for k in mcp_keywords)
        needs_rag = any(k in q for k in rag_keywords)

        if needs_mcp and needs_rag:
            return "hybrid"
        if needs_mcp:
            return "mcp"
        if needs_rag:
            return "rag"

        return "unknown"