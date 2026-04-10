from langfuse import Langfuse
from app.config import get_settings
from functools import lru_cache


@lru_cache
def get_langfuse() -> Langfuse:
    s = get_settings()
    return Langfuse(
        public_key=s.langfuse_public_key,
        secret_key=s.langfuse_secret_key,
        host=s.langfuse_host,
    )


def trace_agent_run(query: str, session_id: str):
    lf = get_langfuse()
    return lf.trace(
        name="agentflow-run",
        input={"query": query},
        session_id=session_id,
    )
