from typing import Dict, TypedDict
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):  # State Schema
    number1: int
    number2: int
    operation: str
    finalNumber: int
    number3: int
    number4: int
    operation2: str
    finalNumber2: int


def adder(state: AgentState) -> AgentState:
    """First node that adds two numbers"""
    state["finalNumber"] = state["number1"] + state["number2"]
    state["finalNumber2"] = state["number3"] + state["number4"]
    return state


def substractor(state: AgentState) -> AgentState:
    """Second node that substracts two numbers"""
    state["finalNumber"] = state["number1"] - state["number2"]
    state["finalNumber2"] = state["number3"] - state["number4"]
    return state


def decide_next_node(state: AgentState):
    """This node is decide"""
    if state["operation"] == "+" or state["operation2"] == "+":
        return "addition_operation"
    elif state["operation"] == "-" or state["operation2"] == "-":
        return "substraction_operation"


graph = StateGraph(AgentState)

graph.add_node("add_node", adder)
graph.add_node("substract_node", substractor)
graph.add_node("router", lambda state: state)

graph.add_edge(START, "router")

graph.add_conditional_edges(
    "router",
    decide_next_node,
    {"addition_operation": "add_node", "substraction_operation": "substract_node"},
)

graph.add_node("add_node2", adder)
graph.add_node("substract_node2", substractor)
graph.add_node("router2", lambda state: state)

graph.add_edge("add_node", "router2")
graph.add_edge("substract_node", "router2")


graph.add_conditional_edges(
    "router2",
    decide_next_node,
    {"addition_operation": "add_node2", "substraction_operation": "substract_node2"},
)

graph.add_edge("add_node2", END)
graph.add_edge("substract_node2", END)

app = graph.compile()

initial_state_1 = AgentState(
    number1=10,
    operation="-",
    number2=5,
    finalNumber=0,
    number3=40,
    number4=30,
    operation2="+",
    finalNumber2=0,
)

print(app.invoke(initial_state_1))
