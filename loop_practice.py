import random
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# The state - our notebook
class GameState(TypedDict):
    target: int
    guess: int
    attempts: int

# NODE: makes a random guess and counts the attempt
def guess_node(state: GameState):
    new_guess = random.randint(1, 5)
    new_attempts = state["attempts"] + 1
    print(f"Attempt {new_attempts}: guessing {new_guess} (target is {state['target']})")
    return {"guess": new_guess, "attempts": new_attempts}

# DECISION: check if the guess is correct - decides where to go next
def should_continue(state: GameState):
    if state["guess"] == state["target"]:
        return "correct"
    else:
        return "try_again"
    
# Build the graph
builder = StateGraph(GameState)

# Add the guessing node
builder.add_node("guess_node", guess_node)

# Start -> guess_node
builder.add_edge(START, "guess_node")

# THE CONDITIONAL EDGE - the loop!
builder.add_conditional_edges(
    "guess_node",
    should_continue,
    {
        "correct": END,
        "try_again": "guess_node"
    }
)

graph = builder.compile()

# Run the graph - start with a target, guess=0, attempts=0
result = graph.invoke({"target": 3, "guess": 0, "attempts": 0})

print("---")
print(f"Got it! The number was {result['target']}, found in {result['attempts']} attempts.")