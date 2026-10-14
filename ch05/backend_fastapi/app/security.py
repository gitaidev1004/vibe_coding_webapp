"""
ch05/backend_fastapi/app/security.py
비밀번호 해시와 간단한 토큰 기반 인증을 처리하는 모듈.
실무에서는 passlib(bcrypt)와 PyJWT 같은 검증된 라이브러리를 사용하는 것을
권장하지만, 이 책에서는 별도 설치 없이 개념을 확인할 수 있도록
표준 라이브러리(hashlib, secrets)만으로 최소한의 구현을 제공한다.
"""
import hashlib
import secrets

# 로그인 성공 시 발급한 토큰을 서버 메모리에 저장한다.
# (실제 서비스에서는 Redis 등 공유 저장소나 JWT의 자체 서명 검증을 사용한다)
_token_store: dict[str, int] = {}  # token -> member_id


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


def revoke_token(token: str) -> None:
    _token_store.pop(token, None)
