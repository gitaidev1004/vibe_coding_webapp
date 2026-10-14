# ch05. AI와 Backend 및 실전 웹 애플리케이션 구현 - 실습 소스 코드

이 폴더는 동일한 요구사항(회원가입/로그인, 게시판 CRUD, 역할·권한 기반 접근제어,
활동 로그)을 Spring Boot, FastAPI, Flask 세 가지 백엔드 프레임워크로 각각
구현한 실전 프로젝트입니다.

## 폴더 구성

```
ch05/
├── backend_fastapi/     FastAPI 구현 (Router-Service-Repository-Schema-Model)
│   ├── app/
│   │   ├── models/        member.py, board.py, access.py, log.py, comment.py
│   │   ├── schemas/       member.py, board.py, admin.py, comment.py
│   │   ├── repositories/  member/board/admin/log/comment Repository
│   │   ├── services/      member/board/access_control/admin/log/comment Service
│   │   ├── routers/       auth/member/board/admin/comment Router
│   │   ├── deps.py        의존성 주입(DB 세션, 로그인 회원, 접근제어)
│   │   ├── security.py    비밀번호 해시, 토큰 발급/조회
│   │   ├── seed.py        초기 데이터(역할/메뉴/기능/권한/관리자 계정)
│   │   └── main.py
│   ├── tests/             pytest 기반 18개 테스트 (댓글 기능 3개 포함)
│   └── requirements.txt
├── backend_flask/        Flask 구현 (동일한 계층 구조, Blueprint 기반)
│   ├── app/  (fastapi와 동일한 폴더 구조)
│   ├── tests/             pytest 기반 15개 테스트
│   └── requirements.txt
├── backend_springboot/   Spring Boot 구현 (Layered MVC)
│   ├── pom.xml
│   └── src/main/java/com/example/webapp/
│       ├── entity/         Role, Member, Board, Post, Menu, Function, Permission, Log
│       ├── repository/     각 엔터티별 JpaRepository
│       ├── service/        Member/Board/AccessControl/Admin/LogService
│       ├── controller/     Auth/Member/Post/AdminController
│       └── security/       PasswordUtil, TokenStore, CurrentMember 등
└── practice/              장 마무리 실습 템플릿
    ├── comparison_template.md
    └── practice_checklist.md
```

## 공통 기능
- 회원가입 / 로그인(토큰 발급) / 내 정보 조회 / 회원 목록·수정·삭제(관리자)
- 게시글 목록(검색·페이징) / 상세(조회수 증가) / 등록 / 수정(작성자만) / 삭제(작성자·관리자)
- 역할(Role) · 메뉴(Menu) · 기능(Function) · 권한(Permission) 기반 접근제어
  (사용자 확인 -> 역할 확인 -> 권한 확인 -> 기능 실행/접근 차단)
- 모든 로그인, 접근 허용/거부 이력을 log 테이블에 자동 기록

## 실행 방법

### FastAPI
```bash
cd ch05/backend_fastapi
pip install -r requirements.txt
python -m pytest tests/ -v          # 전체 테스트 실행
uvicorn app.main:app --reload       # 개발 서버 실행 (http://localhost:8000)
```

### Flask
```bash
cd ch05/backend_flask
pip install -r requirements.txt
python -m pytest tests/ -v          # 전체 테스트 실행
python -m app.app                   # 개발 서버 실행 (http://localhost:5000)
```

### Spring Boot
Maven과 인터넷 연결(Maven Central 접근)이 가능한 환경에서:
```bash
cd ch05/backend_springboot
mvn spring-boot:run                 # 개발 서버 실행 (http://localhost:8080)
mvn test                            # 테스트 실행
```
> 이 책의 실습 환경은 외부 저장소(Maven Central) 접근이 제한되어 있어 Maven
> 빌드를 직접 실행하지는 못했지만, 코드는 Spring Boot 3.x / Java 17 표준
> 문법을 따르며 FastAPI·Flask 버전과 동일한 시나리오의 테스트를 포함합니다.
> 실제 Maven 프로젝트에 그대로 옮겨 사용할 수 있습니다.

## 기본 계정
시드 데이터로 관리자 계정이 자동 생성됩니다.
- 아이디: `admin` / 비밀번호: `admin1234!` (역할: ADMIN, 모든 기능 읽기/쓰기 권한)
- 회원가입으로 생성되는 계정은 기본적으로 `MEMBER` 역할이 부여되며,
  관리자 전용 API(MEMBER_MANAGE, ROLE_MANAGE, LOG_VIEW)에는 접근할 수 없습니다.

## 요구 사항
- Python 3.10 이상 (FastAPI, Flask)
- JDK 17 이상, Maven 3.9 이상 (Spring Boot 직접 실행 시)
