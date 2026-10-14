"""
ch05/backend_flask/app/services/member_service.py
회원가입, 로그인, 회원 조회·수정·삭제(사용 여부 포함) 비즈니스 로직
"""
from app.models.member import Member
from app.errors import ApiError
from app.security import hash_password, verify_password, issue_token


class MemberService:
    def __init__(self, repository, role_repository, log_service):
        self.repository = repository
        self.role_repository = role_repository
        self.log_service = log_service

    def signup(self, username, password, email):
        if self.repository.find_by_username(username) is not None:
            raise ApiError("이미 사용 중인 아이디입니다.", 400)

        default_role = self.role_repository.find_by_name("MEMBER")
        if default_role is None:
            raise ApiError("기본 역할(MEMBER)이 설정되어 있지 않습니다.", 500)

        member = Member(
            username=username, password=hash_password(password),
            email=email, role_id=default_role.role_id,
        )
        return self.repository.save(member)

    def login(self, username, password):
        member = self.repository.find_by_username(username)
        if member is None or not verify_password(password, member.password):
            raise ApiError("아이디 또는 비밀번호가 올바르지 않습니다.", 401)
        if not member.is_active:
            raise ApiError("사용이 중지된 계정입니다.", 403)

        token = issue_token(member.member_id)
        self.log_service.record(member.member_id, "LOGIN", target=member.username)
        return token, member

    def get_member(self, member_id):
        member = self.repository.find_by_id(member_id)
        if member is None:
            raise ApiError("회원을 찾을 수 없습니다.", 404)
        return member

    def get_members(self):
        return self.repository.find_all()

    def update_member(self, member_id, email=None, is_active=None):
        member = self.get_member(member_id)
        if email is not None:
            member.email = email
        if is_active is not None:
            member.is_active = is_active
        return self.repository.save(member)

    def delete_member(self, member_id):
        member = self.get_member(member_id)
        self.repository.delete(member)
