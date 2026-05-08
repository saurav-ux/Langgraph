from typing import Dict, TypedDict
from langgraph.graph import StateGraph


class AgentState(TypedDict):  # State Schema
    name: str
    age: str
    final: str


def first_node(state: AgentState) -> AgentState:
    """First node that adds a name to the state"""

    state["final"] = "Hi there " + state["name"]
    return state


def second_node(state: AgentState) -> AgentState:
    """Second node that adds an age to the state"""

    state["final"] = state["final"] + "! Your age is " + state["age"]

    return state


graph = StateGraph(AgentState)
graph.add_node("first", first_node)
graph.add_node("second", second_node)
graph.set_entry_point("first")
graph.add_edge("first", "second")
graph.set_finish_point("second")

app = graph.compile()
result = app.invoke({"name": "Saurav", "age": "25", "final": ""})
print(result["final"])
