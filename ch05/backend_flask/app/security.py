"""
ch05/backend_flask/app/security.py
비밀번호 해시와 간단한 토큰 기반 인증을 처리하는 모듈. (FastAPI 버전과 동일한 방식)
"""
import hashlib
import secrets

_token_store: dict[str, int] = {}


def hash_password(raw_password: str) -> str:
    return hashlib.sha256(raw_password.encode("utf-8")).hexdigest()


def verify_password(raw_password: str, hashed_password: str) -> bool:
    return hash_password(raw_password) == hashed_password


def issue_token(member_id: int) -> str:
    token = secrets.token_hex(16)
    _token_store[token] = member_id
    return token


def get_member_id_by_token(token: str) -> int | None:
    return _token_store.get(token)
