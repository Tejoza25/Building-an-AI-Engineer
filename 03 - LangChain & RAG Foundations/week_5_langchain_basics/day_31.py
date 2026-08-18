"""
Day 31 - Output Parsers & Structured Data

Goal: Extract structured data (typed objects) from LLM responses using
Pydantic models and LangChain's structured output features.

This script demonstrates:
- Pydantic BaseModel for defining output schemas
- PydanticOutputParser (explicit parsing)
- with_structured_output() method (modern approach)
- Real-world example: extracting structured info from movie reviews

Author: Tejoz
"""

import os
import sys

from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


# ============================================================
# CONFIGURATION
# ============================================================

MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"
TEMPERATURE = 0.2  # Low for consistent structured output
TIMEOUT = 30


# ============================================================
# ENVIRONMENT
# ============================================================

from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("❌ OPENROUTER_API_KEY is not set.")
    print(f"Looking for .env at: {env_path}")
    print(f"File exists: {env_path.exists()}")
    sys.exit(1)


# ============================================================
# OUTPUT SCHEMA (Pydantic Model)
# ============================================================

class MovieReview(BaseModel):
    """Structured representation of a movie review."""

    title: str = Field(
        description="The title of the movie being reviewed."
    )

    rating: float = Field(
        description="The numeric rating given in the review, on a scale of 1 to 10."
    )

    sentiment: str = Field(
        description="Overall sentiment of the review: 'positive', 'negative', or 'neutral'."
    )

    key_points: list[str] = Field(
        description="The 2-4 most important points mentioned in the review."
    )

    recommendation: str = Field(
        description="Short recommendation: 'must_watch', 'worth_watching', or 'skip'."
    )


# ============================================================
# LLM SETUP
# ============================================================

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    model=MODEL,
    temperature=TEMPERATURE,
    timeout=TIMEOUT,
)


# ============================================================
# APPROACH 1: PydanticOutputParser (Explicit)
# ============================================================

def build_explicit_chain():
    """Build a chain using the explicit PydanticOutputParser."""

    parser = PydanticOutputParser(pydantic_object=MovieReview)

    prompt = PromptTemplate(
        template=(
            "You are an expert movie review analyzer.\n"
            "\n"
            "Extract structured information from the following review.\n"
            "\n"
            "{format_instructions}\n"
            "\n"
            "Review:\n"
            "{review}\n"
        ),
        input_variables=["review"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser

    return chain


# ============================================================
# APPROACH 2: with_structured_output() (Modern)
# ============================================================

def build_modern_chain():
    """Build a chain using the modern with_structured_output() method."""

    structured_llm = llm.with_structured_output(MovieReview)

    return structured_llm


# ============================================================
# DEMO
# ============================================================

SAMPLE_REVIEWS = [
    (
        "I just watched Inception last night and it absolutely blew my mind. "
        "The visual effects were stunning, the plot was intricate but coherent, "
        "and Hans Zimmer's score was phenomenal. Christopher Nolan is a genius. "
        "I'd give it a 9.5 out of 10 — easily one of the best films of the decade. "
        "If you haven't seen it, you must watch it immediately!"
    ),
    (
        "Honestly, I was really disappointed with the new Marvel movie. "
        "The plot had more holes than Swiss cheese, the dialogue felt forced, "
        "and the humor landed flat almost every time. I'd say a 4 out of 10. "
        "Save your money and skip this one."
    ),
    (
        "The film was okay. Some moments were beautiful, others dragged. "
        "I'd give it a 6 — worth watching if you have time, but not urgent. "
        "The acting was decent, the cinematography was nice, but the story "
        "felt predictable."
    ),
]


def pretty_print(review_data: MovieReview, index: int):
    """Display the extracted review data in a readable format."""

    print(f"\n{'=' * 60}")
    print(f"📽️  REVIEW {index + 1} — EXTRACTED DATA")
    print(f"{'=' * 60}")
    print(f"Title:           {review_data.title}")
    print(f"Rating:          {review_data.rating} / 10")
    print(f"Sentiment:       {review_data.sentiment}")
    print(f"Recommendation:  {review_data.recommendation}")
    print(f"\nKey Points:")
    for point in review_data.key_points:
        print(f"  • {point}")
    print()


def run_with_explicit_parser():
    """Run the demo using the explicit PydanticOutputParser approach."""

    print("\n" + "=" * 60)
    print("🔧 APPROACH 1: PydanticOutputParser (Explicit)")
    print("=" * 60)

    chain = build_explicit_chain()

    for i, review in enumerate(SAMPLE_REVIEWS):
        try:
            result = chain.invoke({"review": review})
            pretty_print(result, i)
        except Exception as error:
            print(f"\n❌ Failed to extract review {i + 1}: {error}")


def run_with_modern_method():
    """Run the demo using the modern with_structured_output() method."""

    print("\n" + "=" * 60)
    print("⚡ APPROACH 2: with_structured_output() (Modern)")
    print("=" * 60)

    structured_llm = build_modern_chain()

    for i, review in enumerate(SAMPLE_REVIEWS):
        try:
            result = structured_llm.invoke(review)
            pretty_print(result, i)
        except Exception as error:
            print(f"\n❌ Failed to extract review {i + 1}: {error}")


if __name__ == "__main__":

    print("=" * 60)
    print("🦜 LangChain Day 31 — Output Parsers & Structured Data")
    print("=" * 60)
    print("\nExtracting structured info from movie reviews...\n")

    run_with_explicit_parser()
    run_with_modern_method()

    print("=" * 60)
    print("✅ Day 31 demo complete!")
    print("=" * 60)
