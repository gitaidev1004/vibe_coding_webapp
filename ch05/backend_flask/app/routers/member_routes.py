"""
ch05/backend_flask/app/routers/member_routes.py
회원가입, 내 정보 조회, 회원 목록/수정/삭제(관리자) API
"""
from flask import Blueprint, request, jsonify, g
from app.deps import get_member_service, get_current_member, require_permission

member_bp = Blueprint("member", __name__, url_prefix="/api/members")


def to_response(member):
    return {
        "member_id": member.member_id, "username": member.username, "email": member.email,
        "role_name": member.role.role_name, "is_active": member.is_active,
        "created_at": member.created_at.isoformat(),
    }


@member_bp.post("")
def signup():
    data = request.get_json()
    member = get_member_service().signup(data["username"], data["password"], data["email"])
    return jsonify(to_response(member)), 201


@member_bp.get("/me")
def get_me():
    member = get_current_member()
    return jsonify(to_response(member)), 200


@member_bp.get("")
@require_permission("MEMBER_MANAGE")
def get_members():
    members = get_member_service().get_members()
    return jsonify([to_response(m) for m in members]), 200


@member_bp.put("/<int:member_id>")
@require_permission("MEMBER_MANAGE", need_write=True)
def update_member(member_id):
    data = request.get_json()
    member = get_member_service().update_member(
        member_id, email=data.get("email"), is_active=data.get("is_active"))
    return jsonify(to_response(member)), 200


@member_bp.delete("/<int:member_id>")
@require_permission("MEMBER_MANAGE", need_write=True)
def delete_member(member_id):
    get_member_service().delete_member(member_id)
    return "", 204
