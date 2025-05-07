from dotenv import load_dotenv
load_dotenv()

import os
from config.settings import (
    KNOWLEDGE_PATH,
    INDEX_PATH,
    EMBED_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser

# In-memory session storage
session_histories = {}

def load_vector_store():
    loader = TextLoader(KNOWLEDGE_PATH, encoding="utf-8")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    if os.path.exists(INDEX_PATH):
        return FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        store = FAISS.from_documents(chunks, embeddings)
        store.save_local(INDEX_PATH)
        return store

def build_retrieval_chain():
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("system",
         "You are Clickatell’s virtual assistant.\n\n"
         "**Tone and Style:**\n"
         "- Clear, concise, and optimistic\n"
         "- Professional yet friendly\n"
         "- Helpful, factual, and accurate\n\n"
         "**Instructions:**\n"
         "- Use bullet points or steps when helpful.\n"
         "- Do not guess. Only answer based on retrieved documents or previous context.\n"
         "- If unsure, say: *I'm not confident I can assist with that. Let me connect you to a live agent.*"),
        ("human", "{input}")
    ])

    chain = (
            {
                "input": lambda x: x["input"],
                "chat_history": lambda x: x["chat_history"]
            }
            | prompt
            | llm
            | StrOutputParser()
    )

    return RunnableWithMessageHistory(
        runnable=chain,
        get_session_history=lambda session_id: session_histories.setdefault(session_id, ChatMessageHistory()),
        input_messages_key="input",
        history_messages_key="chat_history"
    )
