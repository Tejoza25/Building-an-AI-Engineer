import os
import sys
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

# Load .env from current directory or parent paths
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

CHROMA_DIR = "data/chroma_day45"

# Corporate knowledge documents
CORPUS = [
    Document(
        page_content="Engineering team members have a $1,500 annual budget for attending tech conferences and books.",
        metadata={"source": "benefits_guide.pdf", "category": "L&D"},
    ),
    Document(
        page_content="Core working hours are 10:00 AM to 4:00 PM EST. Async communication is expected for status updates.",
        metadata={"source": "engineering_playbook.pdf", "category": "Operations"},
    ),
    Document(
        page_content="Production access requires multi-factor authentication (MFA) and explicit sign-off from team leads.",
        metadata={"source": "security_protocols.pdf", "category": "Infra"},
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
        documents=CORPUS,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )
    return vector_db.as_retriever(search_kwargs={"k": 2})


def format_docs(docs):
    """Formats context documents with reference headers."""
    formatted = []
    for i, doc in enumerate(docs, 1):
        formatted.append(f"[Ref {i} - {doc.metadata.get('source')}]: {doc.page_content}")
    return "\n\n".join(formatted)


def get_llm():
    """Resolves available credentials from .env prioritizing OpenAI, falling back to OpenRouter."""
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()

    if openai_key and openai_key.startswith("sk-") and not openai_key.startswith("sk-or-"):
        print("Authenticating with OpenAI (gpt-4o-mini)...")
        return ChatOpenAI(
            api_key=openai_key,
            model="gpt-4o-mini",
            temperature=0,
            streaming=True,
        )

    if openrouter_key:
        print("Authenticating with OpenRouter (openrouter/free)...")
        return ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_key,
            model="openrouter/free",
            temperature=0,
            streaming=True,
        )

    raise ValueError("No valid OPENAI_API_KEY or OPENROUTER_API_KEY found in .env")


def run_streaming_rag():
    retriever = setup_retriever()
    llm = get_llm()

    prompt = ChatPromptTemplate.from_template(
        "You are an engineering copilot. Answer the question using ONLY the provided context.\n"
        "Cite the reference tag (e.g., [Ref 1]) when stating facts.\n"
        "If the answer cannot be determined from the context, state that you do not know.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    )

    # LCEL Streaming Pipeline
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    query = "What are the rules regarding core hours and educational stipends?"

    print("==================================================")
    print("⚡ DAY 45: REAL-TIME TOKEN STREAMING RAG")
    print("==================================================")
    print(f"Query: {query}\n")
    print("Streaming Response: ", end="", flush=True)

    # Stream output token-by-token using standard LCEL .stream()
    for chunk in rag_chain.stream(query):
        sys.stdout.write(chunk)
        sys.stdout.flush()

    print("\n\n--- Streaming Complete ---")


if __name__ == "__main__":
    run_streaming_rag()