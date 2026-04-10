from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph.message import add_messages
from app.agents.tools import rag_search, web_search
from app.config import get_settings
from app.tracing.langfuse_client import get_langfuse
import uuid


TOOLS = [rag_search, web_search]

SYSTEM_PROMPT = """You are AgentFlow, a helpful ReAct-pattern assistant.

For every query:
1. THINK about what information you need
2. Use rag_search for questions about GCP, agents, LangGraph, Supabase, Langfuse, or Gemini
3. Use web_search for current events or facts outside your document store
4. Combine tool results to give a precise, structured answer

Always cite which tool provided each piece of information.
Return a structured response with: Answer, Sources, Confidence (high/medium/low).
"""


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    query: str
    session_id: str


def build_graph() -> StateGraph:
    s = get_settings()
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=s.google_api_key,
        temperature=0.1,
    ).bind_tools(TOOLS)

    tool_node = ToolNode(TOOLS)

    def should_continue(state: AgentState) -> str:
        last = state["messages"][-1]
        if hasattr(last, "tool_calls") and last.tool_calls:
            return "tools"
        return END

    def agent_node(state: AgentState) -> AgentState:
        lf = get_langfuse()
        span = lf.span(
            name="agent-step",
            input={"messages": len(state["messages"])},
            trace_id=state["session_id"],
        )
        messages = state["messages"]
        if not any(
            hasattr(m, "content") and SYSTEM_PROMPT[:20] in str(m.content)
            for m in messages
        ):
            from langchain_core.messages import SystemMessage
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        response = llm.invoke(messages)
        span.end(output={"response_type": type(response).__name__})
        return {"messages": [response]}

    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue)
    graph.add_edge("tools", "agent")

    return graph.compile()


_graph = None


def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


async def run_agent(query: str) -> dict:
    session_id = str(uuid.uuid4())
    lf = get_langfuse()
    trace = lf.trace(
        name="agentflow-run",
        input={"query": query},
        session_id=session_id,
    )
    graph = get_graph()
    state = await graph.ainvoke({
        "messages": [HumanMessage(content=query)],
        "query": query,
        "session_id": trace.id,
    })
    final = state["messages"][-1]
    answer = final.content if hasattr(final, "content") else str(final)
    trace.update(output={"answer": answer})
    lf.flush()
    return {
        "answer": answer,
        "session_id": session_id,
        "trace_id": trace.id,
        "steps": len(state["messages"]),
    }
