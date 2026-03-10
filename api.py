# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import asyncio
from graph import workflow  # ✅ Matches graph.py export

# 1. Initialize the FastAPI app
app = FastAPI(
    title="Local Agentic Newsroom API",
    description="API for autonomous research and blog writing",
    version="1.0.0"
)

# 2. Define the Request Model
class TopicRequest(BaseModel):
    topic: str
    max_revisions: Optional[int] = 3  # ✅ Plural for consistency

# 3. Define the Response Model
class BlogResponse(BaseModel):
    topic: str
    draft: str
    status: str
    revision_count: int

# 4. Define the Endpoint
@app.post("/generate", response_model=BlogResponse)
async def generate_blog(request: TopicRequest):
    try:
        # 5. Prepare the input state for LangGraph
        # ✅ Initialize ALL state keys defined in GraphState
        initial_state = {
            "topic": request.topic,
            "research_notes": [],
            "draft": "",
            "critique": "",
            "revision_count": 0,
            "max_revisions": request.max_revisions
        }
        
        # 6. Invoke the Graph Asynchronously
        final_state = await workflow.ainvoke(initial_state)
        
        # 7. Return the result
        return BlogResponse(
            topic=final_state["topic"],
            draft=final_state["draft"],
            status="published",
            revision_count=final_state["revision_count"]
        )
    except Exception as e:
        # 8. Error Handling
        raise HTTPException(status_code=500, detail=str(e))