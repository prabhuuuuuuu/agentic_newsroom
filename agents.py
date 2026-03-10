# agents.py
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from state import GraphState
from tools import search_tool, save_file  # ✅ Import individual tools

# Initialize LLM
llm = ChatOllama(
    model="llama3",
    temperature=0
)

def research_node(state: GraphState):
    print("--RESEARCHER--")
    topic = state["topic"]
    
    # ✅ Bind the correct tool (search_tool, not search_tools)
    llm_with_tools = llm.bind_tools([search_tool])
    
    messages = [
        SystemMessage(content="You are a research assistant. Use the search tool to find information."),
        HumanMessage(content=f"Research the following topic thoroughly: {topic}")
    ]
    
    response = llm_with_tools.invoke(messages)
    
    research_notes = []
    # ✅ Correct attribute: tool_calls (underscore, not dot)
    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call['name'] == 'tavily_search_results':
                result = search_tool.invoke(tool_call['args']['query'])
                research_notes.append(result)
    
    return {"research_notes": research_notes}

def write_node(state: GraphState):
    print("--WRITER--")
    topic = state["topic"]
    notes = state["research_notes"]
    critique = state.get("critique", "")
    
    system_prompt = """
    You are a technical writer. 
    Write a comprehensive blog post in GitHub Flavored Markdown.
    Use the provided research notes to ensure factual accuracy.
    """
    
    user_prompt = f"""
    Topic: {topic}
    Research Notes: {notes}
    """
    
    if critique:
        user_prompt += f"\nPrevious Critique: {critique}"
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    response = llm.invoke(messages)
    
    # ✅ No extra space in key ("draft" not "draft ")
    return {"draft": response.content}

def critique_node(state: GraphState):  # ✅ Function name is critique_node
    print("--CRITIC--")
    draft = state["draft"]
    
    system_prompt = """
    You are a harsh technical editor. 
    Evaluate the draft for factual depth, clarity, and formatting.
    If the draft is good, return 'APPROVED'.
    If not, provide specific critiques.
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Review this draft: \n{draft}")
    ]
    
    response = llm.invoke(messages)
    
    return {"critique": response.content}

def publish_node(state: GraphState):
    print("--PUBLISHER--")
    draft = state["draft"]
    result = save_file.invoke({"content": draft})
    print(result)
    
    return {}