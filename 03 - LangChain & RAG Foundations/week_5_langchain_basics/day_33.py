"""
Day 33 - Csutom Tools with Real-World Logic

Goal: Build tool with validation, error handling, and multi-step logic.
Each tool is defensive - it handles bad input gracefully instead of crashing.

This script demonstrates:
- Input validation in tools
- try/except error handling in tools
- Multi-step calculations
- Tool that combine multiple operations
- Defensive tool design

Author: Tejoz
"""
import os
import random
import string
import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# ============================================================
# CONFIGURATION
# ============================================================

MODEL: str = "nvidia/nemotron-3-ultra-550b-a55b:free"
TEMPERATURE =  0.2
TIMEOUT = 30

#============================================================
# ENVIRONMENT
#============================================================

from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("❌ OPENROUTER_API_KEY is not set.")
    print(f"Looking for .env at: {env_path}")
    print(f"File exists: {env_path.exists()}")
    sys.exit(1)


#===========================================================
#  CUSTOM TOOLS WITH VALIDATION AND ERROR HANDLING
#===========================================================

@tool
def analyze_text(text: str) -> str:
    """Analyse a text return word count, sentence count, and character count.
    Use this when user asks for teaxt statistics.
    Example: "Analyze the text: 'Hello world! How are you?
    """
    try:
        if not text or not teaxt.strip():
            return "Error: Teaxt cannot be empty."

        words = text.split()
        word_count = len(words)

        # Count sentances (spilt on . ! ?)
        sentence_count = 0
        for char in text:
            if char in ".!?":
                sentence_count += 1

        if sentence_count == 0:
            sentence_count = 1  # At least one sentence if there's text

        char_count = len(text)
        char_count_no_spaces = len(text.replace(" ", ""))

        avg_word_length = (
            sum(len(word) for word in words) / word_count
            if word_count > 0
            else 0
        )

        return (
            f"Text Analysis:\n"
            f"  Words: {word_count}\n"
            f"  Sentences: {sentence_count}\n"
            f"  Characters (with spaces): {char_count}\n"
            f"  Characters (no spaces): {char_count_no_spaces}\n"
            f"  Average word length: {avg_word_length:.1f} chars"
        )
    except Exception as error:
        return f"Error analyzing text: {error}"

@tool
def convert_temperature(value: float, from_unit: str, to_unit: str) -> str:
    """Convert temperature between Celsius, Fahrenheit, and Kelvin.

    Use this when the user asks to convert temperatures.
    from_unit and to_unit must be 'C', 'F', or 'K'.
    Example: convert_temperature(100, 'C', 'F') → 212°F
    """
    try:
        from_unit = from_unit.upper().strip()
        to_unit = to_unit.upper().strip()

        valid_units = ["C", "F", "K"]

        if from_unit not in valid_units:
            return f"Error: from_unit must be one of {valid_units}, got '{from_unit}'."

        if to_unit not in valid_units:
            return f"Error: to_unit must be one of {valid_units}, got '{to_unit}'."

        # Convert to Celsius first
        if from_unit == "C":
            celsius = value
        elif from_unit == "F":
            celsius = (value - 32) * 5 / 9
        elif from_unit == "K":
            celsius = value - 273.15

        # Absolute zero check (in Celsius)
        if celsius < -273.15:
            return f"Error: Temperature below absolute zero ({celsius:.1f}°C is impossible)."

        # Convert from Celsius to target
        if to_unit == "C":
            result = celsius
        elif to_unit == "F":
            result = (celsius * 9 / 5) + 32
        elif to_unit == "K":
            result = celsius + 273.15

        return f"{value}°{from_unit} = {result:.2f}°{to_unit}"

    except Exception as error:
        return f"Error converting temperature: {error}"


