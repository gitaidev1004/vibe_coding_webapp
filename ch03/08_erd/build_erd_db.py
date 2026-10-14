"""
ch03/08_erd/build_erd_db.py
schema.sql(PostgreSQL 기준)과 동일한 구조를 SQLite로 재현하여
실제로 테이블이 생성되고, 관계(외래키)가 올바르게 동작하는지 검증하는 스크립트입니다.
- SERIAL -> INTEGER PRIMARY KEY AUTOINCREMENT
- BOOLEAN, TIMESTAMP 등은 SQLite에서 동일한 이름으로 사용 가능(타입 어피니티)
"""
import sqlite3

DB_PATH = "ch03_erd_check.db"

SCHEMA_SQLITE = """
PRAGMA foreign_keys = ON;

CREATE TABLE role (
    role_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name   VARCHAR(30) NOT NULL UNIQUE,
    description VARCHAR(200)
);

CREATE TABLE member (
    member_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    username    VARCHAR(50)  NOT NULL UNIQUE,
    password    VARCHAR(200) NOT NULL,
    email       VARCHAR(100) NOT NULL,
    role_id     INTEGER NOT NULL REFERENCES role(role_id),
    is_active   BOOLEAN NOT NULL DEFAULT 1,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE menu (
    menu_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    menu_name   VARCHAR(50) NOT NULL,
    url         VARCHAR(100),
    parent_id   INTEGER REFERENCES menu(menu_id),
    sort_order  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE function (
    function_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    function_name VARCHAR(50) NOT NULL,
    menu_id       INTEGER NOT NULL REFERENCES menu(menu_id),
    description   VARCHAR(200)
);

CREATE TABLE permission (
    role_id     INTEGER NOT NULL REFERENCES role(role_id),
    function_id INTEGER NOT NULL REFERENCES function(function_id),
    can_read    BOOLEAN NOT NULL DEFAULT 0,
    can_write   BOOLEAN NOT NULL DEFAULT 0,
    PRIMARY KEY (role_id, function_id)
);

CREATE TABLE board (
    board_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    board_name  VARCHAR(50) NOT NULL,
    description VARCHAR(200)
);

CREATE TABLE post (
    post_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    board_id    INTEGER NOT NULL REFERENCES board(board_id),
    member_id   INTEGER NOT NULL REFERENCES member(member_id),
    title       VARCHAR(200) NOT NULL,
    content     TEXT NOT NULL,
    view_count  INTEGER NOT NULL DEFAULT 0,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP
);

CREATE TABLE log (
    log_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id   INTEGER REFERENCES member(member_id),
    action      VARCHAR(50) NOT NULL,
    target      VARCHAR(200),
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def build_schema(conn):
    conn.executescript(SCHEMA_SQLITE)


def insert_sample_data(conn):
    cur = conn.cursor()
    cur.execute("INSERT INTO role (role_name, description) VALUES ('ADMIN', '관리자')")
    cur.execute("INSERT INTO role (role_name, description) VALUES ('MEMBER', '일반회원')")

    cur.execute(
        "INSERT INTO member (username, password, email, role_id) VALUES (?, ?, ?, ?)",
        ("admin01", "hashed_pw", "admin@example.com", 1),
    )
    cur.execute(
        "INSERT INTO member (username, password, email, role_id) VALUES (?, ?, ?, ?)",
        ("hong_gildong", "hashed_pw", "hong@example.com", 2),
    )

    cur.execute("INSERT INTO menu (menu_name, url, sort_order) VALUES ('게시판 관리', '/board', 1)")
    cur.execute(
        "INSERT INTO function (function_name, menu_id, description) VALUES (?, ?, ?)",
        ("게시글 삭제", 1, "게시글을 삭제하는 기능"),
    )
    cur.execute(
        "INSERT INTO permission (role_id, function_id, can_read, can_write) VALUES (1, 1, 1, 1)"
    )

    cur.execute("INSERT INTO board (board_name, description) VALUES ('공지사항', '공지 게시판')")
    cur.execute(
        "INSERT INTO post (board_id, member_id, title, content) VALUES (?, ?, ?, ?)",
        (1, 2, "첫 공지입니다", "환영합니다."),
    )
    cur.execute(
        "INSERT INTO log (member_id, action, target) VALUES (?, ?, ?)",
        (2, "CREATE_POST", "post_id=1"),
    )
    conn.commit()


def verify(conn):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT p.title, b.board_name, m.username, r.role_name
        FROM post p
        JOIN board b ON p.board_id = b.board_id
        JOIN member m ON p.member_id = m.member_id
        JOIN role r ON m.role_id = r.role_id
        """
    )
    return cur.fetchall()


if __name__ == "__main__":
    import os
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    build_schema(conn)
    insert_sample_data(conn)

    print("=== ERD 스키마 생성 및 관계 검증 ===")
    print("8개 테이블(role, member, menu, function, permission, board, post, log) 생성 완료")
    print()
    print("게시글 - 게시판 - 작성자 - 역할 JOIN 조회 결과:")
    for row in verify(conn):
        print(f"  제목='{row[0]}', 게시판='{row[1]}', 작성자='{row[2]}', 역할='{row[3]}'")

    conn.close()
    os.remove(DB_PATH)
