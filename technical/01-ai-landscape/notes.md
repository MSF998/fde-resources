# AI Landscape

**Date:** 20206-01-22 | **Track:** Technical | **Session:** 01

## Key Concepts

- Context Engineering: It is the systemic practice of curating, structuring and managing everything that is fed into an AI model like an LLM.
- Components of AI Apps
  - System Prompt
  - LLM
  - Memory
  - Tools

- Deep Learning
  - Deals with unstructured form of data such as images, videos, textutal data etc.
  - Can be categorized into 3 forms of Neural Networks
    - ANN: Artificial Neural Network
    - CNN: Convolutional Neural Network
    - RNN: Recurrent Neural Network

- RNN: Was supposed to handle sequenece. text data.
  - Problems with RNN:
    - it used to experience long term dependency. had limited memory.
      - only used to retain recent data instead of the whole data.
      - Retained only last few words of a sentence
      - To fix this LSTM was introduced
- LSTM: Long Short term memory
  - Do we really need all the words in the sentence which introduced
  - Selective Write
  - Selective Read
  - Selective Forget
  - LSTM was a complex architecture so they introduced GRU
- GRU: Gated Recurrent unit
  - Had a simple architecture
  - after GRU we had attention models
  - after attention model we got encoder decoder architecture
  - after encode decorder we got into transformers then bi directional transformer then we got GPT

### Deep Learning -> RNN -> LSTM -> GRU -> Attention Mechanisms -> Encoder Decoder Arch -> Transformer Arch -> BERT -> **GPT**

- Transformer
  - Components
    - Encoders stacked on top of each other
    - Decoders stacked on top of each other
  - Flow
    - Input -> Encoder -> Decoder -> Predicted output

## What I Built / Tried

-

## Insights & Opinions

- The paper attention is all you need mentioned that they used 6 layers of encoders an 6 layers of decoders

## Questions / Gaps

-

## Links to Projects

-
