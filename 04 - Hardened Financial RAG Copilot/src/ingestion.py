import os
import re
from pathlib import Path
from typing import List
from langchain_core.documents import Document

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"


def extract_global_metadata(content: str, filename: str) -> dict:
    """Extracts high-level document headers (ticker, period)."""
    ticker_match = re.search(r"\*\*Ticker:\*\*\s*([A-Z]+)", content, re.IGNORECASE)
    if not ticker_match:
        # Fallback to searching common patterns or filename
        if "nvda" in filename.lower() or "nvidia" in content.lower():
            ticker = "NVDA"
        elif "aapl" in filename.lower() or "apple" in content.lower():
            ticker = "AAPL"
        else:
            ticker = "NVDA"
    else:
        ticker = ticker_match.group(1).upper()

    period_match = re.search(r"\*\*Filing Type:\*\*\s*(.+)", content)
    doc_type = period_match.group(1).strip() if period_match else "Form 10-K"

    return {
        "ticker": ticker,
        "source_file": filename,
        "doc_type": doc_type,
    }


def classify_statement_type(header_text: str) -> str:
    """Determines financial category from Markdown headers."""
    lowered = header_text.lower()
    if "income" in lowered or "revenue" in lowered:
        return "Income Statement"
    elif "data center" in lowered or "operations" in lowered:
        return "Segment Operations"
    elif "cash flow" in lowered or "capital" in lowered:
        return "Cash Flow & CapEx"
    elif "risk" in lowered:
        return "Risk Factors"
    return "General MD&A"


def load_and_chunk_sec_markdown(file_path: Path) -> List[Document]:
    """
    Parses SEC Markdown filings preserving markdown tables
    intact within individual chunks.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Missing source filing at: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    global_meta = extract_global_metadata(content, file_path.name)
    
    # Split content on markdown section boundaries (both ## and ###)
    sections = re.split(r"\n(?=#{2,3}\s+)", content)
    documents: List[Document] = []

    for section in sections:
        section = section.strip()
        # Skip empty or top-level title-only headers
        if not section or section.startswith("# ") and not ("|" in section or "revenue" in section.lower()):
            continue

        # Extract section header title
        header_match = re.match(r"#{2,3}\s+(.+)", section)
        section_title = header_match.group(1).split("\n")[0].strip() if header_match else "Overview"
        statement_type = classify_statement_type(section_title)

        # Extract numeric fiscal years
        year_strings = re.findall(r"(?:FY)?(202[3-6])", section)
        years = [int(y) for y in year_strings]
        primary_year = 2025 if 2025 in years else (years[0] if years else 2025)

        chunk_metadata = {
            "ticker": global_meta["ticker"],
            "source_file": global_meta["source_file"],
            "statement_type": statement_type,
            "section_title": section_title,
            "fiscal_year": primary_year,
            "fiscal_period": "FY",
        }

        doc = Document(page_content=section, metadata=chunk_metadata)
        documents.append(doc)

    return documents


if __name__ == "__main__":
    test_file = RAW_DATA_DIR / "nvda_fy24_fy25_10k.md"
    print("==================================================")
    print("🚀 DAY 51: TABLE-AWARE SEC INGESTION PIPELINE")
    print("==================================================")
    print(f"Loading: {test_file.name}\n")

    chunks = load_and_chunk_sec_markdown(test_file)

    print(f"✅ Successfully extracted {len(chunks)} intact chunks.\n")
    for idx, chunk in enumerate(chunks, 1):
        print(f"--- [Chunk {idx}] ---")
        print(f"Metadata: {chunk.metadata}")
        has_table = "|" in chunk.page_content
        print(f"Contains Table: {has_table}")
        preview = chunk.page_content.split("\n")[:2]
        print("Preview:\n" + "\n".join(preview))
        print()