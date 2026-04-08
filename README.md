# rag_vs_mcp_demo

A working local demo of a Data Pipeline Support Agent that combines:
- **RAG** — retrieves policy knowledge from internal `.md` docs
- **MCP-style tool calls** — fetches live pipeline status via OpenAI function calling

---

## Project Structure

```
rag_vs_mcp_demo/
├── agent/
│   ├── __init__.py
│   ├── llm_router.py        # Keyword-based RAG/MCP/hybrid classifier
│   ├── openai_agent.py      # Main agent: RAG + OpenAI tool calling
│   ├── openai_client.py     # OpenAI client + tool schema
│   └── orchestrator.py      # Keyword-based orchestrator (no LLM)
├── rag/
│   ├── __init__.py
│   ├── embedder.py          # HuggingFace embeddings wrapper
│   ├── retriever.py         # Chunk → embed → FAISS → retrieve
│   └── vector_store.py      # FAISS wrapper
├── tools/
│   ├── __init__.py
│   ├── fake_api.py          # Simulated latency + failures
│   ├── pipeline_status.py   # Fake live pipeline status data
│   ├── router.py            # Tool dispatcher
│   └── row_count.py         # Fake row count tool
├── data/
│   ├── runbook_sla.md
│   ├── dataquality_standards.md
│   └── oncall_responsibilities.md
├── examples/
│   └── demo_query.py        # Run this to test all 4 queries
├── .env.example
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone / copy this project to your machine

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> First run downloads the `all-MiniLM-L6-v2` embedding model (~80MB). Cached after that.

### 4. Set your OpenAI API key

```bash
cp .env.example .env
# Then open .env and paste your key:
# OPENAI_API_KEY=sk-...
```

---

## Run

Always run from the **project root** (not from inside `examples/`):

```bash
cd rag_vs_mcp_demo
python -m examples.demo_query
```

---

## What Each Query Tests

| Query | Mode | What happens |
|---|---|---|
| "What is our SLA for pipeline failures?" | RAG only | Retrieves from runbook_sla.md |
| "Did the sales_ingestion job fail last night?" | MCP only | Calls get_pipeline_run_status tool |
| "What's our SLA and did sales_ingestion breach it?" | Hybrid | RAG + tool call, one unified answer |
| "Give me the row count for the customers table." | MCP only | Calls get_row_count tool |

---

## Notes

- No Databricks or Airflow needed — all live data is simulated in `tools/pipeline_status.py`
- To add real pipelines: replace `LIVE_JOB_RUNS` dict with a real API call
- To add more docs: drop `.md` files into `data/` — they are auto-loaded at startup
