"""
ch03/06_flask/routes.py
Flask Layered Architecture - Blueprint/Route 계층
HTTP 요청을 받아 Service 계층으로 전달하고, 결과를 JSON 응답으로 반환한다.
"""
from flask import Blueprint, request, jsonify, g

from database import SessionLocal
from repository import MemberRepository
from service import MemberService, MemberError

member_bp = Blueprint("member", __name__, url_prefix="/api/members")


def get_service():
    if "db" not in g:
        g.db = SessionLocal()
    return MemberService(MemberRepository(g.db))


@member_bp.post("")
def signup():
    data = request.get_json()
    service = get_service()
    try:
        member = service.signup(data["username"], data["password"], data["email"])
        return jsonify(member.to_dict()), 201
    except MemberError as e:
        return jsonify({"detail": e.message}), e.status_code


@member_bp.get("")
def get_members():
    service = get_service()
    members = service.get_members()
    return jsonify([m.to_dict() for m in members]), 200
