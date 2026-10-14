"""
ch05/backend_fastapi/app/repositories/admin_repository.py
메뉴(Menu), 기능(Function), 권한(Permission) 데이터 접근 계층
"""
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.access import Menu, Function, Permission


class AccessRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_function_by_code(self, function_code: str) -> Function | None:
        stmt = select(Function).where(Function.function_code == function_code)
        return self.db.execute(stmt).scalar_one_or_none()

    def find_permission(self, role_id: int, function_id: int) -> Permission | None:
        return self.db.get(Permission, {"role_id": role_id, "function_id": function_id})

    def save_menu(self, menu: Menu) -> Menu:
        self.db.add(menu)
        self.db.commit()
        self.db.refresh(menu)
        return menu

    def save_function(self, function: Function) -> Function:
        self.db.add(function)
        self.db.commit()
        self.db.refresh(function)
        return function

    def save_permission(self, permission: Permission) -> Permission:
        self.db.add(permission)
        self.db.commit()
        self.db.refresh(permission)
        return permission
