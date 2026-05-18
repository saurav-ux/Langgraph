from typing import Dict, TypedDict
from langgraph.graph import StateGraph


class AgentState(TypedDict):  # State Schema
    value: list[int]
    name: str
    result: str
    operator: str


def process_values(state: AgentState) -> AgentState:
    """This functions handles multiple inputs"""
    if state["operator"] == "+":

        state["result"] = f"Hi there {state['name']}! Your sum = {sum(state['value'])}"
    else:
        state["result"] = (
            f"Hi there {state['name']}! Your max value = {max(state['value'])}"
        )

    return state


graph = StateGraph(AgentState)
graph.add_node("processor", process_values)
graph.set_entry_point("processor")
graph.set_finish_point("processor")

app = graph.compile()
answers = app.invoke(
    {"value": [1, 2, 3, 4], "name": "Steve", "result": "", "operator": "*"}
)

print(answers["result"])
