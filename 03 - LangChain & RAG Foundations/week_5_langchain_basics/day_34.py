"""
Day 34 - Vector Stores & Embeddings

Goal: Build my first vector database using FAISS and sentence-transformers.
Learn how to store document embeddings and search by semantic similarity.

This script demonstrates:
- Generating embeddings with sentence-transformers
- Storing embeddings in FAISS
- Performing similarity search
- Ranking documents by relevance

Author: Tejoz
"""

import os
import sys

from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ============================================================
# CONFIGURATION
# ============================================================

# Use a small, fast embedding model that runs locally
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# ============================================================
# ENVIRONMENT
# ============================================================

from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Note: We don't need OpenRouter API for this script — embeddings run locally


# ============================================================
# SAMPLE DOCUMENTS
# ============================================================

DOCUMENTS = [
    {
        "id": 1,
        "title": "Introduction to Python",
        "content": (
            "Python is a high-level programming language known for its "
            "simplicity and readability. It is widely used in web development, "
            "data science, and artificial intelligence."
        ),
    },
    {
        "id": 2,
        "title": "Machine Learning Basics",
        "content": (
            "Machine learning is a subset of artificial intelligence that "
            "enables computers to learn from data without being explicitly "
            "programmed. Common algorithms include linear regression, decision "
            "trees, and neural networks."
        ),
    },
    {
        "id": 3,
        "title": "Italian Cooking",
        "content": (
            "Italian cuisine is famous for its pasta, pizza, and risotto dishes. "
            "Traditional recipes use fresh ingredients like tomatoes, basil, "
            "olive oil, and parmesan cheese. Each region has its own specialties."
        ),
    },
    {
        "id": 4,
        "title": "Deep Learning and Neural Networks",
        "content": (
            "Deep learning uses multi-layer neural networks to learn complex "
            "patterns from large datasets. It powers modern AI systems like "
            "image recognition, language models, and self-driving cars."
        ),
    },
    {
        "id": 5,
        "title": "Travel in Japan",
        "content": (
            "Japan offers a unique blend of traditional and modern experiences. "
            "Visit Tokyo for cutting-edge technology, Kyoto for ancient temples, "
            "and Hokkaido for beautiful nature and skiing."
        ),
    },
]


# ============================================================
# DEMO
# ============================================================

def main() -> None:
    """Build a vector store and demonstrate similarity search."""

    print("=" * 60)
    print("🔍 LangChain Day 34 — Vector Stores & Embeddings")
    print("=" * 60)
    print()

    # Step 1: Load the embedding model
    print(f"⏳ Loading embedding model: {EMBEDDING_MODEL}")
    print("   (First run downloads the model — may take a minute)\n")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
    )

    print("✅ Embedding model loaded!\n")

    # Step 2: Create the vector store from documents
    print("⏳ Creating FAISS vector store from documents...\n")

    texts = [doc["content"] for doc in DOCUMENTS]
    metadatas = [{"title": doc["title"], "id": doc["id"]} for doc in DOCUMENTS]

    vector_store = FAISS.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
    )

    print(f"✅ Vector store created with {len(DOCUMENTS)} documents!\n")

    # Step 3: Test queries
    test_queries = [
        "Tell me about AI and neural networks",
        "What's the best food in Italy?",
        "I want to learn programming",
        "Where should I go on vacation in Asia?",
        "How do computers learn from data?",
    ]

    print("=" * 60)
    print("🔎 SEMANTIC SEARCH RESULTS")
    print("=" * 60)

    for query in test_queries:
        print(f"\n❓ Query: '{query}'")
        print("-" * 60)

        # Search for top 3 most similar documents
        results = vector_store.similarity_search_with_score(query, k=3)

        for i, (doc, score) in enumerate(results, 1):
            # FAISS returns distance, lower is better
            # Convert distance to similarity score (1 - normalized distance)
            similarity = 1 / (1 + score)

            print(f"\n   Rank {i}: (similarity: {similarity:.3f})")
            print(f"   Title: {doc.metadata['title']}")
            print(f"   Content: {doc.page_content[:100]}...")

        print()

    # Step 4: Save the vector store to disk
    save_path = "faiss_index"
    vector_store.save_local(save_path)
    print(f"\n💾 Vector store saved to: {save_path}/")
    print("   (You can reload it later with: FAISS.load_local())\n")

    print("=" * 60)
    print("✅ Day 34 demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
