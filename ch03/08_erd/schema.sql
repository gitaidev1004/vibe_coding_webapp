-- ch03/08_erd/schema.sql
-- 실습 프로젝트 전체 ERD DDL (PostgreSQL 기준)
-- 사용자 / 역할 / 권한 / 메뉴 / 기능 / 게시판 / 게시글 / 로그

-- 1. 역할(role)
CREATE TABLE role (
    role_id     SERIAL PRIMARY KEY,
    role_name   VARCHAR(30) NOT NULL UNIQUE,
    description VARCHAR(200)
);

-- 2. 사용자(member) - role을 참조(N:1)
CREATE TABLE member (
    member_id   SERIAL PRIMARY KEY,
    username    VARCHAR(50)  NOT NULL UNIQUE,
    password    VARCHAR(200) NOT NULL,
    email       VARCHAR(100) NOT NULL,
    role_id     INTEGER NOT NULL REFERENCES role(role_id),
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 3. 메뉴(menu) - 자기 자신을 참조하는 계층 구조(상위 메뉴)
CREATE TABLE menu (
    menu_id     SERIAL PRIMARY KEY,
    menu_name   VARCHAR(50) NOT NULL,
    url         VARCHAR(100),
    parent_id   INTEGER REFERENCES menu(menu_id),
    sort_order  INTEGER NOT NULL DEFAULT 0
);

-- 4. 기능(function) - menu를 참조(N:1)
CREATE TABLE function (
    function_id   SERIAL PRIMARY KEY,
    function_name VARCHAR(50) NOT NULL,
    menu_id       INTEGER NOT NULL REFERENCES menu(menu_id),
    description   VARCHAR(200)
);

-- 5. 권한(permission) - role과 function의 N:M 관계를 표현하는 연결 테이블
CREATE TABLE permission (
    role_id     INTEGER NOT NULL REFERENCES role(role_id),
    function_id INTEGER NOT NULL REFERENCES function(function_id),
    can_read    BOOLEAN NOT NULL DEFAULT FALSE,
    can_write   BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (role_id, function_id)
);

-- 6. 게시판(board)
CREATE TABLE board (
    board_id    SERIAL PRIMARY KEY,
    board_name  VARCHAR(50) NOT NULL,
    description VARCHAR(200)
);

-- 7. 게시글(post) - board(N:1), member(N:1) 참조
CREATE TABLE post (
    post_id     SERIAL PRIMARY KEY,
    board_id    INTEGER NOT NULL REFERENCES board(board_id),
    member_id   INTEGER NOT NULL REFERENCES member(member_id),
    title       VARCHAR(200) NOT NULL,
    content     TEXT NOT NULL,
    view_count  INTEGER NOT NULL DEFAULT 0,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP
);

-- 8. 로그(log) - member(N:1) 참조
CREATE TABLE log (
    log_id      SERIAL PRIMARY KEY,
    member_id   INTEGER REFERENCES member(member_id),
    action      VARCHAR(50) NOT NULL,
    target      VARCHAR(200),
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
