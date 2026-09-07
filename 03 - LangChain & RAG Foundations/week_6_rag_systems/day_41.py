import os
import shutil
from typing import List
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI

# Load API credentials from root .env
load_dotenv(dotenv_path="../.env")

CHROMA_DIR = "data/chroma_day41"

# ---------------------------------------------------------------------------
# 1. Knowledge Base Documents (Simulating Ingested Pipeline)
# ---------------------------------------------------------------------------
KNOWLEDGE_DOCS = [
    Document(
        page_content="Day 37 teaches document loading from PDF, Markdown, and TXT files into Document objects.",
        metadata={"source": "curriculum_day37.txt", "week": 6},
    ),
    Document(
        page_content="Day 38 covers RecursiveCharacterTextSplitter for optimal chunking and boundary overlap.",
        metadata={"source": "curriculum_day38.txt", "week": 6},
    ),
    Document(
        page_content="Day 39 uses sentence-transformers/all-MiniLM-L6-v2 to map text to 384-dimensional dense vectors.",
        metadata={"source": "curriculum_day39.txt", "week": 6},
    ),
    Document(
        page_content="Day 40 indexes vectors into Chroma and FAISS databases for fast disk-persistent similarity queries.",
        metadata={"source": "curriculum_day40.txt", "week": 6},
    ),
    Document(
        page_content="Day 41 connects a vector store retriever directly to an LLM using LCEL to build an end-to-end RAG chain.",
        metadata={"source": "curriculum_day41.txt", "week": 6},
    ),
]


def format_docs(docs: List[Document]) -> str:
    """Combines retrieved document contents into a structured context string."""
    return "\n\n".join(
        f"[Source: {doc.metadata.get('source')}]\n{doc.page_content}"
        for doc in docs
    )


def build_and_run_rag():
    print("=== Building Day 41 End-to-End RAG Pipeline ===\n")

    # Clean local store path for repeatable demonstration
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    # 1. Initialize local embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    # 2. Populate and persist Chroma Vector DB
    vector_db = Chroma.from_documents(
        documents=KNOWLEDGE_DOCS,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )

    # 3. Convert Vector DB to Retriever interface
    retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 2},
    )

    # 4. Prompt Template enforcing factual grounding
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "You are a strict, grounded AI Engineering assistant.\n"
            "Answer the question using ONLY the retrieved context below.\n"
            "If the answer cannot be determined from the context, state that you do not know.\n\n"
            "Retrieved Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Grounded Answer:"
        ),
    )

    # 5. LLM Configuration via OpenRouter dynamic router
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model="openrouter/free",
        temperature=0,
    )

    # 6. Modern LCEL RAG Chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Test Query 1: Information contained in the knowledge base
    query_1 = "Which day introduced 384-dimensional dense vectors and what model was used?"
    print(f"Query 1: '{query_1}'")
    answer_1 = rag_chain.invoke(query_1)
    print(f"Response:\n{answer_1}\n")

    # Test Query 2: Information NOT in the knowledge base (tests grounding)
    query_2 = "What programming language was invented in 1991?"
    print(f"Query 2: '{query_2}'")
    answer_2 = rag_chain.invoke(query_2)
    print(f"Response:\n{answer_2}\n")


if __name__ == "__main__":
    build_and_run_rag()