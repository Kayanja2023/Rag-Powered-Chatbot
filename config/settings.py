# config/settings.py

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

# Path to the knowledge base text file
KNOWLEDGE_PATH = os.path.join("data", "knowledge_base_clickatell.txt")

# Directory to store/load FAISS vector index
INDEX_PATH = os.path.join("vector_store", "faiss_index")

# Embedding model to use from HuggingFace
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Chunking configuration for splitting documents
CHUNK_SIZE = 600                                                   #  Maximum number of characters per chunk
CHUNK_OVERLAP = 80                                                 #  Overlap between chunks to preserve context
