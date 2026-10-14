"""
ch05/backend_flask/tests/test_access_control.py
역할·권한 기반 접근제어(RBAC)가 의도대로 동작하는지 검증한다.
"""
from tests.conftest import signup_and_login, admin_login


def test_general_member_cannot_access_admin_api(client):
    headers = signup_and_login(client)
    res = client.get("/api/members", headers=headers)
    assert res.status_code == 403
    assert "접근 권한이 없습니다" in res.get_json()["detail"]


def test_admin_can_access_admin_api(client):
    headers = admin_login(client)
    res = client.get("/api/members", headers=headers)
    assert res.status_code == 200


def test_no_token_returns_401(client):
    res = client.get("/api/members")
    assert res.status_code == 401


def test_access_denied_is_logged(client):
    headers = signup_and_login(client)
    client.get("/api/members", headers=headers)

    admin_headers = admin_login(client)
    logs = client.get("/api/admin/logs", headers=admin_headers).get_json()
    denied_logs = [log for log in logs if log["action"] == "ACCESS_DENIED"]
    assert len(denied_logs) >= 1
    assert "MEMBER_MANAGE" in denied_logs[0]["target"]


def test_granting_permission_allows_access(client):
    admin_headers = admin_login(client)

    role_res = client.post("/api/admin/roles", json={"role_name": "STAFF", "description": "운영진"},
                            headers=admin_headers)
    assert role_res.status_code == 201

    perm_res = client.post("/api/admin/permissions", json={
        "role_id": role_res.get_json()["role_id"], "function_code": "MEMBER_MANAGE",
        "can_read": True, "can_write": False,
    }, headers=admin_headers)
    assert perm_res.status_code == 204
