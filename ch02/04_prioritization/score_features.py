"""
ch02/04_prioritization/score_features.py
RICE 기법(Reach, Impact, Confidence, Effort)으로 기능 우선순위 점수를 계산하는 예제입니다.
점수 = (Reach * Impact * Confidence) / Effort
- Reach: 영향을 받는 사용자 규모(예: 월간 예상 사용자 수)
- Impact: 사용자에게 미치는 영향 크기(0.25=낮음, 0.5=보통, 1=높음, 2=매우 높음)
- Confidence: 추정에 대한 확신도(0.5=낮음, 0.8=보통, 1.0=높음)
- Effort: 개발에 필요한 예상 작업량(사람-주 단위)
"""

features = [
    {"name": "회원가입/로그인", "reach": 500, "impact": 2, "confidence": 1.0, "effort": 2},
    {"name": "게시판 CRUD", "reach": 500, "impact": 2, "confidence": 1.0, "effort": 3},
    {"name": "게시글 검색", "reach": 300, "impact": 1, "confidence": 0.8, "effort": 1},
    {"name": "댓글 기능", "reach": 200, "impact": 0.5, "confidence": 0.8, "effort": 2},
    {"name": "실시간 알림", "reach": 150, "impact": 1, "confidence": 0.5, "effort": 4},
]


def rice_score(f):
    return round((f["reach"] * f["impact"] * f["confidence"]) / f["effort"], 1)


def moscow_grade(score, ranks):
    """점수 순위에 따라 MoSCoW 등급을 자동으로 매긴다."""
    position = ranks.index(score)
    if position == 0:
        return "Must"
    elif position <= 1:
        return "Should"
    elif position <= 3:
        return "Could"
    else:
        return "Won't"


if __name__ == "__main__":
    for f in features:
        f["score"] = rice_score(f)

    features_sorted = sorted(features, key=lambda f: f["score"], reverse=True)
    ranks = [f["score"] for f in features_sorted]

    print("=== RICE 기법 기능 우선순위 산정 결과 ===")
    print(f"{'기능명':16s} {'점수':>6s}  {'등급':6s}")
    for f in features_sorted:
        grade = moscow_grade(f["score"], ranks)
        print(f"{f['name']:16s} {f['score']:>6.1f}  {grade:6s}")
