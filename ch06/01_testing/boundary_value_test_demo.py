"""
ch06/01_testing/boundary_value_test_demo.py
경계값 테스트(Boundary Value Testing)와 예외 테스트 기법을 보여주는 예제입니다.
2.4(2)④에서 만든 회원가입 요구사항(비밀번호 8자 이상)을 검증 대상으로 삼는다.
"""


def validate_password(password: str) -> tuple[bool, str]:
    """비밀번호는 8자 이상 20자 이하여야 한다."""
    if not isinstance(password, str):
        return False, "비밀번호는 문자열이어야 합니다."
    length = len(password)
    if length < 8:
        return False, "비밀번호는 8자 이상이어야 합니다."
    if length > 20:
        return False, "비밀번호는 20자 이하여야 합니다."
    return True, "유효한 비밀번호입니다."


# 경계값 테스트: 조건이 바뀌는 지점(7,8,9자 / 19,20,21자) 주변을 집중적으로 검사한다.
boundary_cases = [
    ("1234567", False),    # 7자 - 경계값 미만
    ("12345678", True),    # 8자 - 경계값(최소)
    ("123456789", True),   # 9자 - 경계값 바로 위
    ("1" * 19, True),      # 19자 - 경계값 바로 아래
    ("1" * 20, True),      # 20자 - 경계값(최대)
    ("1" * 21, False),     # 21자 - 경계값 초과
]

# 예외 테스트: 정상적인 문자열이 아닌 값이 들어왔을 때의 처리를 확인한다.
exception_cases = [
    ("", False),
    (None, False),
    (12345678, False),  # 문자열이 아닌 숫자 타입
]


def run_cases(title, cases):
    print(f"=== {title} ===")
    passed = 0
    for value, expected_valid in cases:
        is_valid, message = validate_password(value)
        status = "통과" if is_valid == expected_valid else "실패"
        if is_valid == expected_valid:
            passed += 1
        display_value = value if not isinstance(value, str) or len(value) <= 10 else f"{value[:10]}...({len(value)}자)"
        print(f"  입력값={display_value!r:25s} 예상={expected_valid!s:5s} 실제={is_valid!s:5s} [{status}]")
    print(f"  -> {len(cases)}건 중 {passed}건 통과\n")


if __name__ == "__main__":
    run_cases("경계값 테스트 (8~20자 조건)", boundary_cases)
    run_cases("예외 테스트 (비정상 입력)", exception_cases)
