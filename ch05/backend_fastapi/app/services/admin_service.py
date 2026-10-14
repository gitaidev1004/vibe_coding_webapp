"""
ch05/backend_fastapi/app/services/admin_service.py
역할(Role), 메뉴(Menu), 기능(Function), 권한(Permission) 관리 비즈니스 로직
"""
from fastapi import HTTPException
from app.models.member import Role
from app.models.access import Menu, Function, Permission
from app.repositories.member_repository import RoleRepository
from app.repositories.admin_repository import AccessRepository
from app.schemas.admin import RoleCreateRequest, PermissionSetRequest


class AdminService:
    def __init__(self, role_repository: RoleRepository, access_repository: AccessRepository):
        self.role_repository = role_repository
        self.access_repository = access_repository

    # --- 역할 관리 ---
    def create_role(self, request: RoleCreateRequest) -> Role:
        if self.role_repository.find_by_name(request.role_name) is not None:
            raise HTTPException(status_code=400, detail="이미 존재하는 역할입니다.")
        role = Role(role_name=request.role_name, description=request.description)
        return self.role_repository.save(role)

    def get_roles(self) -> list[Role]:
        return self.role_repository.find_all()

    def delete_role(self, role_id: int) -> None:
        role = self.role_repository.find_by_id(role_id)
        if role is None:
            raise HTTPException(status_code=404, detail="역할을 찾을 수 없습니다.")
        self.role_repository.delete(role)

    # --- 권한 관리 ---
    def set_permission(self, request: PermissionSetRequest) -> Permission:
        role = self.role_repository.find_by_id(request.role_id)
        if role is None:
            raise HTTPException(status_code=404, detail="역할을 찾을 수 없습니다.")
        function = self.access_repository.find_function_by_code(request.function_code)
        if function is None:
            raise HTTPException(status_code=404, detail="기능을 찾을 수 없습니다.")

        permission = self.access_repository.find_permission(role.role_id, function.function_id)
        if permission is None:
            permission = Permission(role_id=role.role_id, function_id=function.function_id)
        permission.can_read = request.can_read
        permission.can_write = request.can_write
        return self.access_repository.save_permission(permission)
