# LangGraph

**Source:** [Course / Playlist / Book — link] | **Started:** YYYY-MM-DD

## Overview

- LangGraph is a framework to build stateful, production grade AI agents

## Log

- openrouter setup

```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",  # any OpenRouter model id, e.g. "anthropic/claude-sonnet-4.5"
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        # Optional attribution headers OpenRouter uses for its public rankings.
        "HTTP-Referer": os.environ.get("OPENROUTER_SITE_URL", ""),
        "X-Title": os.environ.get("OPENROUTER_SITE_NAME", ""),
    },
)

response = llm.invoke("In one sentence, what is LangChain?")
print(response.content)
```

- basic langgraph setup

```python
from langgraph.graph import StateGraph, MessagesState, START, END

def call_llm(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

graph = StateGraph(MessagesState)

graph.add_node("call_llm", call_llm)

graph.add_edge(START, "call_llm")
graph.add_edge("call_llm", END)

graph = graph.compile()

if __name__ == "__main__":
    result = graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})
    print(result["messages"][-1].content)

```

- StageGraph
  - a graph where nodes represent functions and edges define the execution flow between nodes
  - StateGraph helps maintain a shared state

- node
  - a node is a function that takes a current state and returns a dict of updates to merge into it.
  - add_node registers a function under a name so that edges can refer to

- State
  - State is the current data at any point in the workflow
  - it can be defined using Pydantic's BaseModel or TypedDict

```python
from pydantic import BaseModel
class MathState(BaseModel):
    num1: float
    num2: float
    sum_result: float = 0
    final_result: float = 0
```

- complete example of a graph workflow

```python
import asyncio
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END

# Define the state using BaseModel
class MathState(BaseModel):
    num1: float
    num2: float
    sum_result: float = 0
    product_result: float = 0
    final_result: float = 0

# Define node functions
async def add_numbers(state: MathState) -> MathState:
    state.sum_result = state.num1 + state.num2
    return state

async def multiply_result(state: MathState) -> MathState:
    state.final_result = state.product_result * 2
    return state

async def divide(state: MathState) -> MathState:
    state.product_result = state.sum_result / state.num2
    return state

# Initialize and build the graph
graph = StateGraph(MathState)

graph.add_node("add", add_numbers)
graph.add_node("multiply", multiply_result)
graph.add_node("divide", divide)

graph.add_edge(START, "add")
graph.add_edge("add","divide")
graph.add_edge("divide", "multiply")
graph.add_edge("multiply", END)

# Compile and execute
app = graph.compile()

async def main():
    initial_state = MathState(num1=5, num2=3)
    final_state = await app.ainvoke(initial_state)
    print(f"Final Result: {final_state['final_result']}")

if __name__ == "__main__":
    asyncio.run(main())
```

- ReAct

- act
  - a normal node, runs one per loop

```python
# --- "act" node: this is the node whose outgoing edge we'll make conditional ---
async def act(state: MathState) -> MathState:
    """
    A node doesn't have to just compute a final answer - it can also take an
    action that changes the state for the *next* loop iteration. Here we bump
    num1 a bit, simulating "try again with an adjusted input".
    """
    state.attempts += 1
    print(f"[act] attempt {state.attempts}: final_result={state.final_result:.3f} "
          f"(threshold={state.threshold})")
    state.num1 += 5
    return state
```

- route_after_act
  - a router, runs after act, read the state a returns a condition

```python
# --- route_after_act: a ROUTER function, not a node ---
def route_after_act(state: MathState) -> str:
    """
    LangGraph calls this immediately after the "act" node runs. Unlike a node,
    a router function:
      - takes the state (read-only in spirit - don't mutate it here)
      - returns a plain string "label"
      - does NOT return the state itself

    That label is then looked up in the mapping passed to add_conditional_edges
    to decide which node runs next. This is what lets a graph branch or loop
    based on runtime data instead of being a fixed pipeline.
    """
    keep_going = state.final_result < state.threshold and state.attempts < state.max_attempts

    if keep_going:
        print(f"  -> route_after_act: below threshold, retrying (attempt {state.attempts} "
              f"< {state.max_attempts})")
        return "retry"

    reason = "reached threshold" if state.final_result >= state.threshold else "hit max_attempts"
    print(f"  -> route_after_act: stopping ({reason})")
    return "done"
```

