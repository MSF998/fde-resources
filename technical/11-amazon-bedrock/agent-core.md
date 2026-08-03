# Agent Core

**Date:** YYYY-MM-DD | **Track:** Technical | **Session:** XX

## Going In

-

## Key Concepts

- Agent Core is a an agentic platform with the following components
  - Runtime
  - Gateway
  - Memory
  - Identity
  - Policy
  - Observability
  - Evaluations
  - Code Interpreter
  - Browser

- Agent Core Runtime
  - Framework & Model Independant Deployment
    - supports Langgraph, langchain, CrewAI
    - any models
  - use case independant
    - can handle large payload sizes (upto 100 MB)
    - can work with multi modal models
  - Secure
    - true session isolation
    - built in Auth
  - Deployment Steps
    - build the agent or tool code
    - configure it for agent core runtime
    - we get a docker file
    - ECR is created
    - Agent core runtime deploys it

- Agent Core Gateway
  - service that securely connects AI agents to external tools and services
  - simplify tool dev and integration
  - Arch of Gateway
    - enables to discover and use tools using a single gateway
    - uses the MCP arch
    - access to many tools using simple semantic search

- Agent Core Memory
  - helps build context aware agents
  - eliminates complex memory infra management
  - provides security
  - keeps data isolated and accessible via VPC

- Agent Core Identity
  - Inbound/Outbound manager
  - Provides access to AWS services as well as 3rd party tools
  - reduces the need for constant authorisation
  - token vault
  - Components
    - Identity Directory
      - acts a single source of truth for agents across org
    - Authoriser
    - Resource Creds provider
      - secure broker
    - resource token vault
      - holds OAuths
      - handles automatic refresh
    - Observability
      - tracks agent identity

- Agent core browser
  - agent access to browser for human like interaction
  - auto scales
  - concurrent sessions

- Agent core code interpreter
  - code execution environment
  - access S3

- Agent Core Observability
  - logging the actions takes by the agent
  - integrates with langsmit
  - offers detail visualisation
  - audit
  - supports open telemetry

- Policy in Agent Core
  - rule book
  - intercepts every action and validates if the action is allowed
  - policy enforcement
  - custom evaluation

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
