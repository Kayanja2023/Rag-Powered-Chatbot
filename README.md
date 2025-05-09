# Clickatell RAG-Powered Q&A Chatbot

## Project Requirements

 The ask for the project [RaD-GP-C25-P-I6] is to build a chatbot that integrates company-specific knowledge into a Generative AI system using embedding-based retrieval and conversational memory. The goal is to demonstrate how internal knowledge assets can be structured, embedded, and queried to support accurate and brand-consistent answers. The chatbot should provide coherent, multi-turn dialogue capabilities while gracefully handling uncertainty with a seamless fallback mechanism.

### The deliverables include:

- An embedded knowledge base built from company FAQs, product info, and policies
- A chatbot with memory to support context-aware, multi-turn conversations
- Standardized prompt templates to ensure consistent tone and structure
- A fallback system to detect uncertainty and offer live agent handover
- A working prototype demonstrating RAG-based question answering
- A live demo covering architecture, features, and chatbot examples

## Clickatell RAG-Powered Q&A Chatbot


### Components

| Module              | Description                                          |
|---------------------|------------------------------------------------------|
| `chatbot.py`        | CLI-based main interface loop for user interaction   |
| `retrieval_chain.py`| Initializes vector store, memory, and LLM pipeline   |
| `config/settings.py`| Stores constants for chunking, model, paths, etc.    |
| `data/knowledge_base_clickatell.txt` | Source knowledge file                                |
| `vector_store/`     | FAISS index generated from the knowledge base        |
| `prompts/`          | Contains prompt templates for chat/system formatting |
| `evaluation/`       | Examples annotated responses                         |
| `docs/`             | Contains project documentation like research summary |

---
## Overview  
This repository contains a LangChain-based chatbot designed to answer company-specific questions using a local knowledge base. By combining embedding-based retrieval with conversational memory, the chatbot delivers accurate, context-aware responses that reflect internal documentation. It supports multi-turn interactions, prompt templating, and a fallback mechanism for seamless live agent escalation.

---
## Features

### 1. RAG Pipeline
- Uses `langchain`, `FAISS`, and `HuggingFaceEmbeddings`
- Breaks input knowledge into retrievable chunks

### 2. Conversational Buffer Memory
- Session-based in-memory history via `ChatMessageHistory`
- Ensures consistent and coherent multi-turn interactions

### 3. Prompt Engineering & Templating
- Company voice defined in `system_prompt.txt`
- Responses consistently structured with numbered steps/bullets
- Fallback behavior embedded into the LLM prompt itself

### 4. Seamless Live Agent Handover
- Triggers on model uncertainty via phrase detection
- Responds: *"I'm not confident I can assist with that. Let me connect you to a live agent."*

---

## How to Run

> Prerequisites:
- Python 3.10+
- `requirements.txt` installed (`pip install -r requirements.txt`)
- `.env` file with any API keys (e.g., OpenAI)

```bash
python chatbot.py
```

---

## Sample Prompts to Test Fallback

```text
What is Clickatell’s current share price?
Tell me something about our CEO's favorite movie.
Can you enable psychic mode?
```

These should all gracefully fall back to the live agent handover.

---

## Directory Overview

```bash
├── chatbot.py                  # Main user interaction loop
├── retrieval_chain.py          # LLM + retrieval + memory pipeline
├── config/
│   └── settings.py             # Constants for chunking, model, paths
├── data/
│   └── knowledge_base_clickatell.txt
├── docs/
│   └── research_summary.pdf
├── prompts/
│   ├── system_prompt.txt
│   └── chat_prompt.txt
├── evaluation/
│   └── responses_with_rag.md
├── vector_store/
│   └── faiss_index/            # FAISS index and metadata
├── requirements.txt
├── README.md
└── .env                        # API keys 
```

---

## Research Summary

See `docs/research_summary.pdf` for a full write-up on:
- Prompt Design adn Templating
- Buffer Memory
- Embedding and vector Database
- Workflow Summary


`#GenerativeAI` `#RAG` `#LangChain` `#VectorSearch` `#PromptEngineering` `#ClickatellR&D`