"""
ch05/backend_fastapi/app/repositories/log_repository.py
로그(Log) 데이터 접근 계층
"""
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.log import Log


class LogRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, log: Log) -> Log:
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def find_all(self, limit: int = 100) -> list[Log]:
        stmt = select(Log).order_by(Log.log_id.desc()).limit(limit)
        return list(self.db.execute(stmt).scalars().all())

    def find_by_member(self, member_id: int) -> list[Log]:
        stmt = select(Log).where(Log.member_id == member_id).order_by(Log.log_id.desc())
        return list(self.db.execute(stmt).scalars().all())
