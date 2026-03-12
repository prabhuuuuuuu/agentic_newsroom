# agents.py
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from tools import search_tool, generate_image_tool, save_file_tool

# Initialize local LLM - runs on your machine, FREE!
# temperature=0 makes output deterministic (same input = same output)
llm = ChatOllama(model="llama3.2", temperature=0)

def researcher_node(state):
    """
    RESEARCHER AGENT
    Searches web for sources on the topic.
    """
    topic = state["topic"]
    
    # Call search tool
    search_results = search_tool(topic)
    
    # Return state updates (LangGraph merges these automatically)
    return {
        "research_notes": search_results,
        "messages": [f"🔍 Researched: {topic} - Found {len(search_results)} sources"]
    }

def writer_node(state):
    """
    WRITER AGENT
    Creates blog post draft from research notes.
    Handles both initial draft and revisions.
    """
    topic = state["topic"]
    research_notes = state["research_notes"]
    human_feedback = state.get("human_feedback", "")
    critique = state.get("critique", "")
    revision_count = state["revision_count"]
    
    # Combine research into context
    context = "\n\n".join(research_notes)
    
    # Build instruction based on whether this is a revision
    if human_feedback or critique:
        instruction = f"""
        REVISE the draft based on:
        - Critic feedback: {critique}
        - Human editor feedback: {human_feedback}
        - This is revision #{revision_count + 1}
        """
    else:
        instruction = "Write a comprehensive technical blog post from scratch."
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a technical writer. Write in GitHub Flavored Markdown.
        Include: Title (H1), Introduction, Main Sections (H2), Code Examples, Conclusion.
        Be factual and cite sources from research notes."""),
        ("human", """Topic: {topic}
        Research Notes: {context}
        Instruction: {instruction}
        """)
    ])
    
    # Generate draft using LLM
    response = llm.invoke(prompt.format(
        topic=topic, 
        context=context, 
        instruction=instruction
    ))
    
    # Create image prompt for this topic
    image_prompt = f"Technical illustration for blog post about {topic}, minimalist, professional, blue and white"
    
    return {
        "draft": response.content,
        "image_prompt": image_prompt,
        "revision_count": revision_count + 1,
        "messages": [f"✍️ Draft written (Revision {revision_count + 1})"]
    }

def critic_node(state):
    """
    CRITIC AGENT
    Evaluates draft quality. Provides harsh, constructive feedback.
    """
    draft = state["draft"]
    research_notes = state["research_notes"]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a harsh technical editor. Evaluate:
        1. Factual accuracy (cross-reference with research notes)
        2. Depth of content
        3. Markdown formatting
        4. Code example quality
        
        If draft is EXCELLENT, respond exactly: 'APPROVED'
        Otherwise, provide specific critique with sections to improve."""),
        ("human", """Draft: {draft}
        Research Notes: {research_notes}
        """)
    ])
    
    response = llm.invoke(prompt.format(
        draft=draft, 
        research_notes="\n".join(research_notes)
    ))
    
    # Check if approved or needs revision
    approval = "approved" if "APPROVED" in response.content.upper() else "needs_revision"
    
    return {
        "critique": response.content,
        "approval_status": approval,
        "messages": [f"📝 Critic review: {approval}"]
    }

def image_generator_node(state):
    """
    IMAGE GENERATOR AGENT
    Creates featured image using Stability AI.
    """
    image_prompt = state["image_prompt"]
    
    # Call image generation tool
    image_path = generate_image_tool(image_prompt)
    
    return {
        "image_path": image_path,
        "messages": [f"🖼️ Image generated: {image_path}"]
    }

def publisher_node(state):
    """
    PUBLISHER AGENT
    Saves final draft and image to output folder.
    """
    draft = state["draft"]
    image_path = state.get("image_path", "")
    topic = state["topic"]
    
    # Create safe filename from topic
    filename = f"{topic.replace(' ', '_')[:30]}.md"
    
    # Add image reference to markdown if image exists
    if image_path and "error" not in image_path:
        draft = f"![Featured Image]({image_path})\n\n" + draft
    
    # Save file
    save_file_tool(draft, filename)
    
    return {
        "messages": [f"✅ Published: output/{filename}"]
    }