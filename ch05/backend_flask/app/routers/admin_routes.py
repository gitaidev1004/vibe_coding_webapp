"""
ch05/backend_flask/app/routers/admin_routes.py
관리자 전용 API: 역할 관리, 권한 관리, 로그 조회
"""
from flask import Blueprint, request, jsonify
from app.deps import get_admin_service, get_log_service, require_permission

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def role_to_dict(role):
    return {"role_id": role.role_id, "role_name": role.role_name, "description": role.description}


@admin_bp.post("/roles")
@require_permission("ROLE_MANAGE", need_write=True)
def create_role():
    data = request.get_json()
    role = get_admin_service().create_role(data["role_name"], data.get("description"))
    return jsonify(role_to_dict(role)), 201


@admin_bp.get("/roles")
@require_permission("ROLE_MANAGE")
def get_roles():
    roles = get_admin_service().get_roles()
    return jsonify([role_to_dict(r) for r in roles]), 200


@admin_bp.delete("/roles/<int:role_id>")
@require_permission("ROLE_MANAGE", need_write=True)
def delete_role(role_id):
    get_admin_service().delete_role(role_id)
    return "", 204


@admin_bp.post("/permissions")
@require_permission("ROLE_MANAGE", need_write=True)
def set_permission():
    data = request.get_json()
    get_admin_service().set_permission(
        data["role_id"], data["function_code"],
        data.get("can_read", False), data.get("can_write", False),
    )
    return "", 204


@admin_bp.get("/logs")
@require_permission("LOG_VIEW")
def get_logs():
    logs = get_log_service().get_recent_logs()
    return jsonify([log.to_dict() for log in logs]), 200
