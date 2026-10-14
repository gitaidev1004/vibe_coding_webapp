"""
ch05/backend_fastapi/tests/test_access_control.py
역할·권한 기반 접근제어(RBAC)가 의도대로 동작하는지 검증한다.
"""
from tests.conftest import signup_and_login, admin_login


def test_general_member_cannot_access_admin_api(client):
    headers = signup_and_login(client)
    res = client.get("/api/members", headers=headers)
    assert res.status_code == 403
    assert "접근 권한이 없습니다" in res.json()["detail"]


def test_admin_can_access_admin_api(client):
    headers = admin_login(client)
    res = client.get("/api/members", headers=headers)
    assert res.status_code == 200


def test_no_token_returns_401(client):
    res = client.get("/api/members")
    assert res.status_code == 401


def test_access_denied_is_logged(client):
    headers = signup_and_login(client)
    client.get("/api/members", headers=headers)  # 403 예상, 동시에 로그 기록

    admin_headers = admin_login(client)
    logs = client.get("/api/admin/logs", headers=admin_headers).json()
    denied_logs = [log for log in logs if log["action"] == "ACCESS_DENIED"]
    assert len(denied_logs) >= 1
    assert "MEMBER_MANAGE" in denied_logs[0]["target"]


def test_granting_permission_allows_access(client):
    admin_headers = admin_login(client)

    # 새 역할(운영진)을 만들고 MEMBER_MANAGE 읽기 권한을 부여한다.
    role_res = client.post("/api/admin/roles", json={"role_name": "STAFF", "description": "운영진"},
                            headers=admin_headers)
    assert role_res.status_code == 201

    perm_res = client.post("/api/admin/permissions", json={
        "role_id": role_res.json()["role_id"], "function_code": "MEMBER_MANAGE",
        "can_read": True, "can_write": False,
    }, headers=admin_headers)
    assert perm_res.status_code == 204
