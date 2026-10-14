"""
ch03/05_fastapi/router.py
FastAPI Layered Architecture - Router 계층
HTTP 요청을 받아 Service 계층으로 전달하고, 결과를 응답으로 반환한다.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from repository import MemberRepository
from service import MemberService
from schemas import MemberCreateRequest, MemberResponse

router = APIRouter(prefix="/api/members", tags=["members"])


def get_member_service(db: Session = Depends(get_db)) -> MemberService:
    return MemberService(MemberRepository(db))


@router.post("", response_model=MemberResponse, status_code=201)
def signup(request: MemberCreateRequest, service: MemberService = Depends(get_member_service)):
    member = service.signup(request)
    return member


@router.get("", response_model=list[MemberResponse])
def get_members(service: MemberService = Depends(get_member_service)):
    return service.get_members()
