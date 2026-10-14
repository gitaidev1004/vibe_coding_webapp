"""
ch05/backend_fastapi/app/routers/auth_router.py
로그인 API - 인증(Authentication) 처리
"""
from fastapi import APIRouter, Depends
from app.schemas.member import LoginRequest, LoginResponse
from app.services.member_service import MemberService
from app.deps import get_member_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, service: MemberService = Depends(get_member_service)):
    token, member = service.login(request.username, request.password)
    return LoginResponse(token=token, username=member.username, role_name=member.role.role_name)
