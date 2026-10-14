"""
ch01/01_environment/check_db_env.py
RDBMS(관계형 데이터베이스) 연동 확인용 스크립트
- 별도의 서버 설치 없이 파이썬 내장 sqlite3로 CRUD 동작을 즉시 확인합니다.
- 실제 프로젝트에서는 PostgreSQL, MySQL 등으로 접속 정보만 교체하면 됩니다.
"""
import sqlite3
from datetime import datetime

DB_PATH = "ch01_check.db"


def check_db_env():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS member")
    cur.execute(
        """
        CREATE TABLE member (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    cur.execute(
        "INSERT INTO member (username, created_at) VALUES (?, ?)",
        ("hong_gildong", datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()

    cur.execute("SELECT id, username, created_at FROM member")
    rows = cur.fetchall()

    print("=== RDBMS 연동 확인 ===")
    print(f"SQLite 버전 : {sqlite3.sqlite_version}")
    print("member 테이블 조회 결과:")
    for row in rows:
        print(f"  id={row[0]}, username={row[1]}, created_at={row[2]}")

    conn.close()


if __name__ == "__main__":
    check_db_env()
