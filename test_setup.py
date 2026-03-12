# test_state.py
from state import GraphState

# Try to create a valid state
valid_state: GraphState = {
    "topic": "Test",
    "research_notes": ["note1"],
    "draft": "",
    "critique": "",
    "revision_count": 0,
    "human_feedback": "",
    "approval_status": "pending",
    "image_prompt": "",
    "image_path": "",
    "messages": ["start"]
}

print("✅ State structure is valid!")
print(f"Topic: {valid_state['topic']}")