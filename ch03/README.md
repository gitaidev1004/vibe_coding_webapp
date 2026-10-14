# ch03. AI와 시스템 분석·설계 및 데이터 모델링 - 실습 소스 코드

이 폴더는 교재 3장에서 다루는 예제 코드와 실습 자료를 담고 있습니다.

## 폴더 구성

```
ch03/
├── 04_springboot/          3.4절 - Spring Boot Layered MVC 구조 예제 (Java/Maven)
│   ├── pom.xml
│   └── src/main/java/com/example/webapp/
│       ├── WebappApplication.java
│       ├── entity/Member.java
│       ├── repository/MemberRepository.java
│       ├── service/MemberService.java
│       └── controller/MemberController.java
├── 05_fastapi/              3.5절 - FastAPI Layered Architecture 구조 예제 (Python)
│   ├── models.py, schemas.py, repository.py, service.py, router.py
│   ├── database.py, main.py
│   └── test_member_api.py   실행 검증용 테스트
├── 06_flask/                 3.6절 - Flask Layered Architecture 구조 예제 (Python)
│   ├── models.py, repository.py, service.py, routes.py, database.py, app.py
│   └── test_member_api.py   실행 검증용 테스트
├── 07_data_modeling/        3.7절 - 정규화 예제
│   └── normalization_example.py
├── 08_erd/                   3.8절 - 프로젝트 ERD
│   ├── schema.sql            PostgreSQL 기준 전체 ERD DDL
│   └── build_erd_db.py       SQLite로 스키마·관계 검증
├── 09_api/                   3.9절 - API 설계
│   ├── openapi_spec.yaml     게시글 API OpenAPI 명세 예시
│   └── validate_openapi.py   CRUD·응답코드 완전성 점검
└── 10_practice/              장 마무리 실습 템플릿
    ├── usecase_spec_template.md
    ├── erd_data_dictionary_template.csv
    ├── api_spec_template.md
    └── practice_checklist.md
```

## 실행 방법

### FastAPI 예제
```bash
cd ch03/05_fastapi
pip install -r requirements.txt
python test_member_api.py          # 서버 없이 바로 테스트
# 또는 실제 서버로 띄우려면:
uvicorn main:app --reload
```

### Flask 예제
```bash
cd ch03/06_flask
pip install -r requirements.txt
python test_member_api.py          # 서버 없이 바로 테스트
# 또는 실제 서버로 띄우려면:
python app.py
```

### Spring Boot 예제
Maven과 인터넷 연결(Maven Central 접근)이 가능한 환경에서:
```bash
cd ch03/04_springboot
mvn spring-boot:run
```
> 이 책의 실습 환경은 외부 저장소 접근이 제한되어 있어 Maven 빌드를 직접
> 실행하지는 못했지만, 코드는 Spring Boot 3.x / Java 17 표준 문법을 따릅니다.
> 실제 Maven/Gradle 프로젝트에 그대로 옮겨 사용할 수 있습니다.

### 정규화 예제
```bash
cd ch03/07_data_modeling
python normalization_example.py
```

### ERD 검증
```bash
cd ch03/08_erd
python build_erd_db.py
```

### API 명세 점검
```bash
cd ch03/09_api
pip install pyyaml
python validate_openapi.py
```

## 요구 사항
- Python 3.10 이상
- (Spring Boot 예제를 직접 실행하려면) JDK 17 이상, Maven 3.9 이상
