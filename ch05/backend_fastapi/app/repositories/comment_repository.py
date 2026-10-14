"""
ch05/backend_fastapi/app/repositories/comment_repository.py
댓글(Comment) 데이터 접근 계층
"""
from sqlalchemy import select
from app.models.comment import Comment


class CommentRepository:
    def __init__(self, db):
        self.db = db

    def find_by_post(self, post_id: int):
        stmt = select(Comment).where(Comment.post_id == post_id).order_by(Comment.comment_id)
        return list(self.db.execute(stmt).scalars().all())

    def find_by_id(self, comment_id: int):
        return self.db.get(Comment, comment_id)

    def save(self, comment: Comment) -> Comment:
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def delete(self, comment: Comment) -> None:
        self.db.delete(comment)
        self.db.commit()
