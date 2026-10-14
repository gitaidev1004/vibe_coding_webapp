"""
ch06/04_security/access_control_bypass_demo.py
권한 우회(Broken Access Control / IDOR) 취약점을 재현하고,
소유자 검증 로직을 추가하여 방어하는 방법을 확인하는 예제입니다.
5.7(4)에서 구현한 게시글 수정 API의 작성자 확인 로직과 동일한 원리이다.
"""

posts = {
    1: {"post_id": 1, "member_id": 100, "title": "홍길동의 글"},
    2: {"post_id": 2, "member_id": 200, "title": "김철수의 글"},
}


def vulnerable_update_post(post_id: int, requester_id: int, new_title: str) -> str:
    """[취약한 코드] 게시글 존재 여부만 확인하고, 요청자가 작성자인지는 확인하지 않는다."""
    post = posts.get(post_id)
    if post is None:
        return "404 Not Found"
    post["title"] = new_title  # 누구나 다른 사람의 글을 수정할 수 있다!
    return f"200 OK: '{new_title}'로 수정됨"


def safe_update_post(post_id: int, requester_id: int, new_title: str) -> str:
    """[안전한 코드] 요청자가 게시글의 실제 작성자인지 확인한 뒤에만 수정을 허용한다."""
    post = posts.get(post_id)
    if post is None:
        return "404 Not Found"
    if post["member_id"] != requester_id:
        return "403 Forbidden: 작성자만 수정할 수 있습니다."
    post["title"] = new_title
    return f"200 OK: '{new_title}'로 수정됨"


if __name__ == "__main__":
    print("=== 시나리오: member_id=100(홍길동)이 로그인한 상태에서 ===")
    print("    다른 사람(member_id=200, 김철수)의 게시글(post_id=2)을 수정 시도")

    print("\n[취약한 코드]")
    result = vulnerable_update_post(post_id=2, requester_id=100, new_title="해킹당했습니다")
    print(f"  결과: {result}")
    print(f"  실제 데이터: {posts[2]}  <- 소유자가 아닌데도 수정에 성공!")

    # 원상 복구 후 안전한 버전으로 재시도
    posts[2]["title"] = "김철수의 글"
    print("\n[안전한 코드]")
    result = safe_update_post(post_id=2, requester_id=100, new_title="해킹 시도")
    print(f"  결과: {result}")
    print(f"  실제 데이터: {posts[2]}  <- 소유자 검증에 의해 원본이 보호됨")
