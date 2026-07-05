from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# The STATE - the shared folder that travels through the graph
class AgentState(TypedDict):
    question: str
    answer: str

# NODE 1: takes the question, creates an answer
def answer_node(state: AgentState):
    question = state["question"]
    # simple made-up answer for now
    result = f"You asked: '{question}'. This is my answer!"
    return {"answer": result}

# Build the graph
builder = StateGraph(AgentState)

# Add the node to the graph
builder.add_node("answer_node", answer_node)

# Connect with edges: START -> answer_node -> END
builder.add_edge(START, "answer_node")
builder.add_edge("answer_node", END)

# Compile the graph into a runnable app
graph = builder.compile()

# Run the graph with a starting state
result = graph.invoke({"question": "What is LangGraph?"})

print(result)
print("---")
print("Just the answer:", result["answer"])