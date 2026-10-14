"""
ch05/backend_fastapi/app/services/board_service.py
게시글 목록/검색/페이징, 상세 조회(조회수 증가), 등록, 수정, 삭제 비즈니스 로직
"""
from fastapi import HTTPException
from app.models.board import Post
from app.repositories.board_repository import PostRepository
from app.schemas.board import PostCreateRequest, PostUpdateRequest


class BoardService:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    def list_posts(self, keyword: str | None, page: int, page_size: int):
        if page < 1:
            raise HTTPException(status_code=400, detail="페이지 번호는 1 이상이어야 합니다.")
        items, total = self.repository.search(keyword, page, page_size)
        return items, total

    def get_post(self, post_id: int, increase_view: bool = True) -> Post:
        post = self.repository.find_by_id(post_id)
        if post is None:
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
        if increase_view:
            self.repository.increment_view_count(post)
        return post

    def create_post(self, board_id: int, member_id: int, request: PostCreateRequest) -> Post:
        post = Post(
            board_id=board_id, member_id=member_id,
            title=request.title, content=request.content,
        )
        return self.repository.save(post)

    def update_post(self, post_id: int, member_id: int, request: PostUpdateRequest) -> Post:
        post = self.get_post(post_id, increase_view=False)
        if post.member_id != member_id:
            raise HTTPException(status_code=403, detail="작성자만 수정할 수 있습니다.")
        from datetime import datetime
        post.title = request.title
        post.content = request.content
        post.updated_at = datetime.utcnow()
        return self.repository.save(post)

    def delete_post(self, post_id: int, member_id: int, is_admin: bool = False) -> None:
        post = self.get_post(post_id, increase_view=False)
        if post.member_id != member_id and not is_admin:
            raise HTTPException(status_code=403, detail="작성자 또는 관리자만 삭제할 수 있습니다.")
        self.repository.delete(post)
