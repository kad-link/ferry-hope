from langchain_groq import ChatGroq
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from dotenv import load_dotenv
from utils.ai_tools import fetch_particular_order, fetch_all_orders_tool, place_an_order, mark_delivered, cancel_order
from dataclasses import dataclass

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

tools = [fetch_particular_order,
         fetch_all_orders_tool,
         place_an_order,
         mark_delivered,
         cancel_order
         ]

llm_with_tools = llm.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

@dataclass
class AgentContext:
    user_id: int


graph = StateGraph(AgentState, context_schema=AgentContext)

def call_llm(state: AgentState):

    response = llm_with_tools.invoke(state["messages"])

    return {
        "messages" : [response]
    }

tool_node = ToolNode(tools)

graph.add_edge(START, "llm")
graph.add_node("llm", call_llm)
graph.add_node("tools", tool_node)
graph.add_edge("tools", "llm")
graph.add_conditional_edges("llm", tools_condition)

agent = graph.compile()
