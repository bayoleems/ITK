from pydantic import BaseModel, Field

class WebSearchResult(BaseModel):
    """Model for web search results containing top 3 matches with metadata"""

    search_summary: str = Field(..., description="A summary of the search results")
    metadata: dict = Field(..., description="Additional metadata about the search results")
