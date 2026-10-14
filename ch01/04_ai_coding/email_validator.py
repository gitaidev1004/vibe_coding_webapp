"""
ch01/04_ai_coding/email_validator.py
AI 코딩 도구에게 "이메일 형식을 검증하는 함수를 만들어줘"라고
요청했을 때 생성될 수 있는 코드 예시와, 이를 검증하는 테스트 코드입니다.
"""
import re

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def is_valid_email(email: str) -> bool:
    """이메일 형식이 올바르면 True, 아니면 False를 반환한다."""
    if not email:
        return False
    return bool(EMAIL_PATTERN.match(email))


def run_tests():
    test_cases = [
        ("hong@example.com", True),
        ("hong.gildong@company.co.kr", True),
        ("hong@@example.com", False),
        ("hong.example.com", False),
        ("", False),
    ]

    print("=== 이메일 형식 검증 테스트 ===")
    passed = 0
    for email, expected in test_cases:
        result = is_valid_email(email)
        status = "통과" if result == expected else "실패"
        if result == expected:
            passed += 1
        print(f"  입력값: {email or '(빈 문자열)':30s} -> 결과: {result!s:5s} [{status}]")

    print(f"\n총 {len(test_cases)}건 중 {passed}건 통과")


if __name__ == "__main__":
    run_tests()
