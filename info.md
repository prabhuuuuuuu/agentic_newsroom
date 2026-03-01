# Project Spec: Local-Agentic Newsroom (LangGraph + Ollama)

## 🎯 Overview

A multi-agent system designed to research, write, and critique technical blog posts autonomously. The system uses **LangGraph** for orchestration and **Ollama** to run local LLMs (e.g., Llama 3) to ensure the project is entirely free to operate (excluding the optional Tavily search API).

I want you to teach code to me at every point, like why did you write a particular block and how it works every time. I want to learn how to code and not just get dependant on AI to write the code for myself. I want to be able to build such projects on my own.

## 🛠 Tech Stack

* **Orchestration:** LangGraph
* **LLM Provider:** Ollama (Local Llama 3 or Mistral)
* **Framework:** LangChain (Community & Core)
* **Search Tool:** Tavily API (Free Tier)
* **Language:** Python 3.10+

---

## 🏗 Repository Structure

```text
local-ai-newsroom/
├── .env                # TAVILY_API_KEY=your_key_here
├── requirements.txt    # langchain-ollama, langgraph, tavily-python, python-dotenv
├── state.py            # TypedDict defining the GraphState
├── tools.py            # Tavily Search tool & File Saver tool
├── agents.py           # Node functions (Researcher, Writer, Critic)
├── graph.py            # StateGraph definition, nodes, and edges
└── main.py             # Entry point (Invoke graph with a topic)
```

---

## 🧠 Logic Flow & Graph State

### 1. The State (`state.py`)

The `GraphState` must track the following:

* `topic`: The user's original query.
* `research_notes`: Aggregated search results.
* `draft`: The current version of the blog post.
* `critique`: Feedback from the Critic agent.
* `revision_count`: Integer to prevent infinite loops (max 3 revisions).

### 2. The Nodes (`agents.py`)

* **Researcher:** Calls Tavily to get 3-5 high-quality sources.
* **Writer:** Generates a Markdown post based on `research_notes`.
* **Critic:** Evaluates the `draft`. If it lacks detail or formatting, it provides `critique`.
* **Publisher:** Saves the final approved `draft` to a `output/post.md` file.

### 3. The Edges (`graph.py`)

* **START** ⮕ **Researcher** ⮕ **Writer** ⮕ **Critic**
* **Conditional Edge (The Loop):**
  - If **Critic** provides feedback AND `revision_count` < 3 ⮕ **Writer** (for revision).
  - Else ⮕ **Publisher** ⮕ **END**.

---

## 🚦 Implementation Instructions for Coding Agent

1. **Initialize Ollama:** Use `ChatOllama(model="llama3", temperature=0)` for all agents.
2. **Tool Binding:** Ensure the **Researcher** node has access to the `TavilySearchResults` tool.
3. **Prompt Engineering:**
   - The **Writer** must produce output in GitHub Flavored Markdown.
   - The **Critic** must be harsh and look for factual depth.
4. **Safety:** Ensure the graph terminates if the loop exceeds 3 iterations to save local compute resources.

---

### How to use this with your coding agent:

Simply upload or paste this `.md` file and say:

> *"Follow this PROJECT_SPEC.md to scaffold the directory and write the logic for each file, starting with state.py and tools.py."*