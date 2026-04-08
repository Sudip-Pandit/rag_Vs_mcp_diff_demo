import random

def get_row_count(table_name: str) -> dict:
    """
    Fake MCP tool: returns a random row count.
    Simulates a warehouse query.
    """
    return {
        "table": table_name,
        "row_count": random.randint(50_000, 5_000_000)
    }