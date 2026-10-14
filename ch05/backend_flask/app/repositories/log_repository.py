"""
ch05/backend_flask/app/repositories/log_repository.py
로그(Log) 데이터 접근 계층
"""
from sqlalchemy import select
from app.models.log import Log


class LogRepository:
    def __init__(self, db):
        self.db = db

    def save(self, log):
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def find_all(self, limit=100):
        stmt = select(Log).order_by(Log.log_id.desc()).limit(limit)
        return list(self.db.execute(stmt).scalars().all())
