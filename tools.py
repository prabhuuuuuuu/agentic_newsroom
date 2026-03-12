# tools.py
import os
import requests
from datetime import datetime
from tavily import TavilyClient
from dotenv import load_dotenv
from PIL import Image, ImageDraw

# Load environment variables from .env file
load_dotenv()

# Initialize Tavily client for web search
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_tool(query: str) -> list:
    """
    RESEARCH TOOL
    Calls Tavily API to find 3-5 relevant sources.
    Returns list of formatted search results.
    """
    try:
        # Search with max 5 results for quality over quantity
        result = tavily.search(query, max_results=5)
        
        # Tavily returns a dict: {"results": [...], "query": "..."}
        # We need to access the 'results' key to get the actual list
        results_list = result.get("results", [])
        
        # Format each result for the LLM to read
        return [
            f"Source: {r['title']}\nURL: {r['url']}\nContent: {r['content']}" 
            for r in results_list
        ]
    except Exception as e:
        # Never crash - return error message as search result
        return [f"Search error: {str(e)}"]

def _make_placeholder_image(prompt: str) -> str:
    """
    Fallback: generates a styled gradient placeholder image using PIL.
    Used when Stability AI is unavailable or returns an error.
    """
    import textwrap
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"output/image_{timestamp}.png"

    width, height = 1024, 512
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    # Draw a dark gradient background
    for y in range(height):
        ratio = y / height
        r = int(15 + ratio * 20)
        g = int(20 + ratio * 30)
        b = int(40 + ratio * 60)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Draw decorative circles
    for cx, cy, rad, col in [
        (100, 80, 120, (30, 60, 120, 80)),
        (900, 400, 160, (20, 80, 100, 60)),
        (512, 256, 200, (40, 40, 80, 40)),
    ]:
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        ov_draw = ImageDraw.Draw(overlay)
        ov_draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=col)
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        draw = ImageDraw.Draw(img)

    # Draw wrapped topic text
    short_prompt = prompt[:80] if len(prompt) > 80 else prompt
    lines = textwrap.wrap(short_prompt, width=40)
    y_text = height // 2 - len(lines) * 18
    for line in lines:
        text_width = draw.textlength(line) if hasattr(draw, "textlength") else len(line) * 10
        draw.text(((width - text_width) / 2, y_text), line, fill=(200, 220, 255))
        y_text += 32

    img.save(image_path, "PNG")
    return image_path


def generate_image_tool(prompt: str) -> str:
    """
    IMAGE GENERATION TOOL
    Calls Stability AI API to create featured image.
    Falls back to a PIL-generated placeholder on any error.
    Returns local file path of saved image.
    """
    try:
        api_key = os.getenv("STABILITY_API_KEY")
        if not api_key:
            raise ValueError("STABILITY_API_KEY not set")

        url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

        # Stability AI v2beta requires multipart/form-data via files=
        # Using data= sends application/x-www-form-urlencoded which causes 400
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "image/*"
            },
            files={
                "prompt": (None, prompt),
                "mode":   (None, "text-to-image"),
                "output_format": (None, "png"),
            },
            timeout=60
        )
        response.raise_for_status()

        os.makedirs("output", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = f"output/image_{timestamp}.png"
        with open(image_path, "wb") as f:
            f.write(response.content)
        return image_path


    except Exception:
        # Stability AI failed — silently fall back to PIL placeholder
        return _make_placeholder_image(prompt)

def save_file_tool(content: str, filename: str) -> str:
    """
    FILE SAVE TOOL
    Saves final blog post to output folder.
    Returns confirmation message with file path.
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)
        
        # Build full file path
        filepath = f"output/{filename}"
        
        # Write content to file with UTF-8 encoding
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        return f"File saved at: {filepath}"
        
    except Exception as e:
        return f"Save error: {str(e)}"