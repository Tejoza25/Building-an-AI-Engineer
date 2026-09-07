import os
import shutil
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS

# ---------------------------------------------------------------------------
# 1. Setup Local Embeddings
# ---------------------------------------------------------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

# ---------------------------------------------------------------------------
# 2. Sample Ingested Chunks (Simulating Days 37 & 38)
# ---------------------------------------------------------------------------
SAMPLE_DOCUMENTS = [
    Document(
        page_content="LangChain Document Loaders parse unstructured files like PDF and Markdown.",
        metadata={"source": "loaders.txt", "topic": "ingestion", "difficulty": "beginner"},
    ),
    Document(
        page_content="RecursiveCharacterTextSplitter maintains semantic coherence with chunk overlap.",
        metadata={"source": "splitters.txt", "topic": "chunking", "difficulty": "intermediate"},
    ),
    Document(
        page_content="Vector embeddings map words and sentences into high-dimensional coordinate spaces.",
        metadata={"source": "embeddings.txt", "topic": "embeddings", "difficulty": "intermediate"},
    ),
    Document(
        page_content="Chroma and FAISS store vector embeddings and perform sub-second similarity search.",
        metadata={"source": "vectorstores.txt", "topic": "storage", "difficulty": "advanced"},
    ),
]

CHROMA_DIR = "data/chroma_db"
FAISS_DIR = "data/faiss_index"


# ---------------------------------------------------------------------------
# 3. Chroma: Persistent Storage & Metadata Filtering
# ---------------------------------------------------------------------------
def demonstrate_chroma():
    print("=== 1. Persistent Vector Store (Chroma) ===")

    # Clean existing test directory for repeatable runs
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    # Ingest and persist documents to disk
    vector_db = Chroma.from_documents(
        documents=SAMPLE_DOCUMENTS,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )
    print(f"Indexed {len(SAMPLE_DOCUMENTS)} documents into Chroma at '{CHROMA_DIR}'.")

    # A. Basic Similarity Search
    query = "How do we split text documents?"
    results = vector_db.similarity_search(query, k=1)
    print(f"\nQuery: '{query}'")
    print(f"Top Result: '{results[0].page_content}' | Source: {results[0].metadata['source']}")

    # B. Metadata Filtering Search
    filtered_query = "Tell me about data pipelines"
    filtered_results = vector_db.similarity_search(
        filtered_query,
        k=2,
        filter={"difficulty": "intermediate"},
    )
    print(f"\nFiltered Query (difficulty == intermediate): '{filtered_query}'")
    for doc in filtered_results:
        print(f"- [{doc.metadata['topic']}] {doc.page_content}")


# ---------------------------------------------------------------------------
# 4. FAISS: Fast In-Memory Search & Manual Serialization
# ---------------------------------------------------------------------------
def demonstrate_faiss():
    print("\n=== 2. High-Throughput Search & Serialization (FAISS) ===")

    # Create in-memory index
    faiss_db = FAISS.from_documents(SAMPLE_DOCUMENTS, embeddings)

    # Save to disk
    os.makedirs(FAISS_DIR, exist_ok=True)
    faiss_db.save_local(FAISS_DIR)
    print(f"FAISS index saved locally at '{FAISS_DIR}'.")

    # Reload from disk
    reloaded_faiss = FAISS.load_local(
        FAISS_DIR, embeddings, allow_dangerous_deserialization=True
    )

    query = "Where are vector embeddings stored?"
    results_with_scores = reloaded_faiss.similarity_search_with_score(query, k=2)

    print(f"\nQuery: '{query}'")
    for doc, score in results_with_scores:
        print(f"Distance Score: {score:.4f} | Chunk: {doc.page_content}")


if __name__ == "__main__":
    demonstrate_chroma()
    demonstrate_faiss()