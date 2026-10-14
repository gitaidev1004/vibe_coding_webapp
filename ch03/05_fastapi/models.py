"""
ch03/05_fastapi/models.py
FastAPI Layered Architecture - Model 계층
SQLAlchemy ORM을 이용해 member 테이블과 매핑되는 모델을 정의합니다.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Member(Base):
    __tablename__ = "member"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
