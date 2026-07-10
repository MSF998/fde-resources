# Prompt Engineering

**Date:** 2026-04-25 | **Track:** Technical | **Session:** XX

## Key Concepts

- 7 style prompt engineering technique
  - Role: The persona
  - Task: The goal. What the LLM wants to achieve. Better to have task as one liner. Taks will be used by the LLM to strategize its actions. it is the high level goal
  - Context: Provide background information for LLM to reason so that the LLM does not assume
  - Reasoning: How we want the LLM to approach the problem. It is the step by step execution which the LLM needs to follow.
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

### Markdown Prompting Technique

- Why
  - LLMs are pattern-matching engines; they process raw text. If you feed them a wall of text, their attention mechanism diffuses. If you use basic Markdown syntax (#, -, ), you force a hierarchical semantic structure onto the prompt.

- Components
  - `# SYSTEM ROLE`: Defines the operational boundaries and persona. This establishes the baseline weights for how the model should behave and reason
  - `## CONTEXT`: The background data. This is where you inject the necessary external state or data payload required to execute the task
  - `## TASK`: The single, clear objective. What exactly is the model supposed to execute?
  - `## CONSTRAINTS`: The hard rules. Using bullet points here limits the search space and dictates what the model must not do
  - `## EXAMPLES` (Few-Shot): The expected input/output contract. This proves to the model what a successful execution looks like
  - `## OUTPUT FORMAT`: The strict definition of the return payload, locking down the structure so your application can parse it reliably.

- Example:

```
# ROLE
You are an uncompromising Senior Technical Recruiter parsing backend engineering profiles.

## CONTEXT
The hiring team needs a rapid assessment of an applicant's resume against our current tech stack requirements. We do not care about frontend skills.
* Target Stack: Python, FastAPI, Postgres.
* Applicant Resume: [Insert Raw Text Here]

## TASK
Evaluate the applicant's resume against the Target Stack and determine an initial screening decision.

## CONSTRAINTS
* Do not hallucinate skills not explicitly stated in the resume.
* Ignore any experience older than 5 years.
* If Python experience is less than 2 years, immediately reject.

## OUTPUT FORMAT
Provide the response using the following structure:
**Decision:** [Proceed / Reject]
**Reasoning:** [One sentence explanation]
**Missing Core Skills:** [Bullet list of missing Target Stack items]
```

### Keyword Prompting

- Keyword Prompting is a blunt instrument. It is the practice of stripping away grammar, syntax, and structural logic entirely, and instead bombarding the AI with a dense, comma-separated list of high-value trigger words
- Usage:
  - Image & Video Generation (Diffusion models)
  - Traditional Information Retrieval (Search Engines)
- Example:
  - Natural Language Prompt: "Please draw me a picture of a futuristic city at night while it is raining, and make it look like a high-quality 3D render."
  - Keyword Prompt: "cyberpunk city, neon, heavy rain, night, 8k resolution, unreal engine 5, photorealistic, volumetric lighting."

## Insights & Opinions

- Why do we need Task and Reasoning
- Writing a particular statement in a prompt 2 times increased the attention mechanism of the LLM to follow the instructions properly

### GPT-5 System Prompt Insights

- a piece of formatting based on the iCalendar (RFC 5545) specification. Specifically, it is an RRULE (Recurrence Rule) used by calendar applications to define how often an event repeats

```For example, "every morning" would be:
  schedule="BEGIN:VEVENT
  RRULE:FREQ=DAILY;BYHOUR=9;BYMINUTE=0;BYSECOND=0
  END:VEVENT"
```

- Tools Instructions
  - If you are generating files:
    - You MUST use the instructed library for each supported file format. (Do not assume any other libraries are available):
      - pdf --> reportlab
      - docx --> python-docx
      - xlsx --> openpyxl
      - pptx --> python-pptx
      - csv --> pandas
      - rtf --> pypandoc
      - txt --> pypandocdoc
      - md --> pypan
      - ods --> odfpy
      - odt --> odfpy
      - odp --> odfpy

  - Use the `web` tool to access up-to-date information from the web or when responding to the user requires information about their location. Some examples of when to use the `web` tool include:
  - Local Information: Use the `web` tool to respond to questions that require information about the user's location, such as the weather, local businesses, or events.
  - Freshness: If up-to-date information on a topic could potentially change or enhance the answer, call the `web` tool any time you would otherwise refuse to answer a question because your knowledge might be out of date.
  - Niche Information: If the answer would benefit from detailed information not widely known or understood (which might be found on the internet), such as details about a small neighborhood, a less well-known company, or arcane regulations, use web sources directly rather than relying on the distilled knowledge from pretraining.
  - Accuracy: If the cost of a small mistake or outdated information is high (e.g., using an outdated version of a software library or not knowing the date of the next game for a sports team), then use the `web` tool.

## Questions / Gaps

-

## Links to Projects

-
