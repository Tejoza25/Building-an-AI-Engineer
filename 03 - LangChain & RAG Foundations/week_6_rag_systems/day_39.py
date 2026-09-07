import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

# ---------------------------------------------------------------------------
# 1. Initialize Local Embedding Model
# ---------------------------------------------------------------------------
# Uses all-MiniLM-L6-v2: fast, runs locally on CPU, 384 dimensions
embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)


def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Calculates cosine similarity between two unit-normalized vectors."""
    return float(np.dot(vec_a, vec_b))


# ---------------------------------------------------------------------------
# 2. Embedding Inspection
# ---------------------------------------------------------------------------
def demonstrate_single_embedding():
    print("=== 1. Inspecting Vector Embeddings ===")
    sample_text = "Retrieval-Augmented Generation improves LLM accuracy."
    vector = embeddings_model.embed_query(sample_text)

    print(f"Text: '{sample_text}'")
    print(f"Vector Dimensions: {len(vector)}")
    print(f"First 5 Vector Components: {[round(x, 4) for x in vector[:5]]}\n")


# ---------------------------------------------------------------------------
# 3. Semantic Similarity vs. Keyword Mismatch
# ---------------------------------------------------------------------------
def demonstrate_similarity_search():
    print("=== 2. Semantic Similarity Comparison ===")
    query = "How to fix a flat tire?"

    candidates = [
        "Steps to replace a punctured car wheel.",  # High semantic match, zero word overlap
        "A recipe for baking chocolate chip cookies.",  # Completely irrelevant
        "The tire was round and flat on the ground.",  # High keyword overlap, wrong intent
    ]

    query_vec = np.array(embeddings_model.embed_query(query))
    candidate_vecs = embeddings_model.embed_documents(candidates)

    print(f"Query: '{query}'\n")
    for text, vec in zip(candidates, candidate_vecs):
        sim = cosine_similarity(query_vec, np.array(vec))
        print(f"Score: {sim:.4f} | Document: '{text}'")


# ---------------------------------------------------------------------------
# 4. Embedding Day 38 Chunks
# ---------------------------------------------------------------------------
def demonstrate_chunk_embedding():
    print("\n=== 3. Embedding Day 38 Document Chunks ===")
    chunks = [
        "LangChain Document Loaders bridge raw files and vector retrieval pipelines.",
        "They parse unstructured text while preserving vital provenance in metadata.",
        "Standardizing incoming data simplifies downstream text splitting.",
    ]

    embedded_chunks = embeddings_model.embed_documents(chunks)
    print(f"Total Chunks Embedded: {len(embedded_chunks)}")
    print(f"Dimension per Chunk: {len(embedded_chunks[0])}")


if __name__ == "__main__":
    demonstrate_single_embedding()
    demonstrate_similarity_search()
    demonstrate_chunk_embedding()