from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

mcp_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_pipeline_run_status",
            "description": (
                "Fetch the live status of a data pipeline run from the monitoring system."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "pipeline_name": {
                        "type": "string",
                        "description": "Pipeline name (e.g., 'sales_ingestion')"
                    }
                },
                "required": ["pipeline_name"]
            }
        }
    }
]