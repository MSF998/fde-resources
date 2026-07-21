- Identity
  - Request ID must come from frontend
  - Order ID should be generated in the backend
  - Idempotency
  - an operation can be executed multiple times without changing the result beyond the initial execution
  - No duplicate business effect
  - LLMs should not be allowed to generate business identifiers

- Validation
  - use pydantic
  - In some scenarios dont allow pydantic to select values
  - Check the rules and policies explicitly

- Orchestration
  - Extract all the info in one place and allow the LLM to refer from what was extracteds

- Reliability
  - When we face a partial failure
    - retry
    - move to a dead queue
    - another worker picks up
    - perform long polling technique
    - Roll back if nothing works
    - log everything
