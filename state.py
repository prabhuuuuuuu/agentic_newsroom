# state.py
from typing import TypedDict, List, Annotated
import operator

# 1. Define how lists should be updated in the state
# By default, LangGraph overwrites state. 
# We want to APPEND to lists (like notes or messages), not replace them.
def add_to_list(existing: List, new: List):
    return existing + new

# 2. Define the GraphState schema
class GraphState(TypedDict):
    """
    This class defines the structure of data that flows through our agent graph.
    Think of it as a shared whiteboard that every agent (node) can read and write to.
    """
    
    # --- Core Fields (from info.md spec) ---
    topic: str                      # The user's input topic
    research_notes: Annotated[List[str], add_to_list]  # Accumulated search results
    draft: str                      # The current blog post draft
    critique: str                   # Feedback from the Critic agent
    revision_count: int             # Tracks how many times we've revised (max 3)
    
    # --- Expanded Fields (Human-in-the-Loop) ---
    human_feedback: str             # Stores input from the Streamlit UI
    approval_status: str            # "pending", "approved", or "needs_revision"
    
    # --- Expanded Fields (Multi-Modal) ---
    image_prompt: str               # Prompt sent to Stability AI
    image_path: str                 # Local path where image is saved
    
    # --- Expanded Fields (UI/Debugging) ---
    messages: Annotated[List[str], add_to_list]  # Log of events for the UI