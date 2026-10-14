"""
ch05/backend_flask/app/routers/auth_routes.py
로그인 API - 인증(Authentication) 처리
"""
from flask import Blueprint, request, jsonify
from app.deps import get_member_service

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/login")
def login():
    data = request.get_json()
    token, member = get_member_service().login(data["username"], data["password"])
    return jsonify({
        "token": token, "username": member.username, "role_name": member.role.role_name,
    }), 200
