"""
ch05/backend_fastapi/app/services/member_service.py
회원가입, 로그인, 회원 조회·수정·삭제(사용 여부 포함) 비즈니스 로직
"""
from fastapi import HTTPException
from app.models.member import Member
from app.repositories.member_repository import MemberRepository, RoleRepository
from app.schemas.member import MemberSignupRequest, MemberUpdateRequest
from app.security import hash_password, verify_password, issue_token
from app.services.log_service import LogService


class MemberService:
    def __init__(self, repository: MemberRepository, role_repository: RoleRepository,
                 log_service: LogService):
        self.repository = repository
        self.role_repository = role_repository
        self.log_service = log_service

    def signup(self, request: MemberSignupRequest) -> Member:
        if self.repository.find_by_username(request.username) is not None:
            raise HTTPException(status_code=400, detail="이미 사용 중인 아이디입니다.")

        default_role = self.role_repository.find_by_name("MEMBER")
        if default_role is None:
            raise HTTPException(status_code=500, detail="기본 역할(MEMBER)이 설정되어 있지 않습니다.")

        member = Member(
            username=request.username,
            password=hash_password(request.password),
            email=request.email,
            role_id=default_role.role_id,
        )
        return self.repository.save(member)

    def login(self, username: str, password: str) -> tuple[str, Member]:
        member = self.repository.find_by_username(username)
        if member is None or not verify_password(password, member.password):
            raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 올바르지 않습니다.")
        if not member.is_active:
            raise HTTPException(status_code=403, detail="사용이 중지된 계정입니다.")

        token = issue_token(member.member_id)
        self.log_service.record(member.member_id, "LOGIN", target=member.username)
        return token, member

    def get_member(self, member_id: int) -> Member:
        member = self.repository.find_by_id(member_id)
        if member is None:
            raise HTTPException(status_code=404, detail="회원을 찾을 수 없습니다.")
        return member

    def get_members(self) -> list[Member]:
        return self.repository.find_all()

    def update_member(self, member_id: int, request: MemberUpdateRequest) -> Member:
        member = self.get_member(member_id)
        if request.email is not None:
            member.email = request.email
        if request.is_active is not None:
            member.is_active = request.is_active
        return self.repository.save(member)

    def delete_member(self, member_id: int) -> None:
        member = self.get_member(member_id)
        self.repository.delete(member)
