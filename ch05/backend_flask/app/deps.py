"""
ch05/backend_flask/app/deps.py
공통 의존 기능: 현재 요청의 DB 세션 획득, 로그인 회원 확인, 접근제어 데코레이터.
"""
from functools import wraps
from flask import g, request
from app import database
from app.errors import ApiError
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


def get_db():
    if "db" not in g:
        g.db = database.SessionLocal()
    return g.db


def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def get_member_service():
    db = get_db()
    return MemberService(MemberRepository(db), RoleRepository(db), LogService(LogRepository(db)))


def get_board_service():
    return BoardService(PostRepository(get_db()))


def get_access_control_service():
    db = get_db()
    return AccessControlService(AccessRepository(db), LogService(LogRepository(db)))


def get_admin_service():
    db = get_db()
    return AdminService(RoleRepository(db), AccessRepository(db))


def get_log_service():
    return LogService(LogRepository(get_db()))


def get_current_member():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise ApiError("로그인이 필요합니다.", 401)

    token = auth_header.removeprefix("Bearer ").strip()
    member_id = get_member_id_by_token(token)
    if member_id is None:
        raise ApiError("유효하지 않은 토큰입니다.", 401)

    member = MemberRepository(get_db()).find_by_id(member_id)
    if member is None:
        raise ApiError("회원을 찾을 수 없습니다.", 401)
    return member


def require_permission(function_code, need_write=False):
    """특정 기능에 대한 접근 권한을 검사하는 데코레이터를 생성하는 팩토리 함수."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            member = get_current_member()
            get_access_control_service().check_permission(member, function_code, need_write)
            g.current_member = member
            return view_func(*args, **kwargs)
        return wrapper
    return decorator
