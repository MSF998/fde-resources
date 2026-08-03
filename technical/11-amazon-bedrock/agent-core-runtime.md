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

## What I Built / Tried

-

## Insights & Opinions

-

## Questions / Gaps

-

## Links to Projects

-

## Coming Out

- s
