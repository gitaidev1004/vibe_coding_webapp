"""
ch05/backend_flask/app/services/board_service.py
게시글 목록/검색/페이징, 상세 조회(조회수 증가), 등록, 수정, 삭제 비즈니스 로직
"""
from datetime import datetime
from app.models.board import Post
from app.errors import ApiError


class BoardService:
    def __init__(self, repository):
        self.repository = repository

    def list_posts(self, keyword, page, page_size):
        if page < 1:
            raise ApiError("페이지 번호는 1 이상이어야 합니다.", 400)
        return self.repository.search(keyword, page, page_size)

    def get_post(self, post_id, increase_view=True):
        post = self.repository.find_by_id(post_id)
        if post is None:
            raise ApiError("게시글을 찾을 수 없습니다.", 404)
        if increase_view:
            self.repository.increment_view_count(post)
        return post

    def create_post(self, board_id, member_id, title, content):
        post = Post(board_id=board_id, member_id=member_id, title=title, content=content)
        return self.repository.save(post)

    def update_post(self, post_id, member_id, title, content):
        post = self.get_post(post_id, increase_view=False)
        if post.member_id != member_id:
            raise ApiError("작성자만 수정할 수 있습니다.", 403)
        post.title = title
        post.content = content
        post.updated_at = datetime.utcnow()
        return self.repository.save(post)

    def delete_post(self, post_id, member_id, is_admin=False):
        post = self.get_post(post_id, increase_view=False)
        if post.member_id != member_id and not is_admin:
            raise ApiError("작성자 또는 관리자만 삭제할 수 있습니다.", 403)
        self.repository.delete(post)
