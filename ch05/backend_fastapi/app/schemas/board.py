"""
ch05/backend_fastapi/app/schemas/board.py
게시글 관련 Request/Response Schema
"""
from pydantic import BaseModel, Field
from datetime import datetime


class PostCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class PostUpdateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class PostListItemResponse(BaseModel):
    post_id: int
    title: str
    author: str
    view_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class PostDetailResponse(BaseModel):
    post_id: int
    board_id: int
    title: str
    content: str
    author: str
    view_count: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


class PagedPostResponse(BaseModel):
    items: list[PostListItemResponse]
    total: int
    page: int
    page_size: int
