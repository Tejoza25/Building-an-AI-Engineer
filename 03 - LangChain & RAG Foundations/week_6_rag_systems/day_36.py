import os
import re
import numpy as np
from typing import List, Dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load API credentials
load_dotenv(dotenv_path="../.env")

# ---------------------------------------------------------------------------
# 1. Knowledge Base (Simulating Ingested Document Chunks)
# ---------------------------------------------------------------------------
KNOWLEDGE_BASE: List[Dict[str, str]] = [
    {
        "id": "chunk_01",
        "content": "Module 3 focuses on LangChain and RAG Foundations running from Day 29 to Day 56."
    },
    {
        "id": "chunk_02",
        "content": "Project 2 is a custom RAG-based knowledge chatbot that answers questions from documents using Streamlit."
    },
    {
        "id": "chunk_03",
        "content": "The Day 32 agent uses tool-calling capabilities to execute Python functions like calculators."
    },
    {
        "id": "chunk_04",
        "content": "Retrieval-Augmented Generation combines an external retrieval store with a generative LLM."
    }
]

# ---------------------------------------------------------------------------
# 2. Embedding & Vector Math (Deterministic Keyword Vectorizer)
# ---------------------------------------------------------------------------
VOCABULARY = [
    "project", "2", "rag", "knowledge", "chatbot", "streamlit",
    "agent", "tool", "calculator", "langchain", "module", "3",
    "documents", "interface", "built"
]

def mock_embed(text: str) -> np.ndarray:
    """
    Creates a term-frequency vector across key vocabulary words
    so the simulator accurately retrieves relevant chunks.
    """
    tokens = re.findall(r"\w+", text.lower())
    vector = np.zeros(len(VOCABULARY), dtype=float)
    
    for i, word in enumerate(VOCABULARY):
        vector[i] = tokens.count(word)
        
    norm = np.linalg.norm(vector)
    return vector / norm if norm != 0 else vector

def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Calculates directional similarity between two normalized vectors."""
    return float(np.dot(vec_a, vec_b))

def retrieve_top_k(query: str, k: int = 1) -> List[Dict[str, str]]:
    """Simulates vector database retrieval via similarity search."""
    query_vector = mock_embed(query)
    scored_chunks = []

    for item in KNOWLEDGE_BASE:
        chunk_vector = mock_embed(item["content"])
        score = cosine_similarity(query_vector, chunk_vector)
        scored_chunks.append((score, item))

    # Sort descending by similarity score
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return [chunk for _, chunk in scored_chunks[:k]]

# ---------------------------------------------------------------------------
# 3. Augmentation & Synthesis (LCEL Generation Chain)
# ---------------------------------------------------------------------------
def run_rag_pipeline(query: str):
    # Step A: Retrieve relevant context
    retrieved_chunks = retrieve_top_k(query, k=1)
    context_text = "\n".join([f"- {c['content']}" for c in retrieved_chunks])
    
    print(f"Query: {query}")
    print(f"Retrieved Source ID: {retrieved_chunks[0]['id']}")
    print(f"Retrieved Context: {context_text}\n")

    # Step B: Augment Prompt
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "You are a strict, grounded assistant. Answer the question using ONLY the provided context.\n"
            "If the answer cannot be found in the context, respond: 'I do not have sufficient information.'\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Answer:"
        )
    )

    # Step C: Setup Model via OpenRouter auto-free router
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model="openrouter/free",
        temperature=0
    )

    # LCEL Pipeline: Prompt -> LLM -> String Output
    rag_chain = prompt_template | llm | StrOutputParser()

    # Step D: Generate final grounded answer
    response = rag_chain.invoke({
        "context": context_text,
        "question": query
    })

    print("--- Model Response ---")
    print(response)

if __name__ == "__main__":
    sample_query = "What will be built for Project 2 and what interface will it have?"
    run_rag_pipeline(sample_query)