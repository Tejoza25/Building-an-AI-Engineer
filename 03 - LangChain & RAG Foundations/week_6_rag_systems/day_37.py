import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader

# ---------------------------------------------------------------------------
# 1. Single Text File Ingestion
# ---------------------------------------------------------------------------
def test_text_loader():
    print("=== 1. Testing TextLoader ===")
    file_path = "data/sample.txt"
    
    loader = TextLoader(file_path, encoding="utf-8")
    docs = loader.load()
    
    for doc in docs:
        print(f"Loaded Object: {type(doc)}")
        print(f"Metadata: {doc.metadata}")
        print(f"Content:\n{doc.page_content.strip()}\n")

# ---------------------------------------------------------------------------
# 2. Markdown File Ingestion
# ---------------------------------------------------------------------------
def test_markdown_loader():
    print("=== 2. Testing Markdown Loading ===")
    file_path = "data/sample.md"
    
    loader = TextLoader(file_path, encoding="utf-8")
    docs = loader.load()
    
    for doc in docs:
        print(f"Metadata: {doc.metadata}")
        print(f"Content Preview:\n{doc.page_content.strip()[:100]}...\n")

# ---------------------------------------------------------------------------
# 3. Directory Batch Ingestion
# ---------------------------------------------------------------------------
def test_directory_loader():
    print("=== 3. Testing DirectoryLoader Batch Ingestion ===")
    dir_loader = DirectoryLoader(
        path="data",
        glob="**/*.*",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True
    )
    
    all_docs = dir_loader.load()
    print(f"\nTotal documents loaded: {len(all_docs)}")
    for i, doc in enumerate(all_docs, 1):
        print(f"[Doc {i}] Source: {doc.metadata.get('source')}")
        print(f"Content Snippet: {doc.page_content.strip()[:50]}...\n")

if __name__ == "__main__":
    test_text_loader()
    test_markdown_loader()
    test_directory_loader()