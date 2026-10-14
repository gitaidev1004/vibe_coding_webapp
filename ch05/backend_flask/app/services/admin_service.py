"""
ch05/backend_flask/app/services/admin_service.py
역할(Role), 권한(Permission) 관리 비즈니스 로직
"""
from app.models.member import Role
from app.models.access import Permission
from app.errors import ApiError


class AdminService:
    def __init__(self, role_repository, access_repository):
        self.role_repository = role_repository
        self.access_repository = access_repository

    def create_role(self, role_name, description=None):
        if self.role_repository.find_by_name(role_name) is not None:
            raise ApiError("이미 존재하는 역할입니다.", 400)
        role = Role(role_name=role_name, description=description)
        return self.role_repository.save(role)

    def get_roles(self):
        return self.role_repository.find_all()

    def delete_role(self, role_id):
        role = self.role_repository.find_by_id(role_id)
        if role is None:
            raise ApiError("역할을 찾을 수 없습니다.", 404)
        self.role_repository.delete(role)

    def set_permission(self, role_id, function_code, can_read, can_write):
        role = self.role_repository.find_by_id(role_id)
        if role is None:
            raise ApiError("역할을 찾을 수 없습니다.", 404)
        function = self.access_repository.find_function_by_code(function_code)
        if function is None:
            raise ApiError("기능을 찾을 수 없습니다.", 404)

        permission = self.access_repository.find_permission(role.role_id, function.function_id)
        if permission is None:
            permission = Permission(role_id=role.role_id, function_id=function.function_id)
        permission.can_read = can_read
        permission.can_write = can_write
        return self.access_repository.save_permission(permission)
