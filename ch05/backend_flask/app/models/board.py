"""
ch05/backend_flask/app/models/board.py
게시판(board)과 게시글(post) 엔터티.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Board(Base):
    __tablename__ = "board"
    board_id = Column(Integer, primary_key=True, autoincrement=True)
    board_name = Column(String(50), nullable=False)
    description = Column(String(200))


class Post(Base):
    __tablename__ = "post"
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    board_id = Column(Integer, ForeignKey("board.board_id"), nullable=False)
    member_id = Column(Integer, ForeignKey("member.member_id"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    view_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    board = relationship("Board")
    member = relationship("Member")

    def to_list_item(self):
        return {
            "post_id": self.post_id, "title": self.title,
            "author": self.member.username, "view_count": self.view_count,
            "created_at": self.created_at.isoformat(),
        }

    def to_detail(self):
        return {
            "post_id": self.post_id, "board_id": self.board_id, "title": self.title,
            "content": self.content, "author": self.member.username,
            "view_count": self.view_count, "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