@tool
def calculate_bmi(height_cm: float, weight_kg: float) -> str:
    """Calculate BMI from height (cm) and weight (kg), and return the category.

    Use this when the user asks to calculate BMI.
    Example: calculate_bmi(175, 70) → BMI: 22.9 (normal weight)
    """
    try:
        if height_cm <= 0:
            return f"Error: Height must be positive, got {height_cm} cm."

        if weight_kg <= 0:
            return f"Error: Weight must be positive, got {weight_kg} kg."

        if height_cm > 300:
            return f"Error: Height {height_cm} cm is unrealistically tall."

        if weight_kg > 500:
            return f"Error: Weight {weight_kg} kg is unrealistically high."

        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)

        if bmi < 18.5:
            category = "underweight"
        elif bmi < 25:
            category = "normal weight"
        elif bmi < 30:
            category = "overweight"
        else:
            category = "obese"

        return f"BMI: {bmi:.1f} ({category})"

    except Exception as error:
        return f"Error calculating BMI: {error}"

tool
def generate_password(length: int, use_symbols: bool = True) -> str:
    """Generate a random password of the specified length.

    Use this when the user asks to generate a password.
    Length must be between 8 and 64.
    If use_symbols is True, includes special characters like !@#$%.
    Example: generate_password(16, True)
    """
    try:
        if length < 8:
            return f"Error: Password length must be at least 8, got {length}."

        if length > 64:
            return f"Error: Password length must be at most 64, got {length}."

        # Build character pool
        chars = string.ascii_letters + string.digits
        if use_symbols:
            chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"

        # Ensure at least one of each type for strength
        password_chars = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase),
            random.choice(string.digits),
        ]
        if use_symbols:
            password_chars.append(random.choice("!@#$%^&*"))

        # Fill the rest
        for _ in range(length - len(password_chars)):
            password_chars.append(random.choice(chars))

        # Shuffle so guaranteed chars aren't always at the start
        random.shuffle(password_chars)

        password = "".join(password_chars)

        return f"Generated password ({length} chars): {password}"

    except Exception as error:
        return f"Error generating password: {error}"


# Collect all tools
tools = [
    analyze_text,
    convert_temperature,
    calculate_bmi,
    generate_password,
]


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
# SYSTEM MESSAGE
# ============================================================

system_message = (
    "You are a helpful AI assistant with access to specialized tools for "
    "text analysis, temperature conversion, BMI calculation, and password generation. "
    "Use the appropriate tool when needed to answer questions accurately. "
    "If a tool returns an error, explain it clearly to the user."
)

# ============================================================
# AGENT SETUP (Modern LangChain v1+ API)
# ============================================================

agent_executor = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_message,
)

# ============================================================
# DEMO
# ============================================================

SAMPLE_QUERIES = [
    "Analyze this text: 'LangChain is amazing. It makes building AI apps so much easier. I love it!'",
    "Convert 100 degrees Celsius to Fahrenheit.",
    "What is the BMI of someone who is 175 cm tall and weighs 70 kg?",
    "Generate a 16-character password with symbols.",
    "What is the BMI of someone with height -100 cm?",  # Should error gracefully
    "Generate a 4-character password.",  # Should error gracefully
]


def run_query(query: str) -> None:
    """Run a single query through the agent."""

    print("\n" + "=" * 60)
    print(f"❓ QUERY: {query}")
    print("=" * 60)

    try:
        result = agent_executor.invoke(
            {"messages": [{"role": "user", "content": query}]}
        )

        final_message = result["messages"][-1]
        final_answer = (
            final_message.content
            if hasattr(final_message, "content")
            else str(final_message)
        )

        print(f"\n✅ ANSWER:\n{final_answer}\n")

    except Exception as error:
        print(f"\n❌ Error: {type(error).__name__}: {error}\n")


if __name__ == "__main__":

    print("=" * 60)
    print("🦜 LangChain Day 33 — Custom Tools & Error Handling")
    print("=" * 60)
    print("\nRunning sample queries through the agent...\n")

    for query in SAMPLE_QUERIES:
        run_query(query)

    print("\n" + "=" * 60)
    print("✅ Day 33 demo complete!")
    print("=" * 60)
    