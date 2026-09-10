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

CHROMA_DIR = "data/chroma_day48"

# Knowledge base
DOCUMENTS = [
    Document(
        page_content="API rate limits for Tier 1 enterprise keys are capped at 10,000 requests per minute.",
        metadata={"source": "api_specs.md"},
    ),
    Document(
        page_content="Data retention for application logs is strictly 30 days before automatic archival to Glacier.",
        metadata={"source": "compliance_specs.md"},
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
    return vector_db.as_retriever(search_kwargs={"k": 1})


def get_llm():
    """Resolves credentials prioritizing OpenAI, falling back to OpenRouter free router."""
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()

    if openai_key and openai_key.startswith("sk-") and not openai_key.startswith("sk-or-"):
        return ChatOpenAI(api_key=openai_key, model="gpt-4o-mini", temperature=0)
    elif openrouter_key:
        return ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_key,
            model="openrouter/free",
            temperature=0,
        )
    raise ValueError("No valid API credentials found in .env")


def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


def evaluate_faithfulness(llm, context: str, answer: str) -> str:
    """Evaluates if the answer contains hallucinated facts outside the retrieved context."""
    eval_prompt = ChatPromptTemplate.from_template(
        "You are an impartial evaluator auditing an AI response for groundedness.\n"
        "Analyze the following context and answer.\n\n"
        "Context:\n{context}\n\n"
        "Answer:\n{answer}\n\n"
        "Task: Determine if every fact in the answer is completely supported by the context.\n"
        "Respond with EXACTLY 'PASSED: Faithfully Grounded' or 'FAILED: Hallucination Detected', "
        "followed by a one-sentence rationale."
    )
    eval_chain = eval_prompt | llm | StrOutputParser()
    return eval_chain.invoke({"context": context, "answer": answer})


def run_rag_eval_benchmark():
    retriever = setup_retriever()
    llm = get_llm()

    # RAG Generation Chain
    rag_prompt = ChatPromptTemplate.from_template(
        "Answer the question based ONLY on the context.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    )

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    # Execute RAG query
    query = "What is the log retention limit and API rate limit?"
    retrieved_docs = retriever.invoke(query)
    context_text = format_docs(retrieved_docs)
    generated_answer = rag_chain.invoke(query)

    print("==================================================")
    print("📊 DAY 48: RAG EVALUATION BENCHMARK")
    print("==================================================")
    print(f"Query: {query}\n")
    print(f"Retrieved Context:\n{context_text}\n")
    print(f"Generated Answer:\n{generated_answer.strip()}\n")

    print("--- Running Automated Faithfulness Audit ---")
    eval_verdict = evaluate_faithfulness(llm, context_text, generated_answer)
    print(f"Verdict:\n{eval_verdict.strip()}")
    print("==================================================")


if __name__ == "__main__":
    run_rag_eval_benchmark()