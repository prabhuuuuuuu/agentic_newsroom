import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tools

load_dotenv()
tavily_api_key = os.getenv("TAVILY_API_KEY")

search_tool = TavilySearchResults(
    max_results = 5,
    api_key=tavily_api_key
)

@tool
def save_file(content: str, filename: str = output/post.md) -> str:
    try:
        os.makedirs("output", exist_ok = True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        return f"File saved successfully as {filename}"
    
    except Exception as e:
        return f"An error occurred while saving the file: {str(e)}"
    
tools = [search_tool, save_file]