# Day 12 – Understanding Tokens, Context Limits & Cost Tracking

## 🎯 Objective

The objective of Day 12 was to understand how Large Language Models (LLMs) process text using tokens, how context windows affect conversations, and how to monitor token usage returned by the API.

---

# 📖 Overview

Large Language Models do not process text as complete words or sentences. Instead, they break text into smaller units called **tokens**.

API providers such as OpenAI and OpenRouter calculate usage and pricing based on the number of input and output tokens processed during each request.

Understanding token usage is essential for designing efficient, scalable, and cost-effective AI applications.

---

# 🧠 Key Concepts Learned

## 1. Tokens

A token is a small unit of text processed by an LLM.

Examples:

- A short word may be one token.
- A long word may be split into multiple tokens.
- Spaces and punctuation also contribute to tokenization.

Both the prompt sent to the model and the generated response consume tokens.

---

## 2. Context Window

The context window represents the maximum number of tokens that a model can process in a single request.

It includes:

- System Prompt
- User Prompt
- Conversation History
- AI Response

When the context limit is exceeded, older messages may need to be removed or summarized.

---

## 3. Token Usage

Every API response provides usage statistics such as:

- Prompt Tokens
- Completion Tokens
- Total Tokens

Monitoring these values helps developers optimize prompt length and reduce API costs.

---

## 4. Cost Awareness

Since most LLM providers charge based on token usage, efficient prompt design reduces operational costs while maintaining response quality.

---

# 💻 Practical Exercise

Built a chatbot that:

- Uses a System Prompt
- Accepts user questions
- Sends requests to the OpenRouter API
- Displays the AI response
- Tracks Prompt Tokens
- Tracks Completion Tokens
- Displays Total Tokens

---

# 🛠 Skills Developed

- Token Awareness
- Context Window Understanding
- API Usage Monitoring
- Cost Optimization Basics
- Prompt Engineering
- AI Chatbot Development

---

# 🌍 Real-World Applications

Understanding token usage is important for:

- AI Customer Support Systems
- AI Agents
- Chatbots
- RAG Applications
- Enterprise AI Solutions
- Production AI Monitoring

---

# 📚 Technologies Used

- Python
- OpenRouter API
- OpenAI Python SDK
- VS Code
- Git
- GitHub

---

# 💡 Reflection

Today I learned that building AI applications is not only about generating responses but also about understanding how LLMs consume tokens, manage context, and impact operational costs. Monitoring token usage is an essential practice for developing scalable and production-ready AI systems.

---

## ✅ Outcome

Successfully learned how Large Language Models process text using tokens, how context limits affect conversations, and how to monitor API token usage for better performance and cost optimization.