"""
ch03/05_fastapi/main.py
FastAPI 애플리케이션 진입점. Router를 연결하고 데이터베이스 테이블을 생성한다.
"""
from fastapi import FastAPI

from database import engine
from models import Base
from router import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="실습 프로젝트 API (FastAPI)")
app.include_router(router)


@app.get("/")
def root():
    return {"message": "FastAPI Layered Architecture 예제"}
