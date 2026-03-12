# main.py
from graph import graph
from state import GraphState

def main():
    """
    Command-line interface for users who prefer terminal.
    """
    print("📰 Local Agentic Newsroom (CLI Mode)")
    print("=" * 50)
    
    topic = input("Enter blog topic: ")
    
    if not topic:
        print("❌ No topic provided. Exiting.")
        return
    
    # Initialize state
    initial_state = {
        "topic": topic,
        "research_notes": [],
        "draft": "",
        "critique": "",
        "revision_count": 0,
        "human_feedback": "",
        "approval_status": "pending",
        "image_prompt": "",
        "image_path": "",
        "messages": []
    }
    
    config = {"configurable": {"thread_id": "cli_session"}}
    
    print("\n🚀 Starting generation...\n")
    
    # Run graph (invoke = run all at once, no streaming)
    final_state = graph.invoke(initial_state, config)
    
    # Display results
    print("\n" + "=" * 50)
    print("✅ GENERATION COMPLETE")
    print("=" * 50)
    print(f"\n📄 Draft saved to: output/")
    print(f"🖼️ Image: {final_state.get('image_path', 'Not generated')}")
    print(f"\n📋 Process Log:")
    for msg in final_state.get("messages", []):
        print(f"  {msg}")

if __name__ == "__main__":
    main()