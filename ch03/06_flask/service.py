"""
ch03/06_flask/service.py
Flask Layered Architecture - Service 계층
"""
from models import Member


class MemberError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code


class MemberService:
    def __init__(self, repository):
        self.repository = repository

    def signup(self, username, password, email):
        if self.repository.find_by_username(username) is not None:
            raise MemberError("이미 사용 중인 아이디입니다.", 400)

        member = Member(username=username, password=password, email=email)
        return self.repository.save(member)

    def get_members(self):
        return self.repository.find_all()
