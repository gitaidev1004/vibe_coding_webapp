"""
ch05/backend_fastapi/app/models/member.py
사용자(member)와 역할(role) 엔터티. 3.8(4)에서 설계한 ERD를 그대로 구현한다.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Role(Base):
    __tablename__ = "role"

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(30), nullable=False, unique=True)
    description = Column(String(200))

    members = relationship("Member", back_populates="role")


class Member(Base):
    __tablename__ = "member"

    member_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    role_id = Column(Integer, ForeignKey("role.role_id"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    role = relationship("Role", back_populates="members")
