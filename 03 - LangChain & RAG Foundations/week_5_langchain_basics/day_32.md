# 📅 Day 32 — LangChain Agents & Tools

**Date:** Day 32 of 90
**Module:** 3 — LangChain & RAG Foundations
**Week:** 5 — LangChain Basics
**Goal:** Build a LangChain agent that uses tools (calculator, word counter, datetime) to answer user questions intelligently.

---

## 🎯 What I Learned Today

### From Chains to Agents

So far, I've built **chains** — fixed sequences of operations:

```text
prompt → LLM → output parser
� Day 32 — LangChain Agents & Tools
Date: Day 32 of 90 Module: 3 — LangChain & RAG Foundations Week: 5 — LangChain Basics Goal: Build a LangChain agent that uses tools (calculator, word counter, datetime) to answer user questions intelligently.

🎯 What I Learned Today
From Chains to Agents
So far, I've built chains — fixed sequences of operations:

prompt → LLM → output parser
The flow is predictable and linear.

Today I learned agents — dynamic, decision-making systems:

User input → Agent decides:
              ├─ Which tool to use?
              ├─ Calls the tool
              ├─ Observes the result
              ├─ Maybe calls another tool?
              └─ Returns final answer
The flow is dynamic and the agent chooses its own path.

The ReAct Pattern
ReAct = Reasoning + Acting. The agent thinks step by step and uses tools when needed.

A typical ReAct loop looks like this:

Thought: I need to calculate 15% of 240.
Action: calculate_percentage(percent=15, number=240)
Observation: 15% of 240 is 36.0
Thought: I have the answer.
Final Answer: 15% of 240 is 36.0
The agent alternates between thinking and acting until it reaches a final answer.

The @tool Decorator
LangChain provides a simple way to turn any Python function into a tool that the agent can use:

from langchain_core.tools import tool

@tool
def my_function(arg1: float, arg2: float) -> str:
    """Description of what the tool does."""
    # ... function logic ...
    return result
The decorator:

Wraps the function with metadata
Uses the docstring to describe what the tool does (the LLM reads this!)
Uses type hints to describe arguments
Makes the tool available to the agent
Important: The docstring is critical. The agent uses it to decide when to use the tool. Always write clear, specific docstrings.

Agent Executor
The AgentExecutor runs the agent in a loop:

Calls the agent to decide the next action
Executes the chosen tool
Feeds the result back to the agent
Repeats until the agent gives a final answer
Returns the final answer to the user
Modern Agent Creation (LangChain v1+)
In modern LangChain, the recommended way to create an agent is create_tool_calling_agent, which uses the model's native tool calling capability instead of text-based ReAct:

from langchain.agents import create_tool_calling_agent, AgentExecutor

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,         # Show reasoning
    handle_parsing_errors=True
)
result = executor.invoke({"input": "What's 15% of 240?"})
This is cleaner and more reliable than the older text-based approach.

Why verbose=True Matters
Setting verbose=True in the AgentExecutor prints the agent's internal reasoning to the console:

> Entering new AgentExecutor chain...
Invoking: calculate_percentage with {'percent': 15, 'number': 240}
15% of 240 is 36.0
> Finished chain.
This is invaluable for:

Debugging — see why the agent picked a particular tool
Learning — understand the decision-making process
Trust — verify the agent is doing the right thing
In production, you might turn this off, but for development it's essential.

💻 What I Built
✅ A calculator tool with percentage and square root operations ✅ A word counter tool for text analysis ✅ A date/time tool for current time queries ✅ An add numbers tool for simple addition ✅ An agent that intelligently picks the right tool for each query ✅ Tested with 5 different sample queries ✅ Used verbose=True to see the agent's reasoning

� Key Concepts to Remember
Concept	Description
Agent	LLM that decides what to do dynamically
Tool	Python function wrapped with @tool decorator
ReAct	Reasoning + Acting pattern
AgentExecutor	Runs the agent in a loop until done
create_tool_calling_agent	Modern way to create an agent
@tool decorator	Turns a function into an agent-usable tool
verbose=True	Shows the agent's reasoning (for debugging)
handle_parsing_errors	Gracefully handles LLM output errors
Docstring	Critical — describes when the agent should use the tool
🔍 How the Agent Decides
The agent uses the docstring of each tool to decide:

@tool
def calculate_percentage(percent: float, number: float) -> str:
    """Calculate a percentage of a number.

    Use this when the user asks what X% of Y is.
    Example: 'What's 15% of 240?' → use calculate_percentage(15, 240)
    """
When the user asks "What's 15% of 240?", the agent reads the docstring, matches the example, and picks the right tool.

This is why clear docstrings matter!

� Sample Queries I Tested
Query	Tool Picked	Result
"What is 15% of 240?"	calculate_percentage	15% of 240 is 36.0
"What's the square root of 144?"	calculate_square_root	The square root of 144 is 12.0
"How many words are in this sentence: ...?"	count_words	The text contains N words.
"What is the current date and time?"	get_current_datetime	2026-XX-XX HH:MM:SS
"What is 87 plus 156?"	add_numbers	87 + 156 = 243
Each query made the agent pick a different tool. This proves the agent is reasoning about which tool fits, not just guessing.

🔜 Tomorrow (Day 33)
I'll learn about:

Custom tools with complex logic — tools that interact with APIs or do real work
Tool error handling — what happens when a tool fails
Tool descriptions and prompt engineering — how to write better docstrings
🆘 Issues I Encountered
ImportError: cannot import name 'create_tool_calling_agent'
If you see this error, your LangChain version is too old:

python -m pip install --upgrade langchain langchain-core
Model doesn't support tool calling
Some models don't support tool calling natively. Try:

nvidia/nemotron-3-ultra-550b-a55b:free
meta-llama/llama-3.1-8b-instruct:free
📚 Resources
YouTube: "LangChain agents tutorial for beginners"
YouTube: "LangChain @tool decorator explained"
YouTube: "LangChain create_tool_calling_agent tutorial"
LangChain docs: https://python.langchain.com/docs/concepts/agents
LangChain agents how-to: https://python.langchain.com/docs/how_to/#agents
⭐ Why This Matters
Agents are the foundation of modern AI applications. When you build a chatbot that searches the web, queries a database, sends emails, or controls other software, you're using the agent pattern.

The skills I learned today will apply directly to:

Project 2 (RAG-based knowledge chatbot — uses tools for retrieval)
Real-world AI apps at work (almost all use agents)
This is one of the most transferable skills in AI engineering.