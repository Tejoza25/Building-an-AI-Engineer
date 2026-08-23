# 📅 Day 34 — Vector Stores & Embeddings

**Date:** Day 34 of 90
**Module:** 3 — LangChain & RAG Foundations
**Week:** 5 — LangChain Basics
**Goal:** Understand embeddings and build my first vector store with FAISS.

---

## 🎯 What I Learned Today

### From Text to Numbers

Computers can't compare the *meaning* of text directly. They need numbers. **Embeddings** convert text into high-dimensional vectors where similar meanings produce similar numbers.

### What Is an Embedding?

An embedding is a list of numbers that represents the **semantic meaning** of text:

```text
"The cat sat on the mat"
→ [0.12, -0.45, 0.78, 0.33, ..., 0.91]
   ↑
   1536 numbers for OpenAI's text-embedding-3-small
   384 numbers for sentence-transformers

   Similar texts have similar vectors. The word "cat" and "kitten" would produce vectors that are very close together.

Cosine Similarity
We measure how close two embeddings are using cosine similarity — the cosine of the angle between two vectors:

Score	Meaning
1.0	Identical meaning
0.7–0.9	Very similar
0.3–0.7	Somewhat related
0.0	No relationship
-1.0	Opposite meaning
For example:

"I love programming" and "I enjoy coding" → ~0.85 (very similar)
"I love programming" and "Pizza is delicious" → ~0.10 (unrelated)
What Is a Vector Database?
A vector database stores embeddings and lets you search by similarity:

Add: Store text + its embedding
Search: Given a query, find the N most similar stored texts
Return: Original texts that are closest in meaning
FAISS vs Chroma
Feature	FAISS	Chroma
Speed	Very fast	Fast
Storage	In-memory	Persistent (saves to disk)
Setup	Simple	Simple
Best for	Prototyping, demos	Production, persistence
LangChain integration	Excellent	Excellent
For Day 34, I used FAISS for simplicity. For the RAG project later, Chroma is better because it persists data.

Embedding Models
I used sentence-transformers (free, runs locally) instead of OpenAI embeddings:

OpenAI embeddings — high quality, costs money
sentence-transformers — free, runs locally, decent quality
HuggingFace embeddings — many models to choose from
For learning and small projects, sentence-transformers is ideal. For production, OpenAI or Cohere are better.

My Day 34 Project
I built a simple document search system:

Created 5 sample documents about different topics
Generated embeddings for each document
Stored them in a FAISS vector store
Searched the store with various queries
Retrieved the most relevant documents
Example:

Query: "Tell me about machine learning"
Result: Document about AI/ML (similarity: 0.82)
        Document about data science (similarity: 0.65)
        Document about cooking (similarity: 0.12)
💻 What I Built
✅ A FAISS vector store with 5 sample documents ✅ An embedding pipeline using sentence-transformers ✅ A similarity search function ✅ Multiple test queries showing relevance ranking ✅ Printed similarity scores

🧠 Key Concepts to Remember
Concept	Description
Embedding	Vector representation of text meaning
Cosine similarity	Measure of how similar two embeddings are
Vector database	Stores embeddings for fast similarity search
FAISS	Fast, in-memory vector database
Chroma	Persistent vector database
sentence-transformers	Free, local embedding model
k-NN search	Find the k most similar vectors
🔜 Tomorrow (Day 35)
Week 5 review — I'll reflect on the 6 days of LangChain work, polish documentation, and push everything to GitHub.

Then Week 6 (Days 36-42) covers RAG fundamentals:

What is RAG?
Document loaders
Text splitters and chunking
Building a complete RAG pipeline
Improving retrieval quality
📚 Resources
YouTube: "Visualizing Embeddings 3Blue1Brown"
YouTube: "Vector database FAISS Chroma tutorial"
LangChain docs: https://python.langchain.com/docs/concepts/vectorstores
FAISS: https://faiss.ai
Chroma: https://www.trychroma.com
sentence-transformers: https://www.sbert.net
⭐ Why This Matters
Vector stores are the foundation of every modern AI application:

RAG (Retrieval-Augmented Generation) — searches documents before answering
Semantic search — Google-style "find similar" features
Recommendation systems — "users who liked X also liked Y"
Document Q&A — ChatGPT for your PDFs, Notion, Slack history
The skills I learned today will apply directly to Project 2 (RAG chatbot) in Week 7.