"""
Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request model for asking questions about a YouTube video."""
    
    video_url: str = Field(..., description="YouTube video ID (11 characters)")
    question: str = Field(..., description="Question to ask about the video content", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "video_url": "https://youtu.be/UifWm9h96Ec?si=lxIApztLZpGTc9nm",
                "question": "What is the main topic of this video?"
            }
        }


class QueryResponse(BaseModel):
    """Response model for question answers."""
    
    answer: str = Field(..., description="Generated answer based on video transcript")
    video_url: str = Field(..., description="The video url that was queried")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "The main topic is...",
                "video_url": "https://youtu.be/UifWm9h96Ec?si=lxIApztLZpGTc9nm"
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str
    message: str