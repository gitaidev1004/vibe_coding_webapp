"""
ch05/backend_fastapi/app/routers/member_router.py
회원가입, 내 정보 조회, 회원 목록/수정/삭제(관리자) API
"""
from fastapi import APIRouter, Depends
from app.schemas.member import MemberSignupRequest, MemberUpdateRequest, MemberResponse
from app.services.member_service import MemberService
from app.deps import get_member_service, get_current_member, require_permission
from app.models.member import Member

router = APIRouter(prefix="/api/members", tags=["members"])


def to_response(member: Member) -> MemberResponse:
    return MemberResponse(
        member_id=member.member_id, username=member.username, email=member.email,
        role_name=member.role.role_name, is_active=member.is_active, created_at=member.created_at,
    )


@router.post("", response_model=MemberResponse, status_code=201)
def signup(request: MemberSignupRequest, service: MemberService = Depends(get_member_service)):
    member = service.signup(request)
    return to_response(member)


@router.get("/me", response_model=MemberResponse)
def get_me(member: Member = Depends(get_current_member)):
    return to_response(member)


@router.get("", response_model=list[MemberResponse])
def get_members(
    service: MemberService = Depends(get_member_service),
    _: Member = Depends(require_permission("MEMBER_MANAGE")),
):
    return [to_response(m) for m in service.get_members()]


@router.put("/{member_id}", response_model=MemberResponse)
def update_member(
    member_id: int, request: MemberUpdateRequest,
    service: MemberService = Depends(get_member_service),
    _: Member = Depends(require_permission("MEMBER_MANAGE", need_write=True)),
):
    return to_response(service.update_member(member_id, request))


@router.delete("/{member_id}", status_code=204)
def delete_member(
    member_id: int,
    service: MemberService = Depends(get_member_service),
    _: Member = Depends(require_permission("MEMBER_MANAGE", need_write=True)),
):
    service.delete_member(member_id)
