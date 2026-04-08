from agent.openai_agent import pipeline_support_agent

# Query 1: Pure RAG — policy question only
pipeline_support_agent("What is our SLA for pipeline failures?")

# Query 2: Pure MCP — live data only
pipeline_support_agent("Did the sales_ingestion job fail last night?")

# Query 3: Hybrid — RAG + MCP combined
pipeline_support_agent("What's our SLA and did sales_ingestion breach it?")

# Query 4: MCP row count tool
pipeline_support_agent("Give me the row count for the customers table.")
