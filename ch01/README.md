# ch01. AI 시대의 웹 애플리케이션 개발 - 실습 소스 코드

이 폴더는 교재 1장에서 다루는 예제 코드와 실습 자료를 담고 있습니다.
모든 코드는 별도의 외부 서버나 API 키 없이 그대로 실행할 수 있도록 작성되었습니다.

## 폴더 구성

```
ch01/
├── 01_environment/                 1.5절 - 개발 환경(기술 스택) 점검 스크립트
│   ├── check_python_env.py         Python(FastAPI/Flask) 환경 확인
│   ├── check_node_env.js           Node.js(Vue.js 3/Vite) 환경 확인
│   ├── check_db_env.py             RDBMS(SQLite 예시) 연동 확인
│   └── requirements.txt            Python 패키지 목록
├── 02_prompt_context/              1.2절 - Prompt/Context, 구조화된 출력 예제
│   └── parse_structured_output.py
├── 04_ai_coding/                   1.4절 - AI Coding 예제
│   └── email_validator.py
└── 05_practice/                    장 마무리 실습
    └── project_plan_template.md    프로젝트 아이디어/개발계획 작성 템플릿
```

## 실행 방법

### 1) Python 환경 확인
```bash
cd ch01/01_environment
python check_python_env.py
```
필요한 패키지를 설치하려면:
```bash
pip install -r requirements.txt
```

### 2) Node.js 환경 확인
```bash
cd ch01/01_environment
node check_node_env.js
```

### 3) RDBMS(데이터베이스) 연동 확인
```bash
cd ch01/01_environment
python check_db_env.py
```
실행하면 현재 폴더에 `ch01_check.db`(SQLite 파일)가 생성됩니다.

### 4) 구조화된 출력(JSON) 파싱 예제
```bash
cd ch01/02_prompt_context
python parse_structured_output.py
```

### 5) AI 코드 생성 예제(이메일 검증)
```bash
cd ch01/04_ai_coding
python email_validator.py
```

### 6) 장 마무리 실습
`05_practice/project_plan_template.md` 파일을 열어 본인의 프로젝트 아이디어를
직접 작성해 봅니다. 작성한 내용을 AI에게 제시하고 보완 의견을 받아보세요.

## 요구 사항
- Python 3.10 이상
- Node.js 18 이상
