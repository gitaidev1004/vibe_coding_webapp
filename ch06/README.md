# ch06. 테스트·보안·배포와 AI 시대의 개발자 - 실습 소스 코드

## 폴더 구성

```
ch06/
├── 01_testing/                6.1절 - 경계값·예외 테스트 예제
│   └── boundary_value_test_demo.py
├── 04_security/                6.4절 - 웹 애플리케이션 보안 취약점/방어 예제
│   ├── sql_injection_demo.py   SQL Injection 취약/방어 비교
│   ├── xss_demo.py             XSS 취약/방어 비교
│   ├── csrf_demo.py            CSRF 토큰 검증
│   └── access_control_bypass_demo.py  권한 우회(IDOR) 취약/방어 비교
├── 05_deployment/              6.5절 - Git, Build, 배포 예제
│   ├── git_workflow_demo.sh    Repository/Commit/Branch/Merge 실습 스크립트
│   ├── Dockerfile.fastapi / .flask / .springboot / .vue
│   ├── docker-compose.yml      프런트+백엔드+DB 통합 실행 설정
│   ├── nginx.conf              정적 파일 서빙 + API 리버스 프록시
│   └── deploy.sh               빌드->테스트->배포->헬스체크 예제 스크립트
├── 06_operations/              6.6절 - 운영과 유지보수 예제
│   └── health_check.py         배포된 서버 상태 점검 스크립트
└── practice/                   장 마무리 실습
    └── final_checklist_template.md
```

## 실행 방법

### 경계값/예외 테스트
```bash
cd ch06/01_testing
python boundary_value_test_demo.py
```

### 보안 취약점/방어 데모
```bash
cd ch06/04_security
python sql_injection_demo.py
python xss_demo.py
python csrf_demo.py
python access_control_bypass_demo.py
```

### Git 워크플로 실습
```bash
bash ch06/05_deployment/git_workflow_demo.sh
```

### 헬스 체크 (5장 백엔드를 먼저 구동한 뒤 실행)
```bash
# 터미널 1
cd ch05/backend_fastapi && uvicorn app.main:app --port 8000
# 터미널 2
python ch06/06_operations/health_check.py
```

### Docker Compose로 전체 구동 (Docker 환경 필요)
```bash
cd ch06/05_deployment
docker compose up -d --build
```

## 요구 사항
- Python 3.10 이상
- Git
- (선택) Docker, Docker Compose - 컨테이너 배포 실습 시
