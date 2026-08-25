# Observability

**Date:** 2026-07-31 | **Track:** Technical | **Session:** 13

## Going In

-

## Key Concepts

- Open Telemetry
  - tokens consumed

- trace - api call of my app
- span - chain.invoke()
  - process within a trace

- langsmith
  - trace - one chain.invoke()

- Instrumentation
  - code wrapped around a function that records what came in and what came out.

The 5-layer monitoring model
When something's wrong, don't guess — walk layers in this order:

1. Dependency — check first, this is where symptoms show. Latency + error rate per external thing: LLM call, each tool, the chain itself. P50/P99 per component. In your code: LLM latency, check_inventory latency, create_order latency, send_confirmation latency — each separately.

2. Trajectory — the path the trace took. llm_calls_per_trace, tool_calls_per_trace, repeated-tool-call rate. Catches "nothing got individually slower, we're just doing more work per request." This is where you'd catch the repeated_inventory incident: dependency layer shows check_inventory latency is normal, but trajectory shows it got called 4× instead of 1×.

3. Decision — for each tool, was it right to call it at all. Needs eval (LLM-as-judge), not just counts — covered later.

4. Input — how much data enters each layer, in chars/tokens. campaign_agent_input_size, chain_input_size, llm_input_tokens. Catches context bloat. This is exactly your memory_explosion incident: \_bloated_history() in [order_chat.py](e:\FDE Resources\tech\sameer\langsmith\distributor-agent-core\order_chat.py) prepends 80 junk messages before the real conversation — dependency layer might look fine (LLM itself isn't "slow"), but input-layer tokens-per-trace would be huge.

5. Outcome — is each layer's output the right shape, not just "did it error." Your confirmation_failure incident (send_confirmation raises RuntimeError("SMTP unavailable")) shows up here differently than at dependency: the tool call fails cleanly (an error span), but premature_order is worse — create_order succeeds with no error at all, yet business-wise it's wrong (retailer said "not yet"). Root-level status stays green. Only outcome-layer inspection (or eval) catches it.

## What I Built / Tried

-

## Insights & Opinions

-

## Questions / Gaps

- Instrumentation, trace, span, run — telemetry vocab
- 5-layer monitoring model (dependency/trajectory/decision/input/outcome)
- LangSmith custom dashboard metrics (ratio charts)
- Offline evaluation
- Online evaluation
- LLM-as-judge + rubrics

## Links to Projects

-

## Coming Out

-
