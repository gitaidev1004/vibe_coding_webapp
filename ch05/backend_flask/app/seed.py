"""
ch05/backend_flask/app/seed.py
애플리케이션 최초 구동 시 필요한 기본 데이터(역할, 메뉴, 기능, 권한, 게시판,
관리자 계정)를 생성하는 시드(seed) 스크립트. (FastAPI 버전과 동일한 데이터)
"""
from app.models.member import Role, Member
from app.models.access import Menu, Function, Permission
from app.models.board import Board
from app.security import hash_password


def run_seed(db) -> None:
    if db.query(Role).count() > 0:
        return

    admin_role = Role(role_name="ADMIN", description="관리자")
    member_role = Role(role_name="MEMBER", description="일반회원")
    db.add_all([admin_role, member_role])
    db.flush()

    board_menu = Menu(menu_name="게시판 관리", url="/board", sort_order=1)
    admin_menu = Menu(menu_name="관리자", url="/admin", sort_order=2)
    db.add_all([board_menu, admin_menu])
    db.flush()

    functions = [
        Function(function_name="게시글 관리", function_code="POST_MANAGE", menu_id=board_menu.menu_id),
        Function(function_name="회원 관리", function_code="MEMBER_MANAGE", menu_id=admin_menu.menu_id),
        Function(function_name="역할 관리", function_code="ROLE_MANAGE", menu_id=admin_menu.menu_id),
        Function(function_name="로그 조회", function_code="LOG_VIEW", menu_id=admin_menu.menu_id),
    ]
    db.add_all(functions)
    db.flush()

    for f in functions:
        db.add(Permission(role_id=admin_role.role_id, function_id=f.function_id,
                           can_read=True, can_write=True))

    db.add(Board(board_name="공지사항", description="공지 게시판"))

    db.add(Member(
        username="admin", password=hash_password("admin1234!"),
        email="admin@example.com", role_id=admin_role.role_id,
    ))

    db.commit()
