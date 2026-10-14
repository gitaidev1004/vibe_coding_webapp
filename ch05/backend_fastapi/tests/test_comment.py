"""
ch05/backend_fastapi/tests/test_comment.py
5.9절 AI Agent 실습 예제로 추가한 댓글 기능을 검증한다.
"""
from tests.conftest import signup_and_login


def test_add_and_get_comments(client):
    headers = signup_and_login(client)
    post_id = client.post("/api/posts", json={"title": "제목", "content": "내용"}, headers=headers).json()["post_id"]

    res = client.post(f"/api/posts/{post_id}/comments", json={"content": "좋은 글이네요"}, headers=headers)
    assert res.status_code == 201

    comments = client.get(f"/api/posts/{post_id}/comments").json()
    assert len(comments) == 1
    assert comments[0]["content"] == "좋은 글이네요"


def test_empty_comment_rejected(client):
    headers = signup_and_login(client)
    post_id = client.post("/api/posts", json={"title": "제목", "content": "내용"}, headers=headers).json()["post_id"]

    res = client.post(f"/api/posts/{post_id}/comments", json={"content": "   "}, headers=headers)
    assert res.status_code in (400, 422)


def test_delete_comment_by_non_author_forbidden(client):
    headers1 = signup_and_login(client, "hong_gildong")
    headers2 = signup_and_login(client, "kim_cheolsu")
    post_id = client.post("/api/posts", json={"title": "제목", "content": "내용"}, headers=headers1).json()["post_id"]
    comment_id = client.post(f"/api/posts/{post_id}/comments", json={"content": "댓글"},
                              headers=headers1).json()["comment_id"]

    res = client.delete(f"/api/posts/{post_id}/comments/{comment_id}", headers=headers2)
    assert res.status_code == 403
