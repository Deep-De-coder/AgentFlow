"""
Small RAG corpus — GCP and AI agent topics.
Extend this for a richer demo.
"""

SAMPLE_DOCUMENTS = [
    {
        "content": (
            "Cloud Run is a fully managed serverless platform on Google Cloud "
            "that automatically scales stateless containers. It supports any "
            "language or framework, charges only for actual use, and integrates "
            "natively with other GCP services like Cloud Build, Artifact Registry, "
            "and Secret Manager."
        ),
        "metadata": {"source": "gcp_cloud_run", "topic": "infrastructure"},
    },
    {
        "content": (
            "Supabase is an open-source Firebase alternative built on PostgreSQL. "
            "It provides a REST API, realtime subscriptions, authentication, and "
            "storage. The pgvector extension enables storing and querying vector "
            "embeddings directly in Postgres, making it suitable for RAG pipelines."
        ),
        "metadata": {"source": "supabase_docs", "topic": "database"},
    },
    {
        "content": (
            "LangGraph is a library for building stateful, multi-agent workflows "
            "using a graph-based execution model. Nodes represent agent actions or "
            "tool calls, edges define routing logic, and the state object is passed "
            "between nodes. It supports cycles, conditional branching, and "
            "human-in-the-loop patterns."
        ),
        "metadata": {"source": "langgraph_docs", "topic": "agents"},
    },
    {
        "content": (
            "The ReAct (Reason + Act) pattern for LLM agents interleaves reasoning "
            "steps with action execution. The agent produces a Thought about what "
            "to do, selects an Action (tool call), receives an Observation, and "
            "repeats until it can produce a final Answer. This pattern reduces "
            "hallucination by grounding reasoning in tool results."
        ),
        "metadata": {"source": "react_paper", "topic": "agents"},
    },
    {
        "content": (
            "Langfuse is an open-source LLM observability platform. It captures "
            "traces, spans, generations, and scores for LLM applications. The free "
            "tier supports unlimited traces with 30-day retention. It integrates "
            "with LangChain via a callback handler and supports manual "
            "instrumentation via the Python SDK."
        ),
        "metadata": {"source": "langfuse_docs", "topic": "observability"},
    },
    {
        "content": (
            "Gemini is Google's multimodal AI model family. Gemini 1.5 Flash "
            "is optimized for speed and cost efficiency, supporting a 1M token "
            "context window. It is available via Google AI Studio and Vertex AI. "
            "The free tier through Google AI Studio allows up to 15 requests per "
            "minute and 1 million tokens per day."
        ),
        "metadata": {"source": "gemini_docs", "topic": "llm"},
    },
]
