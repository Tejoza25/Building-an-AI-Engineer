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

# Explicitly load the local .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

CHROMA_DIR = "data/chroma_day44"

# Ingested knowledge corpus with provenance metadata
CORPUS = [
    Document(
        page_content="Full-time employees receive 25 standard annual leave days per calendar year.",
        metadata={"source": "hr_policy_2026.pdf", "section": "Leave Entitlement", "page": 4},
    ),
    Document(
        page_content="Medical absence exceeding three consecutive business days mandates an official medical certificate.",
        metadata={"source": "hr_policy_2026.pdf", "section": "Sick Leave", "page": 8},
    ),
    Document(
        page_content="Engineers are entitled to an annual $1,500 learning stipend for technical certifications and books.",
        metadata={"source": "benefits_handbook.pdf", "section": "Professional Development", "page": 12},
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
        documents=CORPUS,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )
    return vector_db.as_retriever(search_kwargs={"k": 3})


def format_docs(docs):
    formatted = []
    for i, doc in enumerate(docs, 1):
        formatted.append(f"[Source {i} - {doc.metadata.get('source')}]: {doc.page_content}")
    return "\n\n".join(formatted)


def run():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY missing in .env")

    retriever = setup_retriever()

    # Dynamic free router that does not rely on fragile individual slugs
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key.strip(),
        model="openrouter/free",
        temperature=0,
    )

    # Simple, direct prompt structure to avoid triggering guardrail routers
    prompt = ChatPromptTemplate.from_template(
        "Answer the question using ONLY the provided context.\n"
        "Cite the sources using brackets like [Source 1], [Source 2] for each point.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    )

    chain = (
        RunnableParallel(
            context_docs=retriever,
            question=RunnablePassthrough(),
        )
        | RunnableParallel(
            answer=(
                RunnablePassthrough.assign(context=lambda x: format_docs(x["context_docs"]))
                | prompt
                | llm
                | StrOutputParser()
            ),
            sources=lambda x: [
                {
                    "source": doc.metadata.get("source"),
                    "page": doc.metadata.get("page"),
                    "section": doc.metadata.get("section"),
                    "text": doc.page_content,
                }
                for doc in x["context_docs"]
            ],
        )
    )

    print("==================================================")
    print("🔍 DAY 44: EXPLAINABLE RAG & CITATIONS")
    print("==================================================")

    query = "What is the policy regarding sick leave and learning stipends?"
    print(f"\nQuery: {query}\n")

    result = chain.invoke(query)

    print("--- Grounded Answer ---")
    print(result["answer"].strip())

    print("\n--- Source Audit ---")
    for idx, s in enumerate(result["sources"], 1):
        print(f"[{idx}] {s['source']} (Page {s['page']}) - Section: {s['section']}")
        print(f"    Text: \"{s['text']}\"")


if __name__ == "__main__":
    run()