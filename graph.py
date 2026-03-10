# graph.py
from langgraph.graph import StateGraph, START, END
from state import GraphState
# ✅ Import critique_node (matches agents.py function name)
from agents import research_node, write_node, critique_node, publish_node

# Create the graph
workflow = StateGraph(GraphState)

# Adding nodes to the graph
workflow.add_node("researcher", research_node)
workflow.add_node("write", write_node)  # ✅ Node is named "write"
workflow.add_node("critic", critique_node)  # ✅ Uses critique_node function
workflow.add_node("publisher", publish_node)

# Defining entry point
workflow.add_edge(START, "researcher")

# Define linear flow
workflow.add_edge("researcher", "write")
workflow.add_edge("write", "critic")

# Define conditional edge (The Loop)
def should_continue(state: GraphState):
    print("--DECIDING NEXT STEP--")
    critique = state.get("critique", "")
    revision_count = state.get("revision_count", 0)
    max_revisions = state.get("max_revisions", 3)
    
    # Check if critic approved
    if 'APPROVED' in critique.upper():
        print("-> Critic approved, Sending to Publisher")
        return "publisher"
    
    # Check if max revisions reached
    if revision_count >= max_revisions:
        print("-> Max revision reached, Sending to Publisher")
        return "publisher"
    
    # Request revision
    print("-> Critic requested revisions, Sending back to Writer")
    return "write"  # ✅ Match the node name ("write" not "writer")

workflow.add_conditional_edges(
    source="critic",
    path=should_continue,
)

# Exit point
workflow.add_edge("publisher", END)

# ✅ Compile and export as 'workflow' (matches api.py import)
workflow = workflow.compile()