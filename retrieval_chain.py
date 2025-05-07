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

from langchain.prompts import PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser


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
    # Load vector store but do not use context in prompt for now
    _ = load_vector_store()
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template="""
The following is a friendly conversation between a human and an AI assistant.
The assistant is helpful, context-aware, and answers using memory of the previous messages.

{history}
Human: {input}
AI:"""
    )

    chain = (
            {
                "input": lambda x: x["question"],
                "history": lambda x: x["chat_history"]
            }
            | prompt
            | llm
            | StrOutputParser()
    )

    return RunnableWithMessageHistory(
        runnable=chain,
        get_session_history=lambda session_id: ChatMessageHistory(),
        input_messages_key="question",
        history_messages_key="chat_history"
    )
