# retrieval_chain.py

# loads environment variables
from dotenv import load_dotenv
load_dotenv()

# importing langchain components
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

from config.settings import (
    KNOWLEDGE_PATH,
    INDEX_PATH,
    EMBED_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

def build_retrieval_chain():
    print("Loading knowledge base from:", KNOWLEDGE_PATH)
    loader = TextLoader(KNOWLEDGE_PATH)
    documents = loader.load()

    print(f"Splitting text into chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)

    print("Embedding using model:", EMBED_MODEL)
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    # Create or load FAISS index
    if os.path.exists(INDEX_PATH):
        print("Loading existing FAISS index from:", INDEX_PATH)
        vector_store = FAISS.load_local(
            INDEX_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
    else:
        print("Creating new FAISS index...")
        vector_store = FAISS.from_documents(chunks, embeddings)
        vector_store.save_local(INDEX_PATH)
        print("Saved FAISS index to:", INDEX_PATH)

    # Set up retriever with more results to increase matching probability
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    # Load the LLM (OpenAI GPT-3.5)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    print("Step 5: RetrievalQA chain initialized.")
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )
