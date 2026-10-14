"""
ch03/06_flask/app.py
Flask 애플리케이션 진입점. Blueprint를 등록하고 데이터베이스 테이블을 생성한다.
"""
from flask import Flask

from database import engine
from models import Base
from routes import member_bp

Base.metadata.create_all(bind=engine)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(member_bp)

    @app.get("/")
    def root():
        return {"message": "Flask Layered Architecture 예제"}

    @app.teardown_appcontext
    def close_db(exception=None):
        from flask import g
        db = g.pop("db", None)
        if db is not None:
            db.close()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
