# Day 19 – Multi-Tool AI Agent (Calculator + DuckDuckGo Search)

## 🎯 Objective

The objective of Day 19 was to build a **Multi-Tool AI Agent** capable of selecting and using the appropriate external tool based on the user's request.

Unlike previous projects that relied on a single tool, this agent demonstrates a simplified **ReAct (Reason → Act → Observe → Answer)** workflow by deciding whether to use a calculator or perform a web search before generating the final response.

---

# 📖 Project Overview

This project extends the capabilities of a Large Language Model (LLM) by integrating two external tools:

- 🧮 Calculator Tool
- 🌐 DuckDuckGo Web Search Tool

The agent first analyzes the user's question, determines which tool is required, executes the selected tool, observes the result, and finally asks the LLM to generate a natural language response using the tool output.

---

# 🏗️ System Architecture

```text
                    User
                      │
                      ▼
              User Question
                      │
                      ▼
          AI Agent (Reasoning Layer)
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
 Calculator Tool          DuckDuckGo Search
        │                           │
        └─────────────┬─────────────┘
                      ▼
             Observation (Tool Output)
                      │
                      ▼
          Large Language Model (LLM)
                      │
                      ▼
               Final AI Response
```

---

# 🔄 ReAct Workflow

```text
Reason
   │
   ▼
Select the appropriate tool
   │
   ▼
Execute the tool
   │
   ▼
Observe the result
   │
   ▼
Generate the final answer
```

---

# 🛠️ Tools Implemented

## 🧮 Calculator Tool

Handles mathematical expressions including:

- Basic arithmetic
- Percentage calculations

Example:

```text
23% of 1847
```

Output:

```text
424.81
```

---

## 🌐 DuckDuckGo Search Tool

Performs live web searches for:

- Current events
- Recent news
- Weather
- Prices
- General factual information

Example:

```text
Latest AI news
```

The search results are provided to the LLM before generating the final response.

---

# 🧠 Agent Decision Logic

The AI Agent automatically decides which tool to use based on the user's input.

Examples:

| User Question | Selected Tool |
|--------------|---------------|
| 45 + 18 | Calculator |
| 23% of 1847 | Calculator |
| Latest AI news | DuckDuckGo |
| Who is Sundar Pichai? | DuckDuckGo |
| Explain Machine Learning | LLM Only |

---

# 💻 Features

- Multi-tool AI Agent
- Calculator integration
- DuckDuckGo search integration
- ReAct reasoning workflow
- Intelligent tool selection
- Prompt engineering
- OpenRouter API integration
- Environment variable security using `.env`
- Modular Python code

---

# 🛠️ Technologies Used

- Python
- OpenRouter API
- OpenAI Python SDK
- DDGS (DuckDuckGo Search)
- Regular Expressions (Regex)
- Prompt Engineering
- Git
- GitHub
- VS Code

---

# 🌍 Real-World Applications

The architecture developed in this project can be extended to build:

- AI Research Assistants
- Customer Support Agents
- AI Financial Advisors
- Coding Assistants
- Travel Planning Agents
- Knowledge Retrieval Systems
- Enterprise AI Assistants

---

# 📚 Skills Developed

During this project I strengthened my understanding of:

- Multi-Tool AI Agents
- ReAct Pattern
- Tool Selection Logic
- External Tool Integration
- Prompt Engineering
- Python Functions
- Error Handling
- Software Architecture
- Git Version Control

---

# 💡 Reflection

Day 19 helped me understand how modern AI agents combine reasoning with external tools to solve problems more effectively.

Instead of expecting the language model to perform every task independently, the AI Agent determines which tool is most suitable, gathers the necessary information, and then produces a coherent response.

This project demonstrates the transition from a simple chatbot to an intelligent AI Agent capable of interacting with multiple external systems.

---

# 🚀 Future Improvements

Potential enhancements include:

- Native OpenAI/OpenRouter Tool Calling
- Weather API integration
- Currency Conversion Tool
- Wikipedia Search Tool
- Memory Support
- Multi-step Planning
- LangChain Integration
- LangGraph Agent Workflows

---

# ✅ Outcome

Successfully developed a **Multi-Tool AI Agent** capable of selecting between a Calculator Tool and a DuckDuckGo Search Tool. This project strengthened my understanding of AI Agent architectures, the ReAct workflow, tool integration, and prompt engineering while demonstrating practical AI engineering skills.