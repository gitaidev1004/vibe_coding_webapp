"""
ch05/backend_flask/tests/test_member.py
회원가입, 로그인, 내 정보 조회 기능을 검증한다.
"""
from tests.conftest import signup_and_login, admin_login


def test_signup_success(client):
    res = client.post("/api/members", json={
        "username": "hong_gildong", "password": "pass1234", "email": "hong@example.com",
    })
    assert res.status_code == 201
    assert res.get_json()["role_name"] == "MEMBER"


def test_signup_duplicate_username(client):
    payload = {"username": "hong_gildong", "password": "pass1234", "email": "hong@example.com"}
    client.post("/api/members", json=payload)
    res = client.post("/api/members", json=payload)
    assert res.status_code == 400


def test_login_success_and_me(client):
    headers = signup_and_login(client)
    res = client.get("/api/members/me", headers=headers)
    assert res.status_code == 200
    assert res.get_json()["username"] == "hong_gildong"


def test_login_wrong_password(client):
    client.post("/api/members", json={
        "username": "hong_gildong", "password": "pass1234", "email": "hong@example.com",
    })
    res = client.post("/api/auth/login", json={"username": "hong_gildong", "password": "wrong"})
    assert res.status_code == 401


def test_deactivated_member_cannot_login(client):
    signup_and_login(client)
    admin_headers = admin_login(client)

    members = client.get("/api/members", headers=admin_headers).get_json()
    target = next(m for m in members if m["username"] == "hong_gildong")

    client.put(f"/api/members/{target['member_id']}", json={"is_active": False}, headers=admin_headers)

    res = client.post("/api/auth/login", json={"username": "hong_gildong", "password": "pass1234"})
    assert res.status_code == 403
