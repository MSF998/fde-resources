# [Topic Name]

**Date:** 2026-04-25 | **Track:** Technical | **Session:** XX

## Key Concepts

- 7 style prompt engineering technique
  - Role: The persona
  - Task: The goal. What the LLM wants to achieve. Better to have task as one liner
  - Context: Provide background information for LLM to reason so that the LLM does not assume
  - Reasoning: How we want the LLM to approach the problem
  - Rules: what we want the LLM to do and what we want the LLM to not do.
  - Stop Conditions: control the output from the LLM. control how much the LLM should generate
  - Output Style: How we want the output to look like

## What I Built / Tried

### 7 style prompt engineering technique

- Role: You are an Indian Travel Agent. You have experience in planning trips for people travelling
  to north India

- Task: Plan a 3 day trip from Kanpur to Srinagar(Kashmir)

- Context:
  1. I am a pure veg person,
  2. I am travelling by my bike,
  3. I drive at a speed of 80Kmph,
  4. I am travelling alone,
  5. I will leave on 26th April 2026,
  6. I don't ride bike during nights as I have issues.

- Reasoning: First Plan the road trip from Kanpur to Srinagar and then plan the city exploration in
  and around srinagar.

- Rules:
  1. Make sure the entire trip is concluded in 3 days, including the road travel and city exploration. Keep 2 addtional days for trip back to kanpur.
  2. Suggest proper rest stops with refill options.

- Stop Conditions: just generate the plan in two table with no additional supporting text. stop once
  the plan as a table is ready

- Output Style: Two table, one with road trip and other one with city exploration.

## Insights & Opinions

-

## Questions / Gaps

-

## Links to Projects

-
