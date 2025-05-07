# retrieval_chain.py

# loads environment variables
from dotenv import load_dotenv
load_dotenv()

# importing langchain components
from langchain.prompts import PromptTemplate
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
    CHUNK_OVERLAP, CHAT_PROMPT_PATH
)

def build_retrieval_chain():

    # Step 1: Load the knowledge base text
    print("Loading knowledge base from:", KNOWLEDGE_PATH)
    loader = TextLoader(KNOWLEDGE_PATH, encoding="utf-8")
    documents = loader.load()

    # Step 2: Split the document into overlapping chunks
    print(f"Splitting text into chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)

    # Step 3: Create embeddings for each chunk using HuggingFace model
    print("Embedding using model:", EMBED_MODEL)
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    # Step 4: Initialize FAISS vector store — load from cache if it already exists, else build new index
    if os.path.exists(INDEX_PATH):
        print("Loading existing FAISS index from:", INDEX_PATH)
        vector_store = FAISS.load_local(
            INDEX_PATH,
            embeddings,
            allow_dangerous_deserialization=True                                    # Allows loading of saved FAISS index that includes serialized Python objects ( mainly: embedding models);


        )
    else:
        print("Creating new FAISS index...")
        vector_store = FAISS.from_documents(chunks, embeddings)
        vector_store.save_local(INDEX_PATH)
        print("Saved FAISS index to:", INDEX_PATH)

    # Step 5: Convert the FAISS store into a retriever (searches top-k similar chunks)
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    # Step 6: Load OpenAI’s GPT-3.5 as the language model
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # Load the chat prompt template
    with open(CHAT_PROMPT_PATH, "r", encoding="utf-8") as f:
        chat_prompt_template = f.read()

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=chat_prompt_template
    )



    # Step 7: Combine retriever + LLM into a RetrievalQA chain
    print("RetrievalQA chain initialized.")
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )
