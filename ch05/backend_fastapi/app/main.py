"""
ch05/backend_fastapi/app/main.py
FastAPI 애플리케이션 진입점. 라우터를 연결하고 초기 데이터를 시드한다.
"""
from fastapi import FastAPI
from app.database import engine, Base, SessionLocal
from app.seed import run_seed
from app.routers import auth_router, member_router, board_router, admin_router, comment_router

Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    run_seed(db)

app = FastAPI(title="실습 프로젝트 API (FastAPI)")
app.include_router(auth_router.router)
app.include_router(member_router.router)
app.include_router(board_router.router)
app.include_router(admin_router.router)
app.include_router(comment_router.router)


@app.get("/")
def root():
    return {"message": "실습 프로젝트 FastAPI 백엔드"}
