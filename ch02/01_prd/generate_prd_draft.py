"""
ch02/01_prd/generate_prd_draft.py
AI에게 "간단한 스터디 모임 관리 서비스의 PRD 초안을 JSON으로 작성해줘"라고
요청했다고 가정하고, 그 응답(JSON)을 읽어 마크다운 PRD 문서로 변환하는 예제입니다.
(실제 서비스에서는 ai_response_json 자리에 AI API의 응답 결과가 들어옵니다.)
"""
import json
from pathlib import Path

# AI로부터 받았다고 가정한 응답(JSON 문자열)
ai_response_json = """
{
    "project_name": "스터디 모임 관리 서비스",
    "one_line_summary": "스터디 모임의 공지와 출석을 한곳에서 관리하는 웹 서비스",
    "problem": "스터디 공지가 여러 메신저 방에 흩어져 있어 확인이 번거롭다.",
    "goals": {
        "purpose": "스터디 운영에 필요한 정보를 한곳에 모은다.",
        "user_goal": "공지와 일정을 놓치지 않고 확인한다.",
        "system_goal": "공지 등록 후 3초 이내에 목록에 반영한다.",
        "success_metric": "월간 활성 사용자(MAU) 100명 달성"
    },
    "users": [
        {"type": "일반 회원", "need": "공지 확인, 출석 체크"},
        {"type": "운영진", "need": "공지 작성, 출석 관리"}
    ],
    "core_features": [
        {"id": "F-001", "name": "회원가입/로그인", "priority": "Must"},
        {"id": "F-002", "name": "공지사항 게시판", "priority": "Must"},
        {"id": "F-003", "name": "출석 체크", "priority": "Should"}
    ],
    "non_functional": [
        {"category": "성능", "requirement": "동시 접속 50명까지 응답 지연 1초 이내"},
        {"category": "보안", "requirement": "비밀번호는 해시로 저장"}
    ],
    "constraints": ["1인 개발, 8주 이내 완성"]
}
"""


def build_prd_markdown(data: dict) -> str:
    lines = []
    lines.append(f"# PRD - {data['project_name']}")
    lines.append("")
    lines.append("## 1. 프로젝트 개요")
    lines.append(f"- 한 줄 소개: {data['one_line_summary']}")
    lines.append("")
    lines.append("## 2. 문제 정의")
    lines.append(f"- {data['problem']}")
    lines.append("")
    lines.append("## 3. 목표")
    g = data["goals"]
    lines.append(f"- 프로젝트 목적: {g['purpose']}")
    lines.append(f"- 사용자 목표: {g['user_goal']}")
    lines.append(f"- 시스템 목표: {g['system_goal']}")
    lines.append(f"- 성공 기준: {g['success_metric']}")
    lines.append("")
    lines.append("## 4. 사용자")
    lines.append("| 사용자 유형 | 주요 니즈 |")
    lines.append("|---|---|")
    for u in data["users"]:
        lines.append(f"| {u['type']} | {u['need']} |")
    lines.append("")
    lines.append("## 5. 핵심 기능")
    lines.append("| 기능 ID | 기능명 | 우선순위 |")
    lines.append("|---|---|---|")
    for f in data["core_features"]:
        lines.append(f"| {f['id']} | {f['name']} | {f['priority']} |")
    lines.append("")
    lines.append("## 6. 비기능 요구사항")
    lines.append("| 구분 | 요구사항 |")
    lines.append("|---|---|")
    for n in data["non_functional"]:
        lines.append(f"| {n['category']} | {n['requirement']} |")
    lines.append("")
    lines.append("## 7. 제약사항")
    for c in data["constraints"]:
        lines.append(f"- {c}")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    data = json.loads(ai_response_json)
    markdown = build_prd_markdown(data)

    output_path = Path("prd_draft_output.md")
    output_path.write_text(markdown, encoding="utf-8")

    print("=== PRD 초안 생성 완료 ===")
    print(f"저장 위치: {output_path.resolve()}")
    print()
    print(markdown)
