import os
from typing import List
from operator import itemgetter

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

from config import OPENAI_API_KEY, OPENROUTER_API_KEY, PRIMARY_MODEL
from vectorstore import build_or_load_vectorstore


def get_llm():
    """Builds primary LLM with automatic fallback routing across verified providers."""
    candidates = []

    # 1. Direct OpenAI Model (used if valid account key is present)
    if OPENAI_API_KEY and OPENAI_API_KEY.startswith("sk-") and not OPENAI_API_KEY.startswith("sk-or-"):
        candidates.append(
            ChatOpenAI(
                api_key=OPENAI_API_KEY,
                model=PRIMARY_MODEL,
                temperature=0,
            )
        )

    # 2. OpenRouter Dynamic Free Router (Proven in Days 43 & 45)
    if OPENROUTER_API_KEY:
        candidates.append(
            ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=OPENROUTER_API_KEY,
                model="openrouter/free",
                temperature=0,
            )
        )
        # Additional backup free models in case of dynamic routing spikes
        candidates.append(
            ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=OPENROUTER_API_KEY,
                model="meta-llama/llama-3.1-8b-instruct:free",
                temperature=0,
            )
        )
        candidates.append(
            ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=OPENROUTER_API_KEY,
                model="mistralai/mistral-small-24b-instruct-2501:free",
                temperature=0,
            )
        )

    if not candidates:
        raise ValueError("No valid OPENAI_API_KEY or OPENROUTER_API_KEY detected in environment.")

    primary = candidates[0]
    fallbacks = candidates[1:]

    if fallbacks:
        return primary.with_fallbacks(fallbacks)
    return primary


def format_docs_with_sources(docs: List[Document]) -> str:
    """Formats document chunks preserving markdown table layout with source tags."""
    formatted_chunks = []
    for idx, doc in enumerate(docs, 1):
        source_id = f"[Source {idx}: {doc.metadata.get('source_file', 'SEC Filing')} | Section: {doc.metadata.get('section_title', 'MD&A')}]"
        formatted_chunks.append(f"{source_id}\n{doc.page_content}")
    return "\n\n---\n\n".join(formatted_chunks)


def build_financial_copilot_chain():
    """Builds the complete dual-track conversational financial RAG pipeline."""
    llm = get_llm()
    store = build_or_load_vectorstore(force_reindex=False)
    retriever = store.as_retriever(search_kwargs={"k": 2})

    # 1. Query Contextualizer: Resolves pronouns in follow-ups
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "Given a chat history and the latest user question which might reference context in the chat history, "
            "formulate a standalone question which can be understood without the chat history. "
            "Do NOT answer the question, just reformulate it if needed and otherwise return it as is."
        )),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ])
    contextualize_q_chain = contextualize_q_prompt | llm | StrOutputParser()

    def resolve_question(input_dict):
        if not input_dict.get("chat_history"):
            return input_dict["question"]
        return contextualize_q_chain.invoke(input_dict)

    # 2. Strict Factual Synthesis Prompt
    qa_system_prompt = (
        "You are an enterprise Financial Compliance and SEC Filing Copilot.\n"
        "Answer the question using ONLY the provided audited context excerpts below.\n\n"
        "STRICT GUARDRAILS:\n"
        "1. Quote numerical figures exactly as they appear in the markdown tables.\n"
        "2. Do NOT extrapolate, speculate, or compute unstated financial ratios.\n"
        "3. If the requested information or metric is not present in the context, explicitly state: "
        "'Data not disclosed in the provided filing sections.'\n"
        "4. Attach citation tags like [Source 1] to each factual figure.\n\n"
        "AUDITED CONTEXT:\n{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ])

    # 3. Dual-Track Execution Pipeline via RunnableParallel
    rag_chain = (
        RunnableParallel({
            "resolved_query": RunnableLambda(resolve_question),
            "chat_history": itemgetter("chat_history"),
            "raw_question": itemgetter("question"),
        })
        | RunnableParallel({
            "context_docs": itemgetter("resolved_query") | retriever,
            "chat_history": itemgetter("chat_history"),
            "question": itemgetter("resolved_query"),
        })
        | RunnableParallel({
            "answer": (
                {
                    "context": lambda x: format_docs_with_sources(x["context_docs"]),
                    "chat_history": itemgetter("chat_history"),
                    "question": itemgetter("question"),
                }
                | qa_prompt
                | llm
                | StrOutputParser()
            ),
            "sources": itemgetter("context_docs"),
            "standalone_question": itemgetter("question"),
        })
    )

    return rag_chain


if __name__ == "__main__":
    from langchain_core.messages import HumanMessage, AIMessage

    print("==================================================")
    print("🚀 DAY 53: CONVERSATIONAL FINANCIAL RAG CHAIN")
    print("==================================================")

    copilot = build_financial_copilot_chain()

    # Turn 1: Initial Query
    turn1_q = "What was NVIDIA's revenue from the Data Center segment in FY2025?"
    print(f"\n💬 Human: {turn1_q}")
    result1 = copilot.invoke({"question": turn1_q, "chat_history": []})
    print(f"🤖 Copilot:\n{result1['answer']}")
    print(f"\n📎 Audited Provenance Chunks Retained: {len(result1['sources'])}")

    # Turn 2: Follow-up Query testing pronoun resolution ("it")
    history = [
        HumanMessage(content=turn1_q),
        AIMessage(content=result1["answer"]),
    ]
    turn2_q = "How much did it grow compared to Fiscal 2024?"
    print(f"\n💬 Human (Follow-up): {turn2_q}")
    result2 = copilot.invoke({"question": turn2_q, "chat_history": history})
    print(f"🔍 Reformulated Standalone Query: '{result2['standalone_question']}'")
    print(f"🤖 Copilot:\n{result2['answer']}")