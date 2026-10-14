"""
ch05/backend_flask/app/models/log.py
사용자 활동 이력을 저장하는 로그(log) 엔터티.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base


class Log(Base):
    __tablename__ = "log"
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("member.member_id"), nullable=True)
    action = Column(String(50), nullable=False)
    target = Column(String(200))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "log_id": self.log_id, "member_id": self.member_id,
            "action": self.action, "target": self.target,
            "created_at": self.created_at.isoformat(),
        }