- add_conditional_edges
  - wires both act and route_after_act. based on condition looks up which node to trigger

```python
# Conditional edge: "act" no longer points to a single fixed next node.
# Instead, route_after_act's return value ("retry" or "done") picks the branch.
graph.add_conditional_edges(
    "act",
    route_after_act,
    {
        "retry": "add",  # loop back to the start of the pipeline
        "done": END,     # stop
    },
)
```

- complete example

```python
import asyncio
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END

# Define the state using BaseModel
class MathState(BaseModel):
    num1: float
    num2: float
    sum_result: float = 0
    product_result: float = 0
    final_result: float = 0

    # --- new fields to support the act/route_after_act loop ---
    attempts: int = 0          # how many times we've gone around the loop
    max_attempts: int = 3      # safety valve so we can't loop forever
    threshold: float = 10.0    # target final_result we're trying to reach

# Define node functions
async def add_numbers(state: MathState) -> MathState:
    state.sum_result = state.num1 + state.num2
    return state

async def divide(state: MathState) -> MathState:
    state.product_result = state.sum_result / state.num2
    return state

async def multiply_result(state: MathState) -> MathState:
    state.final_result = state.product_result * 2
    return state

# --- "act" node: this is the node whose outgoing edge we'll make conditional ---
async def act(state: MathState) -> MathState:
    """
    A node doesn't have to just compute a final answer - it can also take an
    action that changes the state for the *next* loop iteration. Here we bump
    num1 a bit, simulating "try again with an adjusted input".
    """
    state.attempts += 1
    print(f"[act] attempt {state.attempts}: final_result={state.final_result:.3f} "
          f"(threshold={state.threshold})")
    state.num1 += 5
    return state

# --- route_after_act: a ROUTER function, not a node ---
def route_after_act(state: MathState) -> str:
    """
    LangGraph calls this immediately after the "act" node runs. Unlike a node,
    a router function:
      - takes the state (read-only in spirit - don't mutate it here)
      - returns a plain string "label"
      - does NOT return the state itself

    That label is then looked up in the mapping passed to add_conditional_edges
    to decide which node runs next. This is what lets a graph branch or loop
    based on runtime data instead of being a fixed pipeline.
    """
    keep_going = state.final_result < state.threshold and state.attempts < state.max_attempts

    if keep_going:
        print(f"  -> route_after_act: below threshold, retrying (attempt {state.attempts} "
              f"< {state.max_attempts})")
        return "retry"

    reason = "reached threshold" if state.final_result >= state.threshold else "hit max_attempts"
    print(f"  -> route_after_act: stopping ({reason})")
    return "done"

# Initialize and build the graph
graph = StateGraph(MathState)

graph.add_node("add", add_numbers)
graph.add_node("divide", divide)
graph.add_node("multiply", multiply_result)
graph.add_node("act", act)

graph.add_edge(START, "add")
graph.add_edge("add", "divide")
graph.add_edge("divide", "multiply")
graph.add_edge("multiply", "act")

# Conditional edge: "act" no longer points to a single fixed next node.
# Instead, route_after_act's return value ("retry" or "done") picks the branch.
graph.add_conditional_edges(
    "act",
    route_after_act,
    {
        "retry": "add",  # loop back to the start of the pipeline
        "done": END,     # stop
    },
)

# Compile and execute
app = graph.compile()

async def main():
    initial_state = MathState(num1=5, num2=3)
    final_state = await app.ainvoke(initial_state)
    print(f"\nFinal Result: {final_state['final_result']:.3f} "
          f"(after {final_state['attempts']} attempt(s))")

if __name__ == "__main__":
    asyncio.run(main())


```

### [Unit / Video / Chapter Name] — YYYY-MM-DD

- Key takeaways:
-
- Questions / Gaps:
-

## Insights & Opinions

-

## Links to Projects

-
