### To remeber

- Longer prompts are fine
- Build model specific prompts
  - Claude prefers XML
  - GPT prefers markdown
- Keep updaing prompts when models update
- LLMs degrade when overwhelmed with irrelevant tokens
  - Curate
- Hallucinations increase with noise
- Start small
- Keep your prompts where specific

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

### Gaps

- Learn more on Harness Engineering
  - the discipline of designing the environment, tools, and feedback loops that govern autonomous AI agents
    - System Prompt
    - Tool Definations
    - Memory
    - Routing Logic
    - Output Validation
    - Feedback Loop

| Hallucination | Confabulation           |
| ------------- | ----------------------- |
| Fabrication   | Plausible but incorrect |
