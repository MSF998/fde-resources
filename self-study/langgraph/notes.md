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

### [Unit / Video / Chapter Name] — YYYY-MM-DD

- Key takeaways:
-
- Questions / Gaps:
-

## Insights & Opinions

-

## Links to Projects

-
