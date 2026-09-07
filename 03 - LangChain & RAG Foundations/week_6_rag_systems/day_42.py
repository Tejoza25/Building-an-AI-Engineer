import os
import time
import shutil
from typing import List
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Load root API keys
load_dotenv(dotenv_path="../.env")

CHROMA_AUDIT_DIR = "data/chroma_day42_audit"

# Comprehensive test knowledge base across Week 6 concepts
RAW_CORPUS = [
    (
        "Day 36 established RAG fundamentals. It decouples parametric model weights "
        "from non-parametric knowledge storage, preventing LLM hallucinations."
    ),
    (
        "Day 37 introduced LangChain Document Loaders like TextLoader and DirectoryLoader "
        "to normalize text and PDF files into standard Document containers with metadata."
    ),
    (
        "Day 38 implemented RecursiveCharacterTextSplitter, configuring chunk_size and "
        "chunk_overlap to preserve semantic boundaries across paragraphs and sentences."
    ),
    (
        "Day 39 transformed raw chunks into 384-dimensional dense vectors using "
        "sentence-transformers/all-MiniLM-L6-v2 with normalized cosine similarity."
    ),
    (
        "Day 40 indexed chunk vectors into Chroma and FAISS vector databases for disk "
        "persistence and Approximate Nearest Neighbor (ANN) sub-second similarity search."
    ),
    (
        "Day 41 wired the Chroma retriever directly to ChatOpenAI via LCEL using "
        "RunnablePassthrough and PromptTemplate for an end-to-end automated pipeline."
    ),
]


def format_retrieved_docs(docs: List[Document]) -> str:
    return "\n\n".join(
        f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
        for doc in docs
    )


def audit_week6_pipeline():
    print("==================================================")
    print("🚀 WEEK 6 MILESTONE AUDIT & PIPELINE VERIFICATION")
    print("==================================================\n")

    start_total = time.time()

    # Step 1: Chunking & Ingestion Verification
    print("Step 1: Chunking Raw Corpus...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=120, chunk_overlap=25)
    documents = [
        Document(page_content=text, metadata={"source": f"module_review_{i}.txt"})
        for i, text in enumerate(RAW_CORPUS, start=36)
    ]
    chunks = splitter.split_documents(documents)
    print(f" -> Generated {len(chunks)} chunks from {len(documents)} source docs.")

    # Step 2: Embeddings & Vector Store Persistence
    print("\nStep 2: Initializing Embeddings & Persisting Chroma DB...")
    if os.path.exists(CHROMA_AUDIT_DIR):
        shutil.rmtree(CHROMA_AUDIT_DIR)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_AUDIT_DIR,
    )
    print(f" -> Persisted vector database to '{CHROMA_AUDIT_DIR}'.")

    # Step 3: Retriever Configuration
    retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 2},
    )

    # Step 4: Strict LCEL RAG Assembly
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "You are a factual AI Engineering evaluation assistant.\n"
            "Answer the question using ONLY the retrieved context below.\n"
            "If the answer cannot be determined from the context, state that you do not know.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Answer:"
        ),
    )

    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model="openrouter/free",
        temperature=0,
    )

    rag_chain = (
        {"context": retriever | format_retrieved_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Step 5: End-to-End Diagnostic Query Runs
    queries = [
        "What model and vector dimension were used on Day 39?",
        "What was the focus of Day 40 in vector databases?",
    ]

    print("\nStep 3: Running Diagnostic Queries Through Chain...")
    for q in queries:
        t0 = time.time()
        answer = rag_chain.invoke(q)
        duration = time.time() - t0
        print(f"\n[Query]: {q}")
        print(f"[Latency]: {duration:.2f}s")
        print(f"[Answer]:\n{answer.strip()}")

    total_time = time.time() - start_total
    print(f"\n==================================================")
    print(f"✅ Week 6 Diagnostic Completed Successfully in {total_time:.2f}s")
    print("==================================================")


if __name__ == "__main__":
    audit_week6_pipeline()