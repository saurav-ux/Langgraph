from typing import Dict, TypedDict
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):  # State Schema
    number1: int
    number2: int
    operation: str
    finalNumber: int


def adder(state: AgentState) -> AgentState:
    """First node that adds two numbers"""
    state["finalNumber"] = state["number1"] + state["number2"]
    return state


def substractor(state: AgentState) -> AgentState:
    """Second node that substracts two numbers"""
    state["finalNumber"] = state["number1"] - state["number2"]
    return state


def decide_next_node(state: AgentState):
    """This node is decide"""
    if state["operation"] == "+":
        return "addition_operation"
    elif state["operation"] == "-":
        return "substraction_operation"


graph = StateGraph(AgentState)

graph.add_node("add_node", adder)
graph.add_node("substract_node", substractor)
graph.add_node(
    "router", lambda state: state
)  # This node will route to the next node based on the operation

graph.add_edge(START, "router")

graph.add_conditional_edges(
    "router",
    decide_next_node,
    {"addition_operation": "add_node", "substraction_operation": "substract_node"},
)
graph.add_edge("add_node", END)
graph.add_edge("substract_node", END)

app = graph.compile()

initial_state_1 = AgentState(number1=10, operation="+", number2=5, finalNumber=0)

print(app.invoke(initial_state_1))
