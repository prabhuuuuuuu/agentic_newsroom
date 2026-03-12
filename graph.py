# graph.py
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from state import GraphState
from agents import (
    researcher_node, 
    writer_node, 
    critic_node, 
    image_generator_node, 
    publisher_node
)

def create_graph():
    """
    Builds the entire agent workflow.
    This is the orchestration engine that connects all nodes.
    """
    
    # Initialize graph with state schema AND checkpointing
    # MemorySaver enables human-in-the-loop (pause/resume)
    memory = MemorySaver()
    workflow = StateGraph(GraphState, checkpointer=memory)
    
    # ============ ADD NODES ============
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("critic", critic_node)
    workflow.add_node("image_generator", image_generator_node)
    workflow.add_node("publisher", publisher_node)
    
    # ============ DEFINE EDGES ============
    
    # Entry point - always starts with research
    workflow.set_entry_point("researcher")
    
    # Linear flow: Research → Writer → Image → Critic
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", "image_generator")
    workflow.add_edge("image_generator", "critic")
    
    # ============ CONDITIONAL EDGE (The Loop) ============
    def should_revision(state):
        """
        Decides: Revise or Publish?
        Returns next node name based on state.
        """
        approval = state.get("approval_status", "pending")
        revision_count = state.get("revision_count", 0)
        human_feedback = state.get("human_feedback", "")
        
        # Human feedback takes priority
        if human_feedback:
            if "reject" in human_feedback.lower() or "revise" in human_feedback.lower():
                if revision_count < 3:
                    return "writer"  # Go back for revision
                else:
                    return "publisher"  # Max revisions reached
        
        # Critic approval
        if approval == "approved":
            return "publisher"
        elif approval == "needs_revision" and revision_count < 3:
            return "writer"
        else:
            return "publisher"
    
    # Add conditional edge from Critic
    workflow.add_conditional_edges(
        "critic",
        should_revision,
        {"writer": "writer", "publisher": "publisher"}
    )
    
    # Publisher ends the graph
    workflow.add_edge("publisher", END)
    
    # Compile with checkpointing enabled
    # interrupt_before=["publisher"] pauses the graph BEFORE publishing
    # so we can show the draft to the human and ask for approval first.
    app = workflow.compile(checkpointer=memory, interrupt_before=["publisher"])
    
    return app

# Create graph instance
graph = create_graph()