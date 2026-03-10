# tools.py
import os
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain_core.tools import tool

load_dotenv()
tavily_api_key = os.getenv("TAVILY_API_KEY")

# 1. Tavily Search Tool
search_tool = TavilySearch(
    max_results=5,
    api_key=tavily_api_key
)

# 2. File Saver Tool (Custom)
@tool
def save_file(content: str, filename: str = "output/post.md") -> str:  # ✅ Added quotes
    """Save content to a markdown file"""
    try:
        os.makedirs("output", exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File saved successfully as {filename}"
    except Exception as e:
        return f"An error occurred while saving the file: {str(e)}"

# 3. Export tools list (optional, for reference)
tools = [search_tool, save_file]