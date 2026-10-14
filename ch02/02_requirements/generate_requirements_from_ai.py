"""
ch02/02_requirements/generate_requirements_from_ai.py
AI에게 "게시판 기능에 대한 요구사항을 JSON으로 뽑아줘"라고 요청했다고 가정하고,
그 응답을 파싱하여 요구사항 정의서(CSV)로 저장하는 예제입니다.
"""
import json
import csv
from pathlib import Path

# AI로부터 받았다고 가정한 응답(JSON 문자열)
ai_response_json = """
[
    {
        "id": "REQ-101",
        "category": "기능",
        "title": "게시글 목록 조회",
        "description": "사용자는 게시글 목록을 최신순으로 조회할 수 있다.",
        "priority": "High",
        "acceptance_criteria": "목록은 페이지당 10건씩 최신 등록순으로 표시된다."
    },
    {
        "id": "REQ-102",
        "category": "기능",
        "title": "게시글 등록",
        "description": "로그인한 사용자는 제목과 내용을 입력하여 게시글을 등록할 수 있다.",
        "priority": "High",
        "acceptance_criteria": "제목이 비어 있으면 등록이 거부되고 오류 메시지가 표시된다."
    },
    {
        "id": "REQ-103",
        "category": "비기능",
        "title": "게시글 저장 안정성",
        "description": "게시글 등록 중 오류가 발생해도 데이터가 유실되지 않아야 한다.",
        "priority": "Medium",
        "acceptance_criteria": "등록 트랜잭션 실패 시 부분 저장 없이 전체 롤백된다."
    }
]
"""

FIELDNAMES = ["요구사항ID", "구분", "제목", "설명", "우선순위", "수용기준"]


def parse_ai_requirements(response_text: str):
    return json.loads(response_text)


def save_as_csv(requirements, output_path: Path):
    with output_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(FIELDNAMES)
        for r in requirements:
            writer.writerow([
                r["id"], r["category"], r["title"],
                r["description"], r["priority"], r["acceptance_criteria"],
            ])


if __name__ == "__main__":
    requirements = parse_ai_requirements(ai_response_json)
    output_path = Path("requirements_generated.csv")
    save_as_csv(requirements, output_path)

    print("=== AI 응답으로부터 요구사항 정의서 생성 완료 ===")
    print(f"저장 위치: {output_path.resolve()}")
    print(f"생성된 요구사항 수: {len(requirements)}건")
    print()
    for r in requirements:
        print(f"[{r['id']}] ({r['category']}/{r['priority']}) {r['title']}")
        print(f"   설명   : {r['description']}")
        print(f"   수용기준: {r['acceptance_criteria']}")
