"""
Project 1 - AI Research Agent

Day 26
Documentation, Demo, File Output and Error Handling

Author: Tejoz

Pipeline:
    Research Topic
        ↓
    DuckDuckGo Search
        ↓
    Web Scraping
        ↓
    LLM Source Summaries
        ↓
    Final LLM Synthesis
        ↓
    Markdown Research Report
"""

import os
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# CONFIGURATION
# ============================================================

MAX_RESULTS = 3
REQUEST_TIMEOUT = 10
MAX_SOURCE_CHARS = 10000
MAX_FINAL_CONTEXT_CHARS = 12000

MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("❌ OPENROUTER_API_KEY is not set.")
    print("Please create a .env file and add your OpenRouter API key.")
    raise SystemExit(1)


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)


# ============================================================
# WEB SEARCH
# ============================================================

def search_web(topic):
    """Search DuckDuckGo and return up to three results."""

    print("\n🔍 Searching the web...\n")

    results = []

    try:
        with DDGS() as ddgs:

            search_results = ddgs.text(
                topic,
                max_results=MAX_RESULTS
            )

            for result in search_results:

                title = result.get("title")
                url = result.get("href")

                if title and url:

                    results.append(
                        {
                            "title": title,
                            "url": url
                        }
                    )

    except Exception as error:

        print("\n❌ Web search failed.")
        print(f"Error type: {type(error).__name__}")
        print(f"Error details: {error}")

    return results


# ============================================================
# WEB SCRAPING
# ============================================================

def scrape_page(url):
    """Download a webpage and extract readable text."""

    try:

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/131.0 Safari/537.36"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for element in soup(
            ["script", "style", "nav", "footer", "header"]
        ):
            element.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        return text

    except requests.Timeout:

        print(f"⏱️ Request timed out: {url}")
        return ""

    except requests.RequestException as error:

        print(f"❌ Network error while reading:")
        print(url)
        print(error)

        return ""

    except Exception as error:

        print("❌ Unexpected scraping error.")
        print(error)

        return ""


# ============================================================
# LLM SOURCE SUMMARIZATION
# ============================================================

def summarize_text(text, source_title):
    """Generate a concise three-bullet summary."""

    if not text.strip():

        return "Summary unavailable because no readable source text was found."

    text = text[:MAX_SOURCE_CHARS]

    prompt = f"""
You are a careful research assistant.

Summarize the following web source.

Return exactly three concise bullet points.

Focus on:
- Important factual information
- Important findings
- Main takeaway

Rules:
- Use only information provided in the source.
- Do not invent facts.
- Do not make unsupported claims.
- Keep each bullet concise.

Source title:
{source_title}

Source text:
{text}
"""

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful research assistant. "
                        "Summarize only the provided source."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            timeout=30
        )

        content = response.choices[0].message.content

        if not content:

            return "Summary unavailable."

        return content.strip()

    except Exception as error:

        print("\n❌ Source summarization failed.")
        print(f"Error type: {type(error).__name__}")
        print(f"Error details: {error}")

        return "Summary unavailable because the LLM request failed."


# ============================================================
# FINAL REPORT GENERATION
# ============================================================

def generate_final_report(topic, summaries):
    """Combine source summaries into a final research report."""

    if not summaries:

        return (
            "Final report unavailable because "
            "no source summaries were generated."
        )

    combined_summaries = "\n\n".join(summaries)

    combined_summaries = combined_summaries[
        :MAX_FINAL_CONTEXT_CHARS
    ]

    prompt = f"""
Create a concise research report about:

{topic}

Below are summaries from multiple web sources:

{combined_summaries}

Use exactly these sections:

## Overview

Provide a short overview.

## Key Findings

List the most important findings.

## Overall Takeaway

Give a concise conclusion.

Rules:
- Use only information present in the supplied summaries.
- Do not invent facts.
- Do not make unsupported claims.
- Keep the report professional and concise.
"""

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional research assistant. "
                        "Synthesize only the supplied source summaries."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            timeout=30
        )

        content = response.choices[0].message.content

        if not content:

            return "Final report unavailable."

        return content.strip()

    except Exception as error:

        print("\n❌ Final LLM request failed.")
        print(f"Error type: {type(error).__name__}")
        print(f"Error details: {error}")

        return "Final report unavailable because the LLM request failed."


# ============================================================
# SAFE FILE NAME
# ============================================================

def create_safe_filename(topic):
    """Convert a research topic into a safe filename."""

    filename = re.sub(
        r"[^a-zA-Z0-9]+",
        "_",
        topic
    ).strip("_")

    if not filename:

        filename = "research_report"

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    return f"{filename}_{timestamp}.md"


# ============================================================
# SAVE REPORT
# ============================================================

def save_report(topic, results, final_report):
    """Save the final research report as Markdown."""

    os.makedirs(
        "reports",
        exist_ok=True
    )

    filename = os.path.join(
        "reports",
        create_safe_filename(topic)
    )

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                f"# Research Report: {topic}\n\n"
            )

            file.write(
                f"**Generated:** "
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )

            file.write("---\n\n")

            file.write("## Sources\n\n")

            for index, result in enumerate(
                results,
                start=1
            ):

                file.write(
                    f"{index}. "
                    f"[{result['title']}]"
                    f"({result['url']})\n"
                )

            file.write("\n---\n\n")

            file.write(
                "## Final Research Report\n\n"
            )

            file.write(final_report)

            file.write("\n")

        return filename

    except OSError as error:

        print("\n❌ Could not save report.")
        print(f"Error details: {error}")

        return ""


# ============================================================
# COMPLETE RESEARCH WORKFLOW
# ============================================================

def research(topic):
    """Run the complete research pipeline."""

    results = search_web(topic)

    if not results:

        print("\n❌ No search results were found.")
        return

    print("📚 Sources found:\n")

    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            f"{index}. {result['title']}"
        )

        print(
            f"   {result['url']}\n"
        )

    summaries = []

    print("🧠 Reading and summarizing sources...\n")

    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            f"--- Source {index} ---"
        )

        print(
            f"Title: {result['title']}"
        )

        text = scrape_page(
            result["url"]
        )

        if not text:

            print(
                "⚠️ No readable text extracted."
            )

            print(
                "Skipping this source.\n"
            )

            continue

        print(
            "Generating source summary..."
        )

        summary = summarize_text(
            text,
            result["title"]
        )

        summaries.append(
            f"### Source {index}: "
            f"{result['title']}\n\n"
            f"{summary}"
        )

        print("\nSummary:")
        print(summary)
        print()

    if not summaries:

        print(
            "❌ No source summaries were successfully generated."
        )

        return

    print("=" * 60)

    print(
        "🧠 Generating final research report..."
    )

    print("=" * 60)

    final_report = generate_final_report(
        topic,
        summaries
    )

    print("\n" + "=" * 60)
    print("📑 FINAL RESEARCH REPORT")
    print("=" * 60)

    print(final_report)

    report_file = save_report(
        topic,
        results,
        final_report
    )

    if report_file:

        print("\n✅ Report saved successfully:")
        print(report_file)

    else:

        print(
            "\n⚠️ Report could not be saved."
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("=" * 60)

    print(
        "🤖 AI Research Agent"
    )

    print(
        "Day 26 - Documentation + Demo"
    )

    print("=" * 60)

    topic = input(
        "\nEnter a research topic: "
    ).strip()

    if not topic:

        print(
            "❌ Please enter a research topic."
        )

    else:

        research(topic)