
# 📰 Local Agentic Newsroom

A multi-agent AI system that autonomously researches, writes, and critiques technical blog posts using **local LLMs** (Llama 3.2) and **LangGraph** for orchestration.

## ✨ Features

- 🤖 **5 Autonomous Agents**: Researcher, Writer, Critic, Image Generator, Publisher
- 🔄 **Human-in-the-Loop**: Review and approve drafts before publishing
- 🖼️ **Multi-Modal Output**: Generate featured images or use your own local images
- 💰 **Free & Local**: Runs entirely on your machine with Ollama (Llama 3.2)
- 📊 **Real-Time Dashboard**: Streamlit UI with live progress tracking
- 🛡️ **Safety Controls**: Max 3 revision iterations to prevent infinite loops

## 🛠 Tech Stack

- **Orchestration**: LangGraph
- **LLM**: Ollama (Llama 3.2)
- **Framework**: LangChain
- **Search**: Tavily API
- **Image Generation**: Stability AI SD 3.5 (optional)
- **UI**: Streamlit
- **Language**: Python 3.10+

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/prabhuuuuuuu/agentic_newsroom.git
cd agentic_newsroom

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Pull Llama 3.2 model
ollama pull llama3.2
```

## ⚙️ Configuration

1. **Create `.env` file**:
```bash
TAVILY_API_KEY=your_tavily_api_key_here
STABILITY_API_KEY=your_stability_api_key_here  # Optional for AI-generated images
```

2. **Get API Keys**:
   - Tavily: https://tavily.com (free tier: 1000 searches/month)
   - Stability AI: https://platform.stability.ai (optional)

## 🚀 Usage

### Option 1: Streamlit Dashboard (Recommended)

```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

**Features**:
- Enter blog topic
- Set max revisions (1-5)
- Real-time progress tracking
- Human approval workflow
- **Upload custom featured image** from your local directory

### Option 2: CLI Mode

```bash
python main.py
```

## 📁 Project Structure

```
local-ai-newsroom/
├── .env                    # API keys
├── requirements.txt        # Dependencies
├── state.py               # GraphState definition
├── tools.py               # Search, image, and file tools
├── agents.py              # Agent node functions
├── graph.py               # LangGraph orchestration
├── app.py                 # Streamlit dashboard
├── main.py                # CLI entry point
└── output/                # Generated posts and images
    ├── post.md
    └── image_*.png
```

## ️ Using Custom Images

The system supports **two modes** for featured images:

### Mode 1: AI-Generated (Automatic)
- Set `STABILITY_API_KEY` in `.env`
- System auto-generates images based on topic

### Mode 2: Local Image Upload (Manual)
1. Place your image in `output/` folder
2. In Streamlit UI, use the **"Upload Custom Image"** feature
3. Select your image file (PNG, JPG supported)
4. The system will use your image instead of generating one

**Supported formats**: `.png`, `.jpg`, `.jpeg`  
**Recommended size**: 1200x630 pixels (blog header ratio)

## 🔄 How It Works
<img width="800" height="3485" alt="mermaid-1773339915101" src="https://github.com/user-attachments/assets/2217e993-98a6-4c01-b26a-e74b236e2748" />


## 🎯 Agents

1. **Researcher**: Searches web for 3-5 high-quality sources using Tavily
2. **Writer**: Creates technical blog post in GitHub Flavored Markdown
3. **Critic**: Evaluates draft for factual depth and formatting
4. **Image Generator**: Creates featured image (optional)
5. **Publisher**: Saves final post to `output/post.md`


## 📄 License

MIT License

---

**Built with** ❤️ **using LangGraph + Ollama + Streamlit**
