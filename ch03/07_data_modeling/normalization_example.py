"""
ch03/07_data_modeling/normalization_example.py
비정규화된 테이블 예시를 정규화 과정(1NF -> 2NF -> 3NF)에 따라
분리해 나가는 과정을 코드로 보여주는 예제입니다.
"""

# 정규화 이전: 하나의 행에 여러 게시글 정보가 반복되고(1NF 위반),
# 작성자 이름이 작성자 ID에만 종속되며(2NF 위반),
# 작성자 소속 부서가 작성자 이름에 종속되는(3NF 위반) 문제가 섞여 있다.
unnormalized_table = [
    {
        "post_id": 1,
        "writer_id": "u01",
        "writer_name": "홍길동",
        "writer_dept": "개발팀",
        "post_titles": ["첫 게시글", "두 번째 게시글"],  # 1NF 위반: 반복 그룹
    },
]


def to_first_normal_form(rows):
    """1NF: 반복 그룹을 제거하고 하나의 셀에는 하나의 값만 담도록 행을 분리한다."""
    result = []
    for row in rows:
        for title in row["post_titles"]:
            result.append({
                "post_id": row["post_id"],
                "writer_id": row["writer_id"],
                "writer_name": row["writer_name"],
                "writer_dept": row["writer_dept"],
                "post_title": title,
            })
    return result


def to_second_normal_form(rows_1nf):
    """2NF: 기본키(post_id) 전체가 아니라 writer_id에만 종속되는 항목을
    별도의 작성자(writer) 테이블로 분리한다."""
    posts, writers = [], {}
    for row in rows_1nf:
        posts.append({"post_id": row["post_id"], "writer_id": row["writer_id"], "post_title": row["post_title"]})
        writers[row["writer_id"]] = {
            "writer_id": row["writer_id"],
            "writer_name": row["writer_name"],
            "writer_dept": row["writer_dept"],
        }
    return posts, list(writers.values())


def to_third_normal_form(writers):
    """3NF: 기본키가 아닌 writer_dept가 writer_name을 거쳐 간접적으로 결정되는
    이행적 종속을 제거하기 위해 부서(department) 테이블을 분리한다."""
    writers_3nf, departments = [], {}
    for w in writers:
        departments[w["writer_dept"]] = {"dept_name": w["writer_dept"]}
        writers_3nf.append({"writer_id": w["writer_id"], "writer_name": w["writer_name"], "dept_name": w["writer_dept"]})
    return writers_3nf, list(departments.values())


if __name__ == "__main__":
    print("=== 정규화 이전 ===")
    print(unnormalized_table)

    rows_1nf = to_first_normal_form(unnormalized_table)
    print("\n=== 1NF 적용 후 (반복 그룹 제거) ===")
    for r in rows_1nf:
        print(r)

    posts_2nf, writers_2nf = to_second_normal_form(rows_1nf)
    print("\n=== 2NF 적용 후 (posts 테이블) ===")
    for r in posts_2nf:
        print(r)
    print("=== 2NF 적용 후 (writers 테이블) ===")
    for r in writers_2nf:
        print(r)

    writers_3nf, departments_3nf = to_third_normal_form(writers_2nf)
    print("\n=== 3NF 적용 후 (writers 테이블) ===")
    for r in writers_3nf:
        print(r)
    print("=== 3NF 적용 후 (departments 테이블) ===")
    for r in departments_3nf:
        print(r)
