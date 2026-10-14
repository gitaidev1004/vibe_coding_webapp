"""
ch05/backend_fastapi/app/repositories/member_repository.py
회원(Member), 역할(Role) 데이터 접근 계층
"""
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.member import Member, Role


class MemberRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_username(self, username: str) -> Member | None:
        stmt = select(Member).where(Member.username == username)
        return self.db.execute(stmt).scalar_one_or_none()

    def find_by_id(self, member_id: int) -> Member | None:
        return self.db.get(Member, member_id)

    def find_all(self) -> list[Member]:
        stmt = select(Member).order_by(Member.member_id)
        return list(self.db.execute(stmt).scalars().all())

    def save(self, member: Member) -> Member:
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def delete(self, member: Member) -> None:
        self.db.delete(member)
        self.db.commit()


class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_name(self, role_name: str) -> Role | None:
        stmt = select(Role).where(Role.role_name == role_name)
        return self.db.execute(stmt).scalar_one_or_none()

    def find_by_id(self, role_id: int) -> Role | None:
        return self.db.get(Role, role_id)

    def find_all(self) -> list[Role]:
        return list(self.db.execute(select(Role).order_by(Role.role_id)).scalars().all())

    def save(self, role: Role) -> Role:
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def delete(self, role: Role) -> None:
        self.db.delete(role)
        self.db.commit()
