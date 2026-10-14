"""
ch05/backend_fastapi/app/schemas/comment.py
댓글 Request/Response Schema
"""
from pydantic import BaseModel, Field
from datetime import datetime


class CommentCreateRequest(BaseModel):
    content: str = Field(min_length=1, max_length=500)


class CommentResponse(BaseModel):
    comment_id: int
    author: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
