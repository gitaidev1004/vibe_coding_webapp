"""
ch05/backend_flask/app/models/access.py
메뉴(menu), 기능(function), 권한(permission) 엔터티.
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Menu(Base):
    __tablename__ = "menu"
    menu_id = Column(Integer, primary_key=True, autoincrement=True)
    menu_name = Column(String(50), nullable=False)
    url = Column(String(100))
    parent_id = Column(Integer, ForeignKey("menu.menu_id"), nullable=True)
    sort_order = Column(Integer, nullable=False, default=0)


class Function(Base):
    __tablename__ = "function"
    function_id = Column(Integer, primary_key=True, autoincrement=True)
    function_name = Column(String(50), nullable=False)
    function_code = Column(String(50), nullable=False, unique=True)
    menu_id = Column(Integer, ForeignKey("menu.menu_id"), nullable=False)
    description = Column(String(200))


class Permission(Base):
    __tablename__ = "permission"
    role_id = Column(Integer, ForeignKey("role.role_id"), primary_key=True)
    function_id = Column(Integer, ForeignKey("function.function_id"), primary_key=True)
    can_read = Column(Boolean, nullable=False, default=False)
    can_write = Column(Boolean, nullable=False, default=False)

    role = relationship("Role")
    function = relationship("Function")
