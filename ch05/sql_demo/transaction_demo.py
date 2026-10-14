"""
ch05/sql_demo/transaction_demo.py
Transaction, Commit, Rollback 개념을 SQLAlchemy 세션으로 확인하는 예제입니다.
"""
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Member(Base):
    __tablename__ = "member"
    member_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)


engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)


def demo_commit():
    db = SessionLocal()
    db.add(Member(username="hong_gildong"))
    db.commit()  # 여기까지의 변경 사항을 데이터베이스에 확정 반영한다.
    print("[커밋 후] 회원 수:", db.query(Member).count())
    db.close()


def demo_rollback():
    db = SessionLocal()
    try:
        db.add(Member(username="kim_cheolsu"))
        db.flush()  # DB에 임시 반영(아직 커밋 전)
        # 의도적으로 같은 아이디를 한 번 더 추가하여 UNIQUE 제약 위반을 발생시킨다.
        db.add(Member(username="kim_cheolsu"))
        db.commit()
    except Exception as e:
        print(f"[오류 발생] {type(e).__name__} -> 롤백을 수행합니다.")
        db.rollback()  # 트랜잭션 시작 시점 상태로 모든 변경을 되돌린다.
    finally:
        db.close()

    db2 = SessionLocal()
    print("[롤백 후] 'kim_cheolsu' 회원 존재 여부:",
          db2.query(Member).filter_by(username="kim_cheolsu").first() is not None)
    db2.close()


if __name__ == "__main__":
    print("=== Transaction과 Commit ===")
    demo_commit()

    print("\n=== Transaction과 Rollback ===")
    demo_rollback()
