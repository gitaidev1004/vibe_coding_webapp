"""
ch03/05_fastapi/test_member_api.py
main.py로 만든 FastAPI 앱이 실제로 정상 동작하는지 확인하는 테스트 코드입니다.
TestClient를 사용하면 서버를 직접 띄우지 않고도 API를 호출해 볼 수 있습니다.
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_signup_and_list():
    # 1) 회원가입 요청
    response = client.post(
        "/api/members",
        json={"username": "hong_gildong", "password": "pass1234", "email": "hong@example.com"},
    )
    print("[POST /api/members] status:", response.status_code)
    print("응답 본문:", response.json())
    assert response.status_code == 201

    # 2) 같은 아이디로 재가입 시도 -> 실패해야 함
    response2 = client.post(
        "/api/members",
        json={"username": "hong_gildong", "password": "pass5678", "email": "hong2@example.com"},
    )
    print("\n[중복 가입 시도] status:", response2.status_code)
    print("응답 본문:", response2.json())
    assert response2.status_code == 400

    # 3) 회원 목록 조회
    response3 = client.get("/api/members")
    print("\n[GET /api/members] status:", response3.status_code)
    print("응답 본문:", response3.json())
    assert response3.status_code == 200
    assert len(response3.json()) == 1


if __name__ == "__main__":
    test_signup_and_list()
    print("\n모든 테스트를 통과했습니다.")
