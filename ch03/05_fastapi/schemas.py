"""
ch03/05_fastapi/schemas.py
FastAPI Layered Architecture - Schema 계층
Pydantic을 이용해 요청(Request)과 응답(Response) 데이터 형식을 정의합니다.
"""
from pydantic import BaseModel, Field
from datetime import datetime


class MemberCreateRequest(BaseModel):
    """회원가입 요청 스키마"""
    username: str = Field(min_length=4, max_length=20)
    password: str = Field(min_length=8)
    email: str


class MemberResponse(BaseModel):
    """회원 조회 응답 스키마 (비밀번호는 응답에 포함하지 않는다)"""
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
