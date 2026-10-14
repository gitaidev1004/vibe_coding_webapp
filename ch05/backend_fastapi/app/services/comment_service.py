"""
ch05/backend_fastapi/app/services/comment_service.py
댓글 등록/조회/삭제 비즈니스 로직
"""
from fastapi import HTTPException
from app.models.comment import Comment


class CommentService:
    def __init__(self, repository, post_repository):
        self.repository = repository
        self.post_repository = post_repository

    def add_comment(self, post_id: int, member_id: int, content: str) -> Comment:
        if self.post_repository.find_by_id(post_id) is None:
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
        if not content.strip():
            raise HTTPException(status_code=400, detail="댓글 내용을 입력해 주세요.")
        comment = Comment(post_id=post_id, member_id=member_id, content=content)
        return self.repository.save(comment)

    def get_comments(self, post_id: int):
        return self.repository.find_by_post(post_id)

    def delete_comment(self, comment_id: int, member_id: int) -> None:
        comment = self.repository.find_by_id(comment_id)
        if comment is None:
            raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
        if comment.member_id != member_id:
            raise HTTPException(status_code=403, detail="작성자만 삭제할 수 있습니다.")
        self.repository.delete(comment)
