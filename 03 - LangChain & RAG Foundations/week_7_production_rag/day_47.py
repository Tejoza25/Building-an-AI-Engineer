import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI

# Load .env credentials from current or parent directories
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

CHROMA_DIR = "data/chroma_day47"

# Enterprise documents
DOCUMENTS = [
    Document(
        page_content="Database maintenance windows run every Sunday from 02:00 to 04:00 UTC.",
        metadata={"source": "database_runbook.md", "tier": "Infrastructure"},
    ),
    Document(
        page_content="Emergency incident escalations must ping the @oncall handle in the #incident-prod Slack channel.",
        metadata={"source": "oncall_procedures.md", "tier": "Operations"},
    ),
]


def setup_retriever():
    """Initializes local embeddings and seeds Chroma persistent store."""
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    vector_db = Chroma.from_documents(
        documents=DOCUMENTS,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )
    return vector_db.as_retriever(search_kwargs={"k": 2})


def format_docs(docs):
    """Formats retrieved context blocks."""
    return "\n\n".join([f"[{doc.metadata.get('source')}]: {doc.page_content}" for doc in docs])


def get_llms():
    """Builds primary (intentionally failing endpoint to test resilience) and fallback LLMs."""
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()

    # Primary LLM: Configured with an invalid model slug to simulate an upstream 404/500 outage
    failing_primary_llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_key if openrouter_key else "dummy-key",
        model="nonexistent-model-failover-test",
        max_retries=1,
    )

    # Secondary LLM: Resolves to standard verified provider
    if openai_key and openai_key.startswith("sk-") and not openai_key.startswith("sk-or-"):
        fallback_llm = ChatOpenAI(
            api_key=openai_key,
            model="gpt-4o-mini",
            temperature=0,
        )
    elif openrouter_key:
        fallback_llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_key,
            model="openrouter/free",
            temperature=0,
        )
    else:
        raise ValueError("No valid API credentials found in .env")

    return failing_primary_llm, fallback_llm


def run_resilient_rag():
    retriever = setup_retriever()
    primary_llm, fallback_llm = get_llms()

    prompt = ChatPromptTemplate.from_template(
        "You are an operations copilot. Answer strictly using the context.\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    )

    # Primary chain that will hit an artificial endpoint failure
    primary_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | primary_llm
        | StrOutputParser()
    )

    # Secondary fallback chain that kicks in seamlessly upon failure
    fallback_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | fallback_llm
        | StrOutputParser()
    )

    # Combine using LCEL .with_fallbacks()
    resilient_chain = primary_chain.with_fallbacks([fallback_chain])

    query = "What is the procedure for database maintenance and incident escalation?"

    print("==================================================")
    print("🛡️ DAY 47: RESILIENT ERROR HANDLING & FALLBACKS")
    print("==================================================")
    print(f"Query: {query}\n")
    print("Executing pipeline (Primary will fail -> Fallback will recover)...")

    response = resilient_chain.invoke(query)

    print("\n--- Final Resilient Response ---")
    print(response.strip())
    print("\n[Pipeline Status]: Recovered via fallback model without downtime.")


if __name__ == "__main__":
    run_resilient_rag()