"""
ch01/02_prompt_context/parse_structured_output.py
AI에게 JSON 형식으로 응답을 요청했다고 가정하고,
그 결과 문자열을 파싱하여 활용하는 예제입니다.
(실제 서비스에서는 이 문자열 자리에 AI API의 응답 결과가 들어옵니다.)
"""
import json

# AI 모델이 아래와 같은 System/User Prompt에 대해
# JSON 형식으로만 응답하도록 요청했다고 가정한다.
SYSTEM_PROMPT = (
    "너는 요구사항 분석가다. 사용자의 요청을 분석하여 "
    "JSON 형식으로만 응답하라. 다른 설명은 출력하지 마라."
)
USER_PROMPT = "회원가입 화면에 필요한 입력 항목을 알려줘."

# AI로부터 받았다고 가정한 응답(JSON 문자열)
ai_response_text = """
{
    "screen_name": "회원가입",
    "fields": [
        {"name": "username", "label": "아이디", "required": true},
        {"name": "password", "label": "비밀번호", "required": true},
        {"name": "email", "label": "이메일", "required": true},
        {"name": "phone", "label": "휴대폰번호", "required": false}
    ]
}
"""


def parse_ai_response(response_text: str) -> dict:
    data = json.loads(response_text)
    return data


if __name__ == "__main__":
    print("[System Prompt]", SYSTEM_PROMPT)
    print("[User Prompt]  ", USER_PROMPT)
    print()

    result = parse_ai_response(ai_response_text)

    print(f"화면명: {result['screen_name']}")
    print("입력 항목 목록:")
    for field in result["fields"]:
        mark = "필수" if field["required"] else "선택"
        print(f"  - {field['label']} ({field['name']}) : {mark}")
