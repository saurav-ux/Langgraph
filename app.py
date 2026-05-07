from typing import Dict, TypedDict
from langgraph.graph import StateGraph


class AgentState(TypedDict):  # State Schema
    message: str


def greeting_node(state: AgentState) -> AgentState:
    """Simple node that adds a greeting to the state"""

    state["message"] = "Hey " + state["message"] + ", how are your day going?"
    return state


graph = StateGraph(AgentState)
graph.add_node("greeter", greeting_node)

graph.set_entry_point("greeter")
graph.set_finish_point("greeter")

app = graph.compile()

result = app.invoke({"message": "Saurav"})

print(result["message"])
