"""
ch05/backend_fastapi/app/models/log.py
사용자 활동 이력을 저장하는 로그(log) 엔터티.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base


class Log(Base):
    __tablename__ = "log"

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("member.member_id"), nullable=True)
    action = Column(String(50), nullable=False)   # 예: LOGIN, CREATE_POST, ACCESS_DENIED
    target = Column(String(200))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
