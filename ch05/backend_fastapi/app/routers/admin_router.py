"""
ch05/backend_fastapi/app/routers/admin_router.py
관리자 전용 API: 역할 관리, 권한 관리, 로그 조회
"""
from fastapi import APIRouter, Depends
from app.schemas.admin import RoleCreateRequest, RoleResponse, PermissionSetRequest, LogResponse
from app.services.admin_service import AdminService
from app.services.log_service import LogService
from app.deps import get_admin_service, get_log_service, require_permission
from app.models.member import Member

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/roles", response_model=RoleResponse, status_code=201)
def create_role(
    request: RoleCreateRequest,
    service: AdminService = Depends(get_admin_service),
    _: Member = Depends(require_permission("ROLE_MANAGE", need_write=True)),
):
    return service.create_role(request)


@router.get("/roles", response_model=list[RoleResponse])
def get_roles(
    service: AdminService = Depends(get_admin_service),
    _: Member = Depends(require_permission("ROLE_MANAGE")),
):
    return service.get_roles()


@router.delete("/roles/{role_id}", status_code=204)
def delete_role(
    role_id: int,
    service: AdminService = Depends(get_admin_service),
    _: Member = Depends(require_permission("ROLE_MANAGE", need_write=True)),
):
    service.delete_role(role_id)


@router.post("/permissions", status_code=204)
def set_permission(
    request: PermissionSetRequest,
    service: AdminService = Depends(get_admin_service),
    _: Member = Depends(require_permission("ROLE_MANAGE", need_write=True)),
):
    service.set_permission(request)


@router.get("/logs", response_model=list[LogResponse])
def get_logs(
    service: LogService = Depends(get_log_service),
    _: Member = Depends(require_permission("LOG_VIEW")),
):
    return service.get_recent_logs()
