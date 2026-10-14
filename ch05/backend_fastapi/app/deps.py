"""
ch05/backend_fastapi/app/deps.py
공통 의존성(Dependency) 정의: DB 세션, 현재 로그인한 회원, 접근제어.
"""
from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.member import Member
from app.repositories.member_repository import MemberRepository, RoleRepository
from app.repositories.board_repository import PostRepository
from app.repositories.admin_repository import AccessRepository
from app.repositories.log_repository import LogRepository
from app.services.log_service import LogService
from app.services.member_service import MemberService
from app.services.board_service import BoardService
from app.services.access_control import AccessControlService
from app.services.admin_service import AdminService
from app.security import get_member_id_by_token


def get_log_service(db: Session = Depends(get_db)) -> LogService:
    return LogService(LogRepository(db))


def get_member_service(db: Session = Depends(get_db),
                        log_service: LogService = Depends(get_log_service)) -> MemberService:
    return MemberService(MemberRepository(db), RoleRepository(db), log_service)


def get_board_service(db: Session = Depends(get_db)) -> BoardService:
    return BoardService(PostRepository(db))


def get_access_control_service(db: Session = Depends(get_db),
                                log_service: LogService = Depends(get_log_service)) -> AccessControlService:
    return AccessControlService(AccessRepository(db), log_service)


def get_admin_service(db: Session = Depends(get_db)) -> AdminService:
    return AdminService(RoleRepository(db), AccessRepository(db))


def get_current_member(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> Member:
    """Authorization: Bearer <token> 헤더로부터 현재 로그인한 회원을 조회한다."""
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    token = authorization.removeprefix("Bearer ").strip()
    member_id = get_member_id_by_token(token)
    if member_id is None:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    member = MemberRepository(db).find_by_id(member_id)
    if member is None:
        raise HTTPException(status_code=401, detail="회원을 찾을 수 없습니다.")
    return member


def require_permission(function_code: str, need_write: bool = False):
    """특정 기능에 대한 접근 권한을 검사하는 의존성을 생성하는 팩토리 함수."""
    def checker(
        member: Member = Depends(get_current_member),
        access_control: AccessControlService = Depends(get_access_control_service),
    ) -> Member:
        access_control.check_permission(member, function_code, need_write)
        return member
    return checker
