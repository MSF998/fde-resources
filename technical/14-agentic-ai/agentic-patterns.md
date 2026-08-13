# [Topic Name]

**Date:** YYYY-MM-DD | **Track:** Technical | **Session:** XX

## Going In

-

## Key Concepts

- Agents Spectrum: We need to decide where does our usecase fit
  - Rule based RPA
    - requires more human oversight
  - Generative AI assistants
    - achieves a specific predifined goal
    - understand natural language
  - Goal Driven AI agents
    - works towards a high level object
    - adapt based on context
  - fully autonomous agentic systems
    - independantly sets and executes goal
    - requires minimal human oversight

- Where does my usecase fit
  - Ask the below questions to find a fit
    - how predictable is the problem
      - if it highly structured RPA should be enough
      - if it is open ended we need higher agency
    - how much human oversight can I provide
      - low human oversight = higher agency
    - level of complexity
    - how much adaptation is needed

- Work Backwards Method
  - used to identify the primary functions of a usecase
  - dimensions
    - can tasks be completed in steps = workflow
    - open ended tasks, dynamic decision making = multi agentic
    - budget
    - latency & performance
      - can my usecase tolerate delay
      - need fast responses
    - Risk
      - for high stake decisions
        - HITL pattern for human judgement

- Design Process
  - Define requirements
  - review common agent design patterns
  - select a patter
  - improve

- Common Design Patterns
  - Single Agent System
    - Uses LLM
    - Access to tools
    - system prompt
      - persona
      - guardrails
      - reasoning process
    - dont add too many tools
    - keep agents tasks specific
  - Multi agent system
    - workflow pattern
      - for highly structured repeatable process
      - not so flexible
      - less adaptibility
      - a sequential agent calling subagents in a sequence where each agent's output serves as the next agent's input
    - parallel pattern
      - agents performing tasks parallely
      - outputs are synthesized for a final response
      - for concurrent task executions
      - increased token consumption
    - loop pattern
      - agents calling each other in a loop until a specific termination condition is met
    - Review and critique pattern
      - loop agent
      - generator agent creates
      - critic subagent reviews it and passes feedback to generator agent
      - has a dedicated verification step

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
