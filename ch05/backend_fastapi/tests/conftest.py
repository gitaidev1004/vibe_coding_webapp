"""
ch05/backend_fastapi/tests/conftest.py
테스트마다 독립된 임시 SQLite 데이터베이스로 초기화하는 공용 fixture.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app import database
from app.seed import run_seed
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    monkeypatch.setattr(database, "engine", engine)
    monkeypatch.setattr(database, "SessionLocal", TestingSessionLocal)

    import app.deps as deps_module
    from app.database import get_db as original_get_db

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    Base.metadata.create_all(bind=engine)
    with TestingSessionLocal() as db:
        run_seed(db)

    app.dependency_overrides[original_get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def signup_and_login(client, username="hong_gildong", password="pass1234"):
    client.post("/api/members", json={
        "username": username, "password": password, "email": f"{username}@example.com",
    })
    res = client.post("/api/auth/login", json={"username": username, "password": password})
    token = res.json()["token"]
    return {"Authorization": f"Bearer {token}"}


def admin_login(client):
    res = client.post("/api/auth/login", json={"username": "admin", "password": "admin1234!"})
    token = res.json()["token"]
    return {"Authorization": f"Bearer {token}"}
