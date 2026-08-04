# Agent Core Runtime

**Date:** YYYY-MM-DD | **Track:** Technical | **Session:** XX

## Going In

-

## Key Concepts

- Building an Agentic System
  - Amazon Cognito: For user authentication and group permission
  - WAF: To protect from DDOS and malicious traffic
  - Amazon Cloud front: CDN to route requests
  - AWS Lambda function: Route logic to call containerized agents
  - Amazon bedrock for agents
  - S3: storage
  - DynamoDB: for maintaing states

- Agentic Core Runtime
  - serverless runtime
  - build to build and deploye AI agents and tools regardless of framework, protocol or model choice
  - session isolation
  - complete memory isolation
  - dedicated ram for each session

- Agent core python SDK

```python
from bedrock_agentcore import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

@app.entrypoint
def my_agent(request):
	# agent logic
	return response

app.run()
```

- started toolkit
  - configure
    - setup ECR, Role, Auth
  - launch
    - deploy to agentcor runtime
  - invoke
    - invoke with payload

- agent created -> arn generated
- create endpoint -> DEFAULT
- API Contracts for Custom Docker Images
  - /ping
  - /invocations
  - port 8080

```python
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
from strands import Agent

app = FastAPI(title="Agent Server", version="1.0.0")
strands_agent = Agent()

@app.post("/invocations")
async dev invoke_agent(request: Request):
  user_message = request.input.get("prompt","")
  result = strands_agent(user_message)
  response = Response(
    content=result.message,
    status_code=200
  )
  return response

@app.get("/ping")
async def ping():
  return {"status":"healthy"}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8080)
```

- True session isolation
  - each session runs in microVM (compute+memory+filesystem)
  - uses firecracker tech
  - maintains state.
  - agentcore memory for short term and long term

- session lifecycle
  - 500 active session workloads
  - session suspended after 5 minutes of inactivity. cuts down CPU cycles
    - application state, file system and env vars are maintained
  - sessions timeout after 15 minutues of inactivity
  - max session duration is 8 hrs
  - pay only for active cpu usage

- MCP Servers within Agent Core Runtime
  - All mcp servers need to be avaialble at port 8000
  - security is implemented using OAuth from cognito
  - run on agent core runtime

## What I Built / Tried

-

## Insights & Opinions

-

## Questions / Gaps

-

## Links to Projects

-

## Coming Out
