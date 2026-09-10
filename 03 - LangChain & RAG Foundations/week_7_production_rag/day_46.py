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

CHROMA_DIR = "data/chroma_day46"

# Grounding dataset
DOCUMENTS = [
    Document(
        page_content="The deployment window for production releases is Tuesday to Thursday between 06:00 and 09:00 UTC.",
        metadata={"source": "deployment_guide.md", "topic": "Infrastructure"},
    ),
    Document(
        page_content="Rollbacks must be initiated immediately if p99 latency degrades by more than 15% over a 5-minute window.",
        metadata={"source": "sla_runbook.md", "topic": "Monitoring"},
    ),
    Document(
        page_content="Secret keys and database credentials must rotate every 90 days via HashiCorp Vault.",
        metadata={"source": "security_policy.md", "topic": "Compliance"},
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
    """Formats retrieved context blocks into structured boundaries."""
    formatted = []
    for i, doc in enumerate(docs, 1):
        formatted.append(f"--- Document Chunk {i} [{doc.metadata.get('source')}] ---\n{doc.page_content}")
    return "\n\n".join(formatted)


def get_llm():
    """Resolves credentials prioritizing OpenAI, falling back to OpenRouter free tier."""
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()

    if openai_key and openai_key.startswith("sk-") and not openai_key.startswith("sk-or-"):
        return ChatOpenAI(
            api_key=openai_key,
            model="gpt-4o-mini",
            temperature=0,
        )

    if openrouter_key:
        return ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_key,
            model="openrouter/free",
            temperature=0,
        )

    raise ValueError("No valid OPENAI_API_KEY or OPENROUTER_API_KEY found in .env")


def run_prompt_grounding_audit():
    retriever = setup_retriever()
    llm = get_llm()

    # Production Strict Prompt Guardrail
    grounded_system_prompt = (
        "You are an enterprise technical verification assistant.\n"
        "Your task is to answer the user's question STRICTLY and ONLY based on the provided context below.\n\n"
        "STRICT CONSTRAINTS:\n"
        "1. Do NOT assume, extrapolate, or use pre-trained background facts outside this context.\n"
        "2. If the exact answer is not explicitly stated in the context, you must respond EXACTLY with:\n"
        "   'Insufficient context to provide an answer.'\n"
        "3. Keep the response direct, objective, and free of conversational pleasantries."
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", grounded_system_prompt),
        ("human", "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"),
    ])

    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    # Test Case 1: In-domain query (Information present)
    query_in_domain = "What are the requirements for deployment windows and rollback triggers?"
    # Test Case 2: Out-of-domain query (Information absent; should trigger rejection guardrail)
    query_out_of_domain = "What is the reimbursement policy for home office equipment?"

    print("==================================================")
    print("🛡️ DAY 46: FACTUAL GROUNDING & PROMPT GUARDRAILS")
    print("==================================================")

    print(f"\n[Test 1 - In Domain]: {query_in_domain}")
    response_1 = rag_chain.invoke(query_in_domain)
    print(f"Result:\n{response_1.strip()}\n")

    print("--------------------------------------------------")
    print(f"[Test 2 - Out of Domain]: {query_out_of_domain}")
    response_2 = rag_chain.invoke(query_out_of_domain)
    print(f"Result:\n{response_2.strip()}\n")
    print("==================================================")


if __name__ == "__main__":
    run_prompt_grounding_audit()