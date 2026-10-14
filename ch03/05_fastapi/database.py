"""
ch03/05_fastapi/database.py
데이터베이스 연결 설정. 실습에서는 별도 서버 설치가 필요 없는 SQLite를 사용한다.
실제 프로젝트에서는 SQLALCHEMY_DATABASE_URL만 PostgreSQL 접속 정보로 교체하면 된다.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./ch03_fastapi.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
