import json
import os
import glob
from agent.openai_client import client, mcp_tools
from tools.pipeline_status import get_pipeline_run_status
from rag import RAGRetriever

# ── Initialize RAG once at module load ──────────────────────────
# Reads all .md files from the data/ folder and indexes them

def _load_data_docs() -> str:
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    md_files = glob.glob(os.path.join(data_dir, "*.md"))
    if not md_files:
        raise FileNotFoundError(f"No .md files found in {data_dir}")
    combined = []
    for path in sorted(md_files):
        with open(path, "r") as f:
            combined.append(f.read())
    print(f"[RAG] Loaded {len(md_files)} doc(s) from data/")
    return "\n\n".join(combined)

_rag = RAGRetriever()
_rag.index(_load_data_docs())

# ── Agent ────────────────────────────────────────────────────────

def pipeline_support_agent(user_query: str):
    print(f"\n{'='*60}")
    print(f"USER QUERY: {user_query}")
    print(f"{'='*60}\n")

    # Step 1: RAG — retrieve relevant policy context
    policy_context = _rag.retrieve(user_query)
    print(f"[RAG] Retrieved policy context:\n{policy_context}\n")
    print("-" * 40)

    system_prompt = """
You are a data engineering support agent with two capabilities:
1. You know internal pipeline policies (context provided below).
2. You can call live monitoring tools to check real pipeline run data.

Rules:
- If the question requires policy/SLA knowledge: use the provided context.
- If it requires live pipeline status: call the get_pipeline_run_status tool.
- If it requires BOTH: do both, then synthesize a single clear answer.
- Always be specific. If an SLA was breached, state it clearly with numbers.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                f"Policy & Runbook Context (from internal docs):\n"
                f"---\n{policy_context}\n---\n\n"
                f"User Question: {user_query}\n\n"
                f"Answer this question. Use the tool if you need live pipeline data."
            )
        }
    ]

    # Step 2: First LLM call — may trigger a tool call
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
        tools=mcp_tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # Step 3: Handle tool call if triggered
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        pipeline_name = args["pipeline_name"]

        print(f"[MCP] Tool called: {tool_call.function.name}")
        print(f"[MCP] Pipeline: {pipeline_name}")

        tool_result = get_pipeline_run_status(pipeline_name)
        print(f"[MCP] Live result: {json.dumps(tool_result, indent=2)}\n")
        print("-" * 40)

        # Feed tool result back for final synthesis
        messages.append(message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_result)
        })

        final = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages
        )

        print(f"[AGENT ANSWER]\n{final.choices[0].message.content}")
        return

    # Pure RAG answer — no tool needed
    print(f"[AGENT ANSWER]\n{message.content}")
