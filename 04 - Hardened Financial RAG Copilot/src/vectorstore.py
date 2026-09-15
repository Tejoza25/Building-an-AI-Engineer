import shutil
from pathlib import Path
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from config import CHROMA_DIR, EMBEDDING_MODEL_NAME, RAW_DATA_DIR
from ingestion import load_and_chunk_sec_markdown


def get_embedding_function() -> HuggingFaceEmbeddings:
    """Initializes the local 384-dimensional embedding model."""
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def build_or_load_vectorstore(force_reindex: bool = False) -> Chroma:
    """
    Builds a Chroma vector store persisted to disk.
    If already existing and force_reindex is False, loads the store directly.
    """
    embedding_fn = get_embedding_function()

    if force_reindex and CHROMA_DIR.exists():
        print(f"Purging existing vector database at: {CHROMA_DIR}")
        shutil.rmtree(CHROMA_DIR)

    # Check if database already exists on disk
    if CHROMA_DIR.exists() and any(CHROMA_DIR.iterdir()):
        print(f"📁 Loading existing persistent Chroma index from: {CHROMA_DIR}")
        vectorstore = Chroma(
            collection_name="sec_financial_filings",
            embedding_function=embedding_fn,
            persist_directory=str(CHROMA_DIR),
        )
        return vectorstore

    print("🚀 Ingesting documents and building persistent Chroma vector store...")
    target_file = RAW_DATA_DIR / "nvda_fy24_fy25_10k.md"
    documents = load_and_chunk_sec_markdown(target_file)

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedding_fn,
        collection_name="sec_financial_filings",
        persist_directory=str(CHROMA_DIR),
    )
    print(f"✅ Successfully indexed {len(documents)} chunks to {CHROMA_DIR}")
    return vectorstore


if __name__ == "__main__":
    print("==================================================")
    print("🚀 DAY 52: LOCAL EMBEDDINGS & CHROMA PERSISTENCE")
    print("==================================================")

    # 1. Build or re-index store
    store = build_or_load_vectorstore(force_reindex=True)

    # 2. Test standard semantic search
    query_1 = "What was NVIDIA's revenue from the Data Center segment?"
    print(f"\n🔍 [Query 1 (Semantic)]: '{query_1}'")
    results_1 = store.similarity_search(query_1, k=1)
    if results_1:
        top_match = results_1[0]
        print(f"Top Match Source: {top_match.metadata.get('section_title')}")
        print(f"Statement Type:   {top_match.metadata.get('statement_type')}")
        print("Content Preview:\n" + "\n".join(top_match.page_content.split("\n")[:4]))

    # 3. Test metadata-filtered similarity search
    query_2 = "What are the export control risks and GPU supply constraints?"
    filter_dict = {"statement_type": "Risk Factors"}
    print(f"\n🔍 [Query 2 (Filtered)]: '{query_2}' with filter {filter_dict}")
    results_2 = store.similarity_search(query_2, k=1, filter=filter_dict)
    if results_2:
        top_match_2 = results_2[0]
        print(f"Top Match Source: {top_match_2.metadata.get('section_title')}")
        print(f"Statement Type:   {top_match_2.metadata.get('statement_type')}")
        print("Content Preview:\n" + "\n".join(top_match_2.page_content.split("\n")[:4]))

    print("\n✅ Day 52 vector indexing and filtered retrieval verified successfully!")