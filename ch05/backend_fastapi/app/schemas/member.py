"""
ch05/backend_fastapi/app/schemas/member.py
회원 관련 Request/Response Schema
"""
from pydantic import BaseModel, Field
from datetime import datetime


class MemberSignupRequest(BaseModel):
    username: str = Field(min_length=4, max_length=20)
    password: str = Field(min_length=8)
    email: str


class MemberUpdateRequest(BaseModel):
    email: str | None = None
    is_active: bool | None = None


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    username: str
    role_name: str


class MemberResponse(BaseModel):
    member_id: int
    username: str
    email: str
    role_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
