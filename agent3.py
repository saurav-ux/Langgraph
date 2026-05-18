from typing import Dict, TypedDict
from langgraph.graph import StateGraph


class AgentState(TypedDict):  # State Schema
    age: str
    name: str
    skills: list[str]
    result: str


def first_node(state: AgentState) -> AgentState:
    """Name Field with greeting"""
    state["result"] = "Hello multi " + state["name"]
    return state


def second_node(state: AgentState) -> AgentState:
    """User's age"""
    state["result"] = state["result"] + " Your age is " + state["age"]
    return state


def third_node(state: AgentState) -> AgentState:
    """Lists the use Skills"""
    state["result"] = (
        state["result"] + " Your Skills are: " + " ,".join(state["skills"])
    )
    return state


graph = StateGraph(AgentState)
graph.add_node("first", first_node)
graph.add_node("second", second_node)
graph.add_node("third", third_node)
graph.set_entry_point("first")
graph.add_edge("first", "second")
graph.add_edge("second", "third")
graph.set_finish_point("third")

app = graph.compile()
result = app.invoke(
    {
        "name": "Saurav Anand",
        "age": "23",
        "skills": ["Cricket", "Video Game"],
        "result": "",
    }
)
print(result["result"])
