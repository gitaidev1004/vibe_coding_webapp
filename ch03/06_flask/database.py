"""
ch03/06_flask/database.py
데이터베이스 연결 설정. 실습에서는 SQLite를 사용하며,
실제 프로젝트에서는 SQLALCHEMY_DATABASE_URL만 교체하면 된다.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./ch03_flask.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
