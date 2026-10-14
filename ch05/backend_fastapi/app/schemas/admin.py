"""
ch05/backend_fastapi/app/schemas/admin.py
역할/권한/로그 관리용 Request/Response Schema
"""
from pydantic import BaseModel
from datetime import datetime


class RoleCreateRequest(BaseModel):
    role_name: str
    description: str | None = None


class RoleResponse(BaseModel):
    role_id: int
    role_name: str
    description: str | None

    class Config:
        from_attributes = True


class PermissionSetRequest(BaseModel):
    role_id: int
    function_code: str
    can_read: bool = False
    can_write: bool = False


class LogResponse(BaseModel):
    log_id: int
    member_id: int | None
    action: str
    target: str | None
    created_at: datetime

    class Config:
        from_attributes = True
