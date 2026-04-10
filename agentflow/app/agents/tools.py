from langchain_core.tools import tool
from app.rag.retriever import retrieve
from serpapi import GoogleSearch
from app.config import get_settings


@tool
def rag_search(query: str) -> str:
    """
    Search the internal document store for relevant context.
    Use this for questions about GCP, LangGraph, Supabase,
    Langfuse, Gemini, or agent architecture.

    Args:
        query: Natural language search query.

    Returns:
        Relevant document chunks as a single string.
    """
    results = retrieve(query, k=4)
    if not results:
        return "No relevant documents found."
    return "\n\n---\n\n".join(
        f"Source: {r['metadata'].get('source', 'unknown')}\n{r['content']}"
        for r in results
    )


@tool
def web_search(query: str) -> str:
    """
    Search the web for current information not in the
    internal document store. Use for recent events,
    specific facts, or anything outside the RAG corpus.

    Args:
        query: Natural language search query.

    Returns:
        Top web search results as a single string.
    """
    s = get_settings()
    search = GoogleSearch({
        "q": query,
        "api_key": s.serpapi_key,
        "num": 5,
    })
    results = search.get_dict()
    organic = results.get("organic_results", [])
    if not organic:
        return "No web results found."
    return "\n\n---\n\n".join(
        f"Title: {r.get('title', '')}\n"
        f"URL: {r.get('link', '')}\n"
        f"Snippet: {r.get('snippet', '')}"
        for r in organic[:5]
    )
