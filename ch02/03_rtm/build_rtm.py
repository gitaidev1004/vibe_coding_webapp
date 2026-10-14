"""
ch02/03_rtm/build_rtm.py
요구사항 목록과, 요구사항이 어떤 기능/유스케이스/화면/API/테스트와
연결되는지 매핑 정보를 합쳐 요구사항 추적표(RTM)를 생성하는 예제입니다.
"""
import csv
from pathlib import Path

# 요구사항 목록 (2.4절 요구사항 정의서에서 가져왔다고 가정)
requirements = [
    {"id": "REQ-001", "title": "회원가입"},
    {"id": "REQ-002", "title": "로그인"},
    {"id": "REQ-101", "title": "게시글 목록 조회"},
]

# 요구사항별 추적 매핑 정보 (설계 산출물에서 가져왔다고 가정)
trace_map = {
    "REQ-001": {
        "usecase": "UC-01 회원가입",
        "screen": "SCR-01 회원가입 화면",
        "api": "POST /api/members",
        "test_case": "TC-001",
    },
    "REQ-002": {
        "usecase": "UC-02 로그인",
        "screen": "SCR-02 로그인 화면",
        "api": "POST /api/auth/login",
        "test_case": "TC-002",
    },
    "REQ-101": {
        "usecase": "UC-03 게시글 목록 조회",
        "screen": "SCR-03 게시판 목록",
        "api": "GET /api/posts",
        "test_case": "TC-101",
    },
}

FIELDNAMES = ["요구사항ID", "기능", "유스케이스", "화면", "API", "테스트케이스"]


def build_rtm_rows(requirements, trace_map):
    rows = []
    missing = []
    for req in requirements:
        trace = trace_map.get(req["id"])
        if trace is None:
            missing.append(req["id"])
            continue
        rows.append([
            req["id"], req["title"], trace["usecase"],
            trace["screen"], trace["api"], trace["test_case"],
        ])
    return rows, missing


def save_rtm_csv(rows, output_path: Path):
    with output_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(FIELDNAMES)
        writer.writerows(rows)


if __name__ == "__main__":
    rows, missing = build_rtm_rows(requirements, trace_map)

    output_path = Path("rtm_generated.csv")
    save_rtm_csv(rows, output_path)

    print("=== 요구사항 추적표(RTM) 생성 완료 ===")
    print(f"저장 위치: {output_path.resolve()}")
    print()
    header = FIELDNAMES
    print(" | ".join(header))
    for row in rows:
        print(" | ".join(row))

    if missing:
        print(f"\n[경고] 추적 정보가 없는 요구사항: {', '.join(missing)}")
    else:
        print("\n모든 요구사항이 기능/유스케이스/화면/API/테스트와 빠짐없이 연결되었습니다.")
