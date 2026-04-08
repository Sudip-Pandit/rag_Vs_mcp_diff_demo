LIVE_JOB_RUNS = {
    "sales_ingestion": {
        "run_id": "run_20240407_001",
        "status": "FAILED",
        "duration_minutes": 312,
        "failure_reason": "Timeout after 5 hours 12 minutes",
        "records_processed": 1_840_000,
        "failure_rate_pct": 0.8,
        "retries": 3,
        "last_run": "2024-04-07 02:15:00"
    },
    "inventory_sync": {
        "run_id": "run_20240407_002",
        "status": "SUCCESS",
        "duration_minutes": 87,
        "failure_rate_pct": 0.1,
        "records_processed": 540_000,
        "retries": 0,
        "last_run": "2024-04-07 03:42:00"
    },
    "customer_360": {
        "run_id": "run_20240407_003",
        "status": "RUNNING",
        "duration_minutes": 220,
        "failure_rate_pct": None,
        "records_processed": 920_000,
        "retries": 1,
        "last_run": "2024-04-07 01:00:00"
    }
}

def get_pipeline_run_status(pipeline_name: str) -> dict:
    """
    Fake MCP tool: returns live pipeline status.
    In production, replace with Databricks / Airflow / REST API.
    """
    key = pipeline_name.lower().replace(" ", "_")
    return LIVE_JOB_RUNS.get(key, {"error": f"Pipeline not found: {pipeline_name}"})