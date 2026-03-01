from langgraph.graph import StateGraph, START, END
from state import GraphState
from agents import research_node, write_node, critic_node, publish_node


workflow = StateGraph(GraphState)

#adding nodes to the graph

workflow.add_node("researcher", research_node)
workflow.add_node("write", write_node)
workflow.add_node("critic", critic_node)
workflow.add_node("publisher", publish_node)

#defining entry point

workflow.add_edge(START, "researcher")

#define linear flow
workflow.add_edge("researcher", "write")
workflow.add_edge("write", "critic")

#define confditional edge

def should_continue(state: GraphState):
    print("--DECIDING NEXT STEP--")
    critique = state.get("critique", "")
    revision_count = state.get("revision_count", 0)
    
    #check if critic approved

    if 'APPROVED' in critique.upper():
        print("-> Critic approved, Sending to Publisher")
        return "publisher"
    
    if revision_count >= 3:
        print("Max revision reached, Sending to Publisher")
        return "publisher"
    
    print("-> Critic requested revisions, Sending back to Writer")
    return "writer"


workflow.add_conditional_edges(
    source="critic",
    path=should_continue,
    mapping={
        "writer": "writer",
        "publisher": "publisher"
    }
)

#exit point
workflow.add_edge("publisher", END) 

app = workflow.compile()