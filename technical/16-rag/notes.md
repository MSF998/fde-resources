# [Topic Name]

**Date:** YYYY-MM-DD | **Track:** Technical | **Session:** XX

## Going In

- attention mechanins: importance of cross dependancy of words
  - each word is attending to each other word

- context window
  - number of tokens an LLM can attend to

- context rot
  - llm does not attend to all the other tokens due to higher number of tokens

## Key Concepts

- RAG
  - ingestion
  - Retrivel
  - Generation

- self RAG
- corrective RAG
- hybrid RAG
  - decide
    - No RAG, keyword based search, semantic, regex (grep)
- graph RAG
  - knowledge graph
    - graph representaion of our data
    - neo4j

- Chunking
  - divide a large doc into small parts
  - why to chunk
    - loss of info if not chunked,
    - to maintain vector quality
  - should not be too small or too large
  - chunking strategies
    - page chunking
      - one page, one chunk
    - delimter chunking
      - choose a delimeter
    - recursive character chunking
    - prepostion chunking

- ## types of chunking strategies

- Embedding
  - Mathematical representation of a word.
  - embedding model
    - a model which takes in a word and gives out a vector representation and stores it in a vector DB
    - vectors hold the meaning of the entire text
- Retrieval
  - use the same embedding model used during ingestion
  - use cosine similarity
  - the input question also converts into vector representation using the same embedding models

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
