from pydantic import BaseModel, Field
from typing import List

class SemanticSearch(BaseModel):
    """Model for semantic search results containing top 2 matches with metadata"""

    query: str = Field(..., description="The search query that was executed")
    results: List[dict] = Field(..., max_items=2, description="List of top 2 search results with detailed information")
    result_summary: str = Field(..., description="A structured summary comparing and analyzing both search results")
    metadata: dict = Field(..., description="Additional metadata about the search results")