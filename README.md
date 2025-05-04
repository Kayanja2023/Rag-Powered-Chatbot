
# RaD-GP-C25-P-I5: Enhancing Generative AI with Embeddings and Vector Databases

## Project Requirements

The ask for the project **[RaD-GP-C25-P-I5]** is to build a chatbot that integrates **vector databases** and **embedding-based retrieval** to enhance contextual responses using Retrieval-Augmented Generation (RAG). The objective is to demonstrate how external knowledge can be embedded, stored, and retrieved to enrich prompts and improve the relevance and accuracy of generated responses.

The deliverables include:
- A comprehensive research summary on embedding techniques and vector database systems
- A revised system architecture and README
- A working RAG-based chatbot prototype 
- A live demonstration showcasing improved contextual accuracy

---

## Overview

This repository hosts a LangChain-powered chatbot that enriches its prompts using embedded knowledge from a local corpus. By leveraging vector similarity search and document chunk retrieval, the chatbot provides contextually relevant responses using information outside the model's pretraining.

---

## Features

- Uses HuggingFace Embeddings (`all-MiniLM-L6-v2`) for lightweight sentence vectorization
- Supports local FaceBook AI Similarity Search (FAISS) 
- Implements Retrieval-Augmented Generation using LangChain's `RetrievalQA` chain
- Modular file structure for easy swapping of embedding models and databases


---


### Retrieval-Augmented Chatbot Pipeline

| Component | Description                                                                                     |
|----------|-------------------------------------------------------------------------------------------------|
| **User Query** | The user's natural language input to the chatbot.                                               |
| **Retrieval-Augmented Generation Chain** | The main pipeline that coordinates embedding, retrieval, and response generation.               |
| **Embeddings** | Converts the user's query into dense vector representations.                                    |
| **Knowledge Base** | Source content (`.txt`) chunked and embedded for context retrieval.                             |
| **Vector Database** | Stores and indexes all document embeddings; enables similarity-based search using FAISS         |
| **Retrieval** | Finds top-k relevant chunks from the vector DB using query embedding.                           |
| **Chatbot** | Final LLM (GPT-3.5) that takes the retrieved content + original query and generates a response. |
---
## Directory Structure

```
rad-gp-c25-p-i5/
├── chatbot.py                  # Runs the chatbot interface
├── retrieval_chain.py          # Constructs the retrieval chain
├── vector_store/
│   └── faiss_index/            # Contains saved FAISS index files (.faiss, .pkl)
├── data/
│   └── knowledge_base.txt      # Source content used for embeddings
├── evaluation/
│   └── responses_with_rag.md   # Logs of enriched chatbot responses
├── config/
│   └── settings.py             # Stores config like index paths and model names
├── docs/
│   └── research_summary.md     # Summary of embedding and vector DB research
│  
├── prompts/                    # Templates for LLM prompts
├── requirements.txt            # Dependency list
└── README.md                   # Overview



```
----




## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file at the root with:

```env
OPENAI_API_KEY=your-api-key-here
```

### 3. Run the Application

```bash
python chatbot.py
```

---



---

