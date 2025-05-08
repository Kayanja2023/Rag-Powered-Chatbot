# Load environment variables from a .env file
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

# In-memory session storage for chat histories
session_histories = {}


# Load and index knowledge base
def load_vector_store():
    loader = TextLoader(KNOWLEDGE_PATH, encoding="utf-8")
    documents = loader.load()

    # Split large information into smaller chunks for embedding
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    # Load existing FAISS index if available, otherwise create one
    if os.path.exists(INDEX_PATH):
        return FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        store = FAISS.from_documents(chunks, embeddings)
        store.save_local(INDEX_PATH)
        return store


# Build the retrieval + LLM chain
def build_retrieval_chain():
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    # Initialize OpenAI Chat model
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)


    # System-level prompt with tone, structure, and fallback behavior
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("system",
         "You are Clickatell’s virtual assistant.\n\n"
         "Your job is to help users by retrieving **only known and verified information** "
         "from company documentation. Never guess or speculate.\n\n"
         "### Brand Voice:\n"
         "- Optimistic and confident\n"
         "- Clear and concise\n"
         "- Friendly but professional\n\n"
         "### Formatting Guidelines:\n"
         "- Use numbered steps or bullet points for clarity\n"
         "- Answer with plain language — avoid jargon\n"
         "- If unsure or information is unavailable, respond exactly with:\n"
         "  *I'm not confident I can assist with that. Let me connect you to a live agent.*\n\n"
         "### IMPORTANT:\n"
         "- Never fabricate information\n"
         "- Always remain helpful and courteous"),
        ("human", "{input}")
    ])

    # Build the LangChain chain
    chain = (
            {
                "input": lambda x: x["input"],
                "chat_history": lambda x: x["chat_history"]
            }
            | prompt
            | llm
            | StrOutputParser()                                                                                          # Ensure string response is returned
    )


    # Wrap the chain with message history (memory) support
    return RunnableWithMessageHistory(
        runnable=chain,
        get_session_history=lambda session_id: session_histories.setdefault(session_id, ChatMessageHistory()),
        input_messages_key="input",
        history_messages_key="chat_history"
    )
