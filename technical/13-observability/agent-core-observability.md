# [Topic Name]
**Date:** YYYY-MM-DD | **Track:** Technical | **Session:** XX

## Going In
-

## Key Concepts
- Agentcore observability is built on top of cloud watch
- supports OTEL compatible
- concepts
    - sessions: complete user conversation or interaction context
    - trace: individual request-response cylces within sessions
    - spans: specific operation within a trace

- OTEL Example
```python
from opentelemetry import trace
tracer = trace.get_trace(__name__)
@tracer.start_as_current_span("process_query")
def handle_request(query):
    span = trace.get_current_span()
    span.set_attribute("query.length",len(query))

    # Agent logic
```

## What I Built / Tried
-

## Insights & Opinions
-

## Questions / Gaps
-

## Links to Projects
-

## Coming Out
-
