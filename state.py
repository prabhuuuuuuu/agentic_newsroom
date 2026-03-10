# state.py
from typing import TypedDict, Annotated, List
import operator

class GraphState(TypedDict):
    topic: str
    research_notes: Annotated[List[str], operator.add]
    draft: str
    critique: str
    revision_count: int
    max_revisions: int  