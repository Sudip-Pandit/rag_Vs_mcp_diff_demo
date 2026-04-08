from .pipeline_status import get_pipeline_run_status
from .row_count import get_row_count
from .fake_api import simulate_latency, simulate_failure

class ToolsRouter:
    """
    MCP-style tool router.
    The agent calls: tools.call(query)
    """

    def call(self, query: str) -> str:
        q = query.lower()

        try:
            simulate_latency()
            simulate_failure(probability=0.05)

            # Pipeline status queries
            if "pipeline" in q or "job" in q or "status" in q:
                name = self._extract_pipeline_name(q)
                return get_pipeline_run_status(name)

            # Row count queries
            if "row count" in q or "records" in q:
                table = self._extract_table_name(q)
                return get_row_count(table)

            return {"error": "No matching tool found for query."}

        except Exception as e:
            return {"error": str(e)}

    # -------------------------
    # Helpers
    # -------------------------
    def _extract_pipeline_name(self, q: str) -> str:
        # naive extraction for demo purposes
        for name in ["sales_ingestion", "inventory_sync", "customer_360"]:
            if name.replace("_", " ") in q or name in q:
                return name
        return "sales_ingestion"

    def _extract_table_name(self, q: str) -> str:
        # naive extraction for demo purposes
        for name in ["orders", "customers", "inventory"]:
            if name in q:
                return name
        return "orders"