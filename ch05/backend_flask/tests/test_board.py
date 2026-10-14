"""
ch05/backend_flask/tests/test_board.py
게시글 등록/조회/검색/페이징/수정/삭제 기능을 검증한다.
"""
from tests.conftest import signup_and_login


def test_create_and_get_post(client):
    headers = signup_and_login(client)
    res = client.post("/api/posts", json={"title": "첫 게시글", "content": "반갑습니다"}, headers=headers)
    assert res.status_code == 201
    post_id = res.get_json()["post_id"]

    detail = client.get(f"/api/posts/{post_id}")
    assert detail.status_code == 200
    assert detail.get_json()["view_count"] == 1


def test_view_count_increments_on_each_view(client):
    headers = signup_and_login(client)
    post_id = client.post("/api/posts", json={"title": "제목", "content": "내용"}, headers=headers).get_json()["post_id"]

    client.get(f"/api/posts/{post_id}")
    client.get(f"/api/posts/{post_id}")
    res = client.get(f"/api/posts/{post_id}")
    assert res.get_json()["view_count"] == 3


def test_search_and_paging(client):
    headers = signup_and_login(client)
    for i in range(7):
        title = "공지 게시글" if i == 0 else f"일반 게시글 {i}"
        client.post("/api/posts", json={"title": title, "content": "내용"}, headers=headers)

    page1 = client.get("/api/posts?page=1&page_size=5").get_json()
    assert len(page1["items"]) == 5
    assert page1["total"] == 7

    searched = client.get("/api/posts?keyword=공지").get_json()
    assert searched["total"] == 1


def test_update_post_by_non_author_forbidden(client):
    headers1 = signup_and_login(client, "hong_gildong")
    headers2 = signup_and_login(client, "kim_cheolsu")

    post_id = client.post("/api/posts", json={"title": "제목", "content": "내용"}, headers=headers1).get_json()["post_id"]

    res = client.put(f"/api/posts/{post_id}", json={"title": "수정", "content": "수정 내용"}, headers=headers2)
    assert res.status_code == 403


def test_delete_post_by_author_success(client):
    headers = signup_and_login(client)
    post_id = client.post("/api/posts", json={"title": "제목", "content": "내용"}, headers=headers).get_json()["post_id"]

    res = client.delete(f"/api/posts/{post_id}", headers=headers)
    assert res.status_code == 204
    assert client.get(f"/api/posts/{post_id}").status_code == 404
