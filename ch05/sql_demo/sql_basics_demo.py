"""
ch05/sql_demo/sql_basics_demo.py
SELECT, INSERT, UPDATE, DELETE, JOIN 다섯 가지 기본 SQL 명령을
SQLite로 실제 실행하며 확인하는 예제입니다.
"""
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()

cur.executescript("""
CREATE TABLE role (role_id INTEGER PRIMARY KEY, role_name TEXT);
CREATE TABLE member (member_id INTEGER PRIMARY KEY, username TEXT, role_id INTEGER);
""")

# INSERT: 새 행을 추가한다.
cur.execute("INSERT INTO role (role_id, role_name) VALUES (1, 'ADMIN')")
cur.execute("INSERT INTO role (role_id, role_name) VALUES (2, 'MEMBER')")
cur.execute("INSERT INTO member (username, role_id) VALUES ('admin', 1)")
cur.execute("INSERT INTO member (username, role_id) VALUES ('hong_gildong', 2)")
conn.commit()

# SELECT: 데이터를 조회한다.
print("=== SELECT ===")
for row in cur.execute("SELECT member_id, username FROM member"):
    print(row)

# UPDATE: 기존 데이터를 수정한다.
cur.execute("UPDATE member SET username = ? WHERE username = ?", ("hong_gd", "hong_gildong"))
conn.commit()
print("\n=== UPDATE 후 ===")
for row in cur.execute("SELECT member_id, username FROM member"):
    print(row)

# JOIN: 두 테이블을 연결하여 조회한다.
print("\n=== JOIN (member + role) ===")
for row in cur.execute("""
    SELECT m.username, r.role_name
    FROM member m JOIN role r ON m.role_id = r.role_id
"""):
    print(row)

# DELETE: 데이터를 삭제한다.
cur.execute("DELETE FROM member WHERE username = ?", ("hong_gd",))
conn.commit()
print("\n=== DELETE 후 ===")
for row in cur.execute("SELECT member_id, username FROM member"):
    print(row)

conn.close()
