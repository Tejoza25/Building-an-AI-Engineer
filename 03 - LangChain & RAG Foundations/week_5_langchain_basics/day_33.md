# 📅 Day 33 — Custom Tools with Real-World Logic

**Date:** Day 33 of 90
**Module:** 3 — LangChain & RAG Foundations
**Week:** 5 — LangChain Basics
**Goal:** Build custom tools that handle complex logic, validation, and errors gracefully.

---

## 🎯 What I Learned Today

### Beyond Simple Tools

Yesterday's tools (Day 32) were simple: percentage, square root, word count. Today I built tools that:

- **Validate inputs** (reject negative numbers, invalid formats)
- **Handle errors gracefully** (return helpful error messages instead of crashing)
- **Perform multiple operations** (combine several calculations)
- **Return structured data** (formatted strings with multiple values)

### The Pattern: Defensive Tool Design

A good tool should:

1. **Validate inputs** — check that arguments make sense
2. **Handle errors** — use try/except for any operation that could fail
3. **Return clear messages** — both success and failure
4. **Be documented** — docstring explains when to use it

### My Day 33 Tools

#### 1. Text Analyzer
- Counts words, sentences, and characters
- Calculates average word length
- Returns structured summary

#### 2. Temperature Converter
- Converts between Celsius, Fahrenheit, Kelvin
- Validates physical limits (below absolute zero)
- Handles all three unit pairs

#### 3. BMI Calculator
- Takes height (cm) and weight (kg)
- Calculates BMI
- Returns category (underweight, normal, overweight, obese)
- Validates positive inputs

#### 4. Password Generator
- Takes desired length
- Optionally includes symbols, numbers, mixed case
- Returns a strong random password

### Why Error Handling Matters

Without error handling, a tool that fails will crash the entire agent. With error handling, the tool returns a helpful message and the agent can try a different approach.

Example:

```python
@tool
def calculate_bmi(height_cm: float, weight_kg: float) -> str:
    """Calculate BMI and return the category."""
    if height_cm <= 0 or weight_kg <= 0:
        return "Error: Height and weight must be positive numbers."
    
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
