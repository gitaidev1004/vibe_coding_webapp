"""
ch03/05_fastapi/repository.py
FastAPI Layered Architecture - Repository 계층
데이터베이스에 직접 접근하는 코드를 이 계층에 모아 둔다.
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Member


class MemberRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_username(self, username: str) -> Member | None:
        stmt = select(Member).where(Member.username == username)
        return self.db.execute(stmt).scalar_one_or_none()

    def save(self, member: Member) -> Member:
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def find_all(self) -> list[Member]:
        stmt = select(Member).order_by(Member.id)
        return list(self.db.execute(stmt).scalars().all())
