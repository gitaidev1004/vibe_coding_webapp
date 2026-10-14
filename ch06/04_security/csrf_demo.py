"""
ch06/04_security/csrf_demo.py
CSRF(Cross-Site Request Forgery) 방어에 사용하는 CSRF 토큰 검증 로직을
간단히 구현하여, 토큰이 없거나 다른 요청의 토큰을 재사용할 경우
요청이 거부되는 것을 확인하는 예제입니다.
"""
import secrets

# 세션별로 발급한 CSRF 토큰을 저장한다고 가정한다. (실제로는 세션 저장소에 보관)
session_csrf_tokens: dict[str, str] = {}


def issue_csrf_token(session_id: str) -> str:
    token = secrets.token_hex(16)
    session_csrf_tokens[session_id] = token
    return token


def verify_csrf_token(session_id: str, submitted_token: str) -> bool:
    expected = session_csrf_tokens.get(session_id)
    return expected is not None and secrets.compare_digest(expected, submitted_token)


def handle_transfer_request(session_id: str, submitted_token: str, amount: int) -> str:
    """중요한 변경 작업(송금 등)을 처리하기 전에 CSRF 토큰을 검증한다."""
    if not verify_csrf_token(session_id, submitted_token):
        return "403 Forbidden: CSRF 토큰이 유효하지 않습니다."
    return f"200 OK: {amount}원 송금이 처리되었습니다."


if __name__ == "__main__":
    session_id = "session-abc123"
    real_token = issue_csrf_token(session_id)
    print(f"정상 발급된 CSRF 토큰: {real_token}")

    print("\n=== 정상적인 요청 (올바른 토큰 포함) ===")
    print(handle_transfer_request(session_id, real_token, 10000))

    print("\n=== CSRF 공격 시나리오 (토큰 없이 요청) ===")
    print(handle_transfer_request(session_id, "", 1000000))

    print("\n=== CSRF 공격 시나리오 (다른 세션의 토큰을 추측/재사용) ===")
    print(handle_transfer_request(session_id, "guessed-or-stolen-token", 1000000))
