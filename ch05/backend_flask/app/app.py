"""
ch05/backend_flask/app/app.py
Flask 애플리케이션 진입점. Blueprint를 등록하고 초기 데이터를 시드하며,
공통 오류(ApiError)를 JSON 응답으로 변환하는 핸들러를 등록한다.
"""
from flask import Flask, jsonify

from app import database
from app.errors import ApiError
from app.seed import run_seed
from app.deps import close_db
from app.routers.auth_routes import auth_bp
from app.routers.member_routes import member_bp
from app.routers.board_routes import board_bp
from app.routers.admin_routes import admin_bp


def create_app():
    # database.engine/SessionLocal을 함수 호출 시점에 참조해야, 테스트 환경에서
    # 임시 데이터베이스로 교체(monkeypatch)했을 때도 정확히 반영된다.
    database.Base.metadata.create_all(bind=database.engine)
    with database.SessionLocal() as db:
        run_seed(db)

    app = Flask(__name__)
    app.register_blueprint(auth_bp)
    app.register_blueprint(member_bp)
    app.register_blueprint(board_bp)
    app.register_blueprint(admin_bp)

    @app.get("/")
    def root():
        return jsonify({"message": "실습 프로젝트 Flask 백엔드"})

    @app.errorhandler(ApiError)
    def handle_api_error(error):
        return jsonify({"detail": error.message}), error.status_code

    app.teardown_appcontext(close_db)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
