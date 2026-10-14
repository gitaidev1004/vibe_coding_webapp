"""
ch06/04_security/sql_injection_demo.py
SQL Injection 취약점이 실제로 어떻게 동작하는지, 그리고 파라미터 바인딩으로
이를 방어하는 방법을 SQLite로 직접 실행하며 확인하는 예제입니다.

경고: vulnerable_login()의 코드는 취약점을 보여주기 위한 예시이며,
실제 서비스 코드에 절대 이런 방식으로 작성해서는 안 됩니다.
"""
import sqlite3


def setup_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE member (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            is_admin INTEGER DEFAULT 0
        )
    """)
    conn.execute("INSERT INTO member VALUES (1, 'admin', 's3cr3t-hash', 1)")
    conn.execute("INSERT INTO member VALUES (2, 'hong_gildong', 'pass1234-hash', 0)")
    conn.commit()
    return conn


def vulnerable_login(conn, username, password):
    """[취약한 코드] 사용자 입력을 SQL 문자열에 그대로 이어붙인다."""
    query = f"SELECT * FROM member WHERE username = '{username}' AND password = '{password}'"
    print(f"  실행되는 SQL: {query}")
    cur = conn.execute(query)
    return cur.fetchone()


def safe_login(conn, username, password):
    """[안전한 코드] 파라미터 바인딩(placeholder)을 사용해 입력값을 데이터로만 취급한다."""
    query = "SELECT * FROM member WHERE username = ? AND password = ?"
    cur = conn.execute(query, (username, password))
    return cur.fetchone()


if __name__ == "__main__":
    conn = setup_db()

    print("=== 정상적인 로그인 시도 ===")
    result = vulnerable_login(conn, "hong_gildong", "pass1234-hash")
    print("  결과:", result)

    print("\n=== SQL Injection 공격 시도 (취약한 코드) ===")
    malicious_username = "' OR '1'='1' -- "
    result = vulnerable_login(conn, malicious_username, "아무거나")
    print(f"  결과: {result}  <- 비밀번호 없이도 관리자 계정 정보가 조회됨!")

    print("\n=== 동일한 공격을 안전한 코드로 시도 ===")
    result = safe_login(conn, malicious_username, "아무거나")
    print(f"  결과: {result}  <- 파라미터 바인딩 덕분에 공격 문자열이 그대로 값으로 취급되어 조회 실패")

    conn.close()
