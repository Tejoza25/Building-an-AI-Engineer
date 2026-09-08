import os
import shutil
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI

load_dotenv(dotenv_path="../.env")

CHROMA_DIR = "data/chroma_day43"

KNOWLEDGE_BASE = [
    Document(
        page_content="Chroma is an open-source, local vector database backed by SQLite and DuckDB.",
        metadata={"source": "vector_dbs.txt"},
    ),
    Document(
        page_content="To install Chroma in Python, execute: pip install chromadb langchain-chroma.",
        metadata={"source": "installation_guide.txt"},
    ),
    Document(
        page_content="FAISS is Meta's high-speed in-memory similarity search library for dense vectors.",
        metadata={"source": "faiss_docs.txt"},
    ),
]


def setup_retriever():
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    vector_db = Chroma.from_documents(
        documents=KNOWLEDGE_BASE,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )
    return vector_db.as_retriever(search_kwargs={"k": 2})


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_conversational_rag():
    retriever = setup_retriever()

    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model="openrouter/free",
        temperature=0,
    )

    # 1. Re-writing sub-chain: Reformulate follow-ups into standalone queries
    rephrase_system_prompt = (
        "Given a chat history and the latest user question which might reference context "
        "in the chat history, formulate a standalone question that can be understood "
        "without the chat history. Do NOT answer the question, just reformulate it "
        "if needed; otherwise return it as is."
    )
    rephrase_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", rephrase_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{question}"),
        ]
    )
    rephrase_chain = rephrase_prompt | llm | StrOutputParser()

    # 2. Synthesis sub-chain: Answer grounded strictly in retrieved context
    qa_system_prompt = (
        "You are a factual AI assistant. Answer the question using ONLY the retrieved context below.\n"
        "If you do not know the answer, state that you do not know.\n\n"
        "Context:\n{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{question}"),
        ]
    )

    def contextual_retriever(inputs):
        # If there is prior conversation, rewrite the query first
        if inputs.get("chat_history"):
            standalone_query = rephrase_chain.invoke(inputs)
            print(f"   [Internal Re-written Query]: \"{standalone_query}\"")
        else:
            standalone_query = inputs["question"]
        return retriever.invoke(standalone_query)

    # 3. End-to-end LCEL chain
    rag_chain = (
        RunnablePassthrough.assign(
            context=lambda x: format_docs(contextual_retriever(x))
        )
        | qa_prompt
        | llm
        | StrOutputParser()
    )

    chat_history = []

    print("==================================================")
    print("🤖 DAY 43: CONVERSATIONAL RAG MULTI-TURN TEST")
    print("==================================================\n")

    # Turn 1
    turn1_input = "What is Chroma?"
    print(f"[User Turn 1]: {turn1_input}")
    res1 = rag_chain.invoke({"question": turn1_input, "chat_history": chat_history})
    print(f"[Assistant Turn 1]:\n{res1.strip()}\n")

    chat_history.extend([
        HumanMessage(content=turn1_input),
        AIMessage(content=res1),
    ])

    # Turn 2 (Pronoun "it" resolution)
    turn2_input = "How do I install it in Python?"
    print(f"[User Turn 2 (Pronoun Ref)]: {turn2_input}")
    res2 = rag_chain.invoke({"question": turn2_input, "chat_history": chat_history})
    print(f"[Assistant Turn 2]:\n{res2.strip()}\n")


if __name__ == "__main__":
    build_conversational_rag()