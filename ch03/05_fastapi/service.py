"""
ch03/05_fastapi/service.py
FastAPI Layered Architecture - Service 계층
비즈니스 로직(중복 검사 등)을 이 계층에서 처리한다.
"""
from fastapi import HTTPException
from models import Member
from repository import MemberRepository
from schemas import MemberCreateRequest


class MemberService:
    def __init__(self, repository: MemberRepository):
        self.repository = repository

    def signup(self, request: MemberCreateRequest) -> Member:
        existing = self.repository.find_by_username(request.username)
        if existing is not None:
            raise HTTPException(status_code=400, detail="이미 사용 중인 아이디입니다.")

        member = Member(
            username=request.username,
            password=request.password,  # 실제 서비스에서는 반드시 해시로 저장해야 한다.
            email=request.email,
        )
        return self.repository.save(member)

    def get_members(self) -> list[Member]:
        return self.repository.find_all()
