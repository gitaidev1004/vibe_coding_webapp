"""
ch03/06_flask/repository.py
Flask Layered Architecture - Repository 계층
"""
from sqlalchemy import select
from models import Member


class MemberRepository:
    def __init__(self, db_session):
        self.db = db_session

    def find_by_username(self, username):
        stmt = select(Member).where(Member.username == username)
        return self.db.execute(stmt).scalar_one_or_none()

    def save(self, member):
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def find_all(self):
        stmt = select(Member).order_by(Member.id)
        return list(self.db.execute(stmt).scalars().all())
