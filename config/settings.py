# config/settings.py

import os

# Path to the knowledge base text file
KNOWLEDGE_PATH = os.path.join("data", "knowledge_base_clickatell.txt")

# Directory to store/load FAISS vector index
INDEX_PATH = os.path.join("vector_store", "faiss_index")

# Embedding model to use from HuggingFace
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Prompt template paths
CHAT_PROMPT_PATH = "prompts/chat_prompt.txt"

SYSTEM_PROMPT_PATH = "prompts/system_prompt.txt"


# Chunking configuration for splitting documents
CHUNK_SIZE = 600                                                   #  Maximum number of characters per chunk
CHUNK_OVERLAP = 80                                                 #  Overlap between chunks to preserve context
