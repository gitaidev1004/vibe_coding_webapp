"""
ch05/backend_flask/app/routers/board_routes.py
게시글 목록/검색/페이징, 상세, 등록, 수정, 삭제 API
"""
from flask import Blueprint, request, jsonify
from app.deps import get_board_service, get_current_member

board_bp = Blueprint("board", __name__, url_prefix="/api/posts")


@board_bp.get("")
def list_posts():
    keyword = request.args.get("keyword")
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))

    items, total = get_board_service().list_posts(keyword, page, page_size)
    return jsonify({
        "items": [p.to_list_item() for p in items],
        "total": total, "page": page, "page_size": page_size,
    }), 200


@board_bp.get("/<int:post_id>")
def get_post(post_id):
    post = get_board_service().get_post(post_id)
    return jsonify(post.to_detail()), 200


@board_bp.post("")
def create_post():
    data = request.get_json()
    member = get_current_member()
    board_id = int(request.args.get("board_id", 1))
    service = get_board_service()
    post = service.create_post(board_id, member.member_id, data["title"], data["content"])
    created = service.get_post(post.post_id, increase_view=False)
    return jsonify(created.to_detail()), 201


@board_bp.put("/<int:post_id>")
def update_post(post_id):
    data = request.get_json()
    member = get_current_member()
    post = get_board_service().update_post(post_id, member.member_id, data["title"], data["content"])
    return jsonify(post.to_detail()), 200


@board_bp.delete("/<int:post_id>")
def delete_post(post_id):
    member = get_current_member()
    is_admin = member.role.role_name == "ADMIN"
    get_board_service().delete_post(post_id, member.member_id, is_admin)
    return "", 204
