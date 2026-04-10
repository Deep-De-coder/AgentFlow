from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agents.orchestrator import run_agent
from app.config import get_settings
import logging

logging.basicConfig(level=get_settings().log_level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AgentFlow",
    description="LangGraph ReAct agent with RAG + web search on GCP",
    version="0.1.0",
)


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    answer: str
    session_id: str
    trace_id: str
    steps: int


@app.get("/health")
async def health():
    return {"status": "ok", "service": "agentflow"}


@app.post("/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    try:
        result = await run_agent(request.query)
        return QueryResponse(**result)
    except Exception as e:
        logger.error(f"Agent run failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {
        "service": "AgentFlow",
        "version": "0.1.0",
        "endpoints": {
            "query": "POST /query",
            "health": "GET /health",
            "docs": "GET /docs",
        },
    }
