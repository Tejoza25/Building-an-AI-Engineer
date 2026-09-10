import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI

# Load .env credentials from current or parent directories
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

CHROMA_DIR = "data/chroma_day49_audit"

# Production enterprise knowledge corpus
ENTERPRISE_CORPUS = [
    Document(
        page_content="Production release approvals require affirmative sign-offs from both the Engineering Lead and SecOps Lead.",
        metadata={"source": "engineering_playbook.md", "section": "Release Governance", "version": "2.4"},
    ),
    Document(
        page_content="On-call incident response mandates initial triage within 15 minutes for Tier 1 customer outages.",
        metadata={"source": "sla_matrix.md", "section": "Incident Management", "version": "1.8"},
    ),
    Document(
        page_content="Continuous Integration (CI) test suites must pass 100% of unit and integration checks prior to staging deployment.",
        metadata={"source": "ci_cd_guidelines.md", "section": "Testing Requirements", "version": "3.1"},
    ),
]


def setup_vector_store():
    """Initializes local embeddings and seeds Chroma persistent store."""
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    vector_db = Chroma.from_documents(
        documents=ENTERPRISE_CORPUS,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )
    return vector_db.as_retriever(search_kwargs={"k": 2})


def format_context_docs(docs):
    formatted = []
    for i, doc in enumerate(docs, 1):
        formatted.append(
            f"[Source {i} - {doc.metadata.get('source')} | Section: {doc.metadata.get('section')}]:\n{doc.page_content}"
        )
    return "\n\n".join(formatted)


def resolve_model_endpoints():
    """Configures resilient primary and fallback LLM endpoints."""
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()

    # 1. Primary Model
    if openai_key and openai_key.startswith("sk-") and not openai_key.startswith("sk-or-"):
        primary_llm = ChatOpenAI(api_key=openai_key, model="gpt-4o-mini", temperature=0, streaming=True)
    elif openrouter_key:
        primary_llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_key,
            model="openrouter/free",
            temperature=0,
            streaming=True,
        )
    else:
        raise ValueError("No valid OPENAI_API_KEY or OPENROUTER_API_KEY found in .env")

    # 2. Resilient Fallback Model
    backup_llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_key if openrouter_key else openai_key,
        model="openrouter/free",
        temperature=0,
        streaming=True,
    )

    return primary_llm.with_fallbacks([backup_llm])


def run_week7_production_audit():
    retriever = setup_vector_store()
    llm = resolve_model_endpoints()

    # Grounded Production Prompt
    system_prompt = (
        "You are an enterprise technical verification assistant.\n"
        "Answer the user query STRICTLY using the provided context chunks.\n"
        "Include source tags (e.g., [Source 1]) for all stated facts.\n"
        "If the context does not supply the answer, reply EXACTLY with:\n"
        "'Insufficient context to provide an answer.'\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Audited Answer:"
    )
    prompt = ChatPromptTemplate.from_template(system_prompt)

    # Explainable Dual-Branch LCEL Pipeline
    audit_chain = RunnableParallel(
        context_docs=retriever,
        question=RunnablePassthrough(),
    ) | RunnableParallel(
        answer=(
            RunnablePassthrough.assign(context=lambda x: format_context_docs(x["context_docs"]))
            | prompt
            | llm
            | StrOutputParser()
        ),
        sources=lambda x: [
            {
                "file": doc.metadata.get("source"),
                "section": doc.metadata.get("section"),
                "version": doc.metadata.get("version"),
                "content": doc.page_content,
            }
            for doc in x["context_docs"]
        ],
    )

    query = "What are the sign-off requirements for production releases and incident triage windows?"

    print("==================================================")
    print("🚀 DAY 49: WEEK 7 PRODUCTION RAG PIPELINE AUDIT")
    print("==================================================")
    print(f"Query: {query}\n")
    print("Executing End-to-End Audited Pipeline...")

    result = audit_chain.invoke(query)

    print("\n--- 🤖 Grounded Response ---")
    print(result["answer"].strip())

    print("\n--- 📑 Source Provenance Audit ---")
    for idx, s in enumerate(result["sources"], 1):
        print(f"[{idx}] {s['file']} (v{s['version']}) | Section: {s['section']}")
        print(f"    Passage: \"{s['content']}\"")

    print("\n==================================================")
    print("✅ WEEK 7 INTEGRATION AUDIT: COMPLETE")
    print("==================================================")


if __name__ == "__main__":
    run_week7_production_audit()