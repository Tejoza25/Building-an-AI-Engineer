from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)
from langchain_community.document_loaders import TextLoader

# ---------------------------------------------------------------------------
# Sample Raw Text for Inspection
# ---------------------------------------------------------------------------
SAMPLE_PARAGRAPH = """Chunking is a core pre-processing stage in Retrieval-Augmented Generation.
Without chunking, large documents cannot fit cleanly into embedding models or vector spaces.

When chunking text, we must balance chunk size with context retention.
If a chunk is too small, it loses core meaning.
If a chunk is too large, search relevance degrades due to noise.

Chunk overlap resolves edge-boundary context loss.
By repeating trailing tokens from one chunk at the start of the next,
semantic completeness is maintained across split boundaries."""


def demonstrate_character_splitter():
    print("=== 1. Naive CharacterTextSplitter ===")
    splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=120,
        chunk_overlap=20,
        length_function=len,
    )
    chunks = splitter.split_text(SAMPLE_PARAGRAPH)
    for i, chunk in enumerate(chunks, 1):
        print(f"[Chunk {i}] ({len(chunk)} chars):\n{repr(chunk)}\n")


def demonstrate_recursive_splitter():
    print("=== 2. Production RecursiveCharacterTextSplitter ===")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=140,
        chunk_overlap=30,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_text(SAMPLE_PARAGRAPH)
    for i, chunk in enumerate(chunks, 1):
        print(f"[Chunk {i}] ({len(chunk)} chars):\n{chunk}")
        print("-" * 30)


def demonstrate_document_chunking():
    print("=== 3. Splitting Day 37 Ingested Document Objects ===")
    # Load document from Day 37 data path
    loader = TextLoader("data/sample.txt", encoding="utf-8")
    raw_docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=90,
        chunk_overlap=15,
    )
    split_docs = splitter.split_documents(raw_docs)

    print(f"Original Document count: {len(raw_docs)}")
    print(f"Generated Split Chunks: {len(split_docs)}")
    for i, doc in enumerate(split_docs, 1):
        print(f"\n[Chunk {i}] Metadata: {doc.metadata}")
        print(f"Content: {doc.page_content}")


def demonstrate_markdown_header_splitter():
    print("\n=== 4. Markdown Structural Splitting ===")
    markdown_document = """# System Architecture
RAG architectures combine information retrieval with language generation.

## Ingestion
Ingestion loads and splits raw files into indexable vectors.

## Retrieval
Retrieval identifies relevant context using distance metrics."""

    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
    ]

    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )
    md_chunks = md_splitter.split_text(markdown_document)

    for i, chunk in enumerate(md_chunks, 1):
        print(f"[MD Chunk {i}] Metadata: {chunk.metadata}")
        print(f"Content: {chunk.page_content}\n")


if __name__ == "__main__":
    demonstrate_character_splitter()
    demonstrate_recursive_splitter()
    demonstrate_document_chunking()
    demonstrate_markdown_header_splitter()