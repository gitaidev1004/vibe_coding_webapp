"""
ch02/02_requirements/validate_requirements.py
요구사항 정의서(리스트)를 규칙 기반으로 점검하는 예제입니다.
- 중복 ID / 누락 항목 / 모호한 표현 / 상충 가능성을 자동으로 찾아냅니다.
- 실제 프로젝트에서는 이 규칙 기반 점검에 AI 검토 결과를 더해 사용합니다.
"""

# 점검 대상 요구사항 목록 (일부러 문제가 되는 항목을 포함시켰다)
requirements = [
    {"id": "REQ-001", "title": "회원가입", "description": "사용자는 회원가입을 할 수 있다.",
     "priority": "High", "acceptance": "아이디 중복 시 가입이 거부된다."},
    {"id": "REQ-002", "title": "로그인", "description": "사용자는 적절히 로그인할 수 있어야 한다.",
     "priority": "High", "acceptance": ""},  # 수용기준 누락
    {"id": "REQ-002", "title": "게시글 등록", "description": "사용자는 게시글을 등록할 수 있다.",
     "priority": "Medium", "acceptance": "제목이 비어 있으면 등록이 거부된다."},  # ID 중복
    {"id": "REQ-004", "title": "게시글 삭제는 관리자만 가능",
     "description": "게시글은 누구나 삭제할 수 있다.",
     "priority": "Medium", "acceptance": "삭제 시 확인 메시지가 표시된다."},  # 제목-설명 상충
]

VAGUE_WORDS = ["적절히", "가능한 한", "빠르게", "알아서", "적당히"]


def check_duplicate_ids(reqs):
    seen, dups = set(), []
    for r in reqs:
        if r["id"] in seen:
            dups.append(r["id"])
        seen.add(r["id"])
    return dups


def check_missing_fields(reqs):
    missing = []
    for r in reqs:
        empty_fields = [k for k in ("title", "description", "acceptance") if not r[k].strip()]
        if empty_fields:
            missing.append((r["id"], empty_fields))
    return missing


def check_vague_expressions(reqs):
    vague = []
    for r in reqs:
        found = [w for w in VAGUE_WORDS if w in r["description"]]
        if found:
            vague.append((r["id"], found))
    return vague


def check_possible_conflicts(reqs):
    conflicts = []
    for r in reqs:
        if "관리자만" in r["title"] and "누구나" in r["description"]:
            conflicts.append((r["id"], "제목은 '관리자만 가능'이라 하지만 설명은 '누구나 가능'으로 되어 있음"))
    return conflicts


if __name__ == "__main__":
    print("=== 요구사항 정의서 자동 점검 ===")

    dups = check_duplicate_ids(requirements)
    print(f"\n[중복 ID] {len(dups)}건")
    for d in dups:
        print(f"  - {d}")

    missing = check_missing_fields(requirements)
    print(f"\n[누락 항목] {len(missing)}건")
    for req_id, fields in missing:
        print(f"  - {req_id} : {', '.join(fields)} 항목이 비어 있음")

    vague = check_vague_expressions(requirements)
    print(f"\n[모호한 표현] {len(vague)}건")
    for req_id, words in vague:
        print(f"  - {req_id} : {', '.join(words)}")

    conflicts = check_possible_conflicts(requirements)
    print(f"\n[상충 가능성] {len(conflicts)}건")
    for req_id, reason in conflicts:
        print(f"  - {req_id} : {reason}")
