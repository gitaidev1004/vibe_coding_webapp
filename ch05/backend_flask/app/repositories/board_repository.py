"""
ch05/backend_flask/app/repositories/board_repository.py
게시판(Board), 게시글(Post) 데이터 접근 계층
"""
from sqlalchemy import select, func, or_
from app.models.board import Board, Post


class BoardRepository:
    def __init__(self, db):
        self.db = db

    def find_all(self):
        return list(self.db.execute(select(Board)).scalars().all())

    def save(self, board):
        self.db.add(board)
        self.db.commit()
        self.db.refresh(board)
        return board


class PostRepository:
    def __init__(self, db):
        self.db = db

    def find_by_id(self, post_id):
        return self.db.get(Post, post_id)

    def search(self, keyword, page, page_size):
        stmt = select(Post)
        count_stmt = select(func.count()).select_from(Post)
        if keyword:
            cond = or_(Post.title.contains(keyword), Post.content.contains(keyword))
            stmt = stmt.where(cond)
            count_stmt = count_stmt.where(cond)

        total = self.db.execute(count_stmt).scalar_one()
        stmt = stmt.order_by(Post.post_id.desc()).offset((page - 1) * page_size).limit(page_size)
        items = list(self.db.execute(stmt).scalars().all())
        return items, total

    def save(self, post):
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def delete(self, post):
        self.db.delete(post)
        self.db.commit()

    def increment_view_count(self, post):
        post.view_count += 1
        self.db.commit()
        self.db.refresh(post)
