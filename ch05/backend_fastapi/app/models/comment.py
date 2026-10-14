"""
ch05/backend_fastapi/app/models/comment.py
댓글(comment) 엔터티. 5.9절의 AI Agent 실습 예제로 추가된 기능이다.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Comment(Base):
    __tablename__ = "comment"

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("post.post_id"), nullable=False)
    member_id = Column(Integer, ForeignKey("member.member_id"), nullable=False)
    content = Column(String(500), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    member = relationship("Member")
