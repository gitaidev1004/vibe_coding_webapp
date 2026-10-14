"""
ch05/backend_flask/app/repositories/member_repository.py
회원(Member), 역할(Role) 데이터 접근 계층
"""
from sqlalchemy import select
from app.models.member import Member, Role


class MemberRepository:
    def __init__(self, db):
        self.db = db

    def find_by_username(self, username):
        stmt = select(Member).where(Member.username == username)
        return self.db.execute(stmt).scalar_one_or_none()

    def find_by_id(self, member_id):
        return self.db.get(Member, member_id)

    def find_all(self):
        return list(self.db.execute(select(Member).order_by(Member.member_id)).scalars().all())

    def save(self, member):
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def delete(self, member):
        self.db.delete(member)
        self.db.commit()


class RoleRepository:
    def __init__(self, db):
        self.db = db

    def find_by_name(self, role_name):
        stmt = select(Role).where(Role.role_name == role_name)
        return self.db.execute(stmt).scalar_one_or_none()

    def find_by_id(self, role_id):
        return self.db.get(Role, role_id)

    def find_all(self):
        return list(self.db.execute(select(Role).order_by(Role.role_id)).scalars().all())

    def save(self, role):
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def delete(self, role):
        self.db.delete(role)
        self.db.commit()
