# ch02. AI와 프로젝트 기획 및 요구사항 분석 - 실습 소스 코드

이 폴더는 교재 2장에서 다루는 예제 코드와 실습 자료를 담고 있습니다.
모든 코드는 별도의 외부 서버나 API 키 없이 그대로 실행할 수 있도록 작성되었습니다.

## 폴더 구성

```
ch02/
├── 01_prd/                          2.3절 - PRD 작성 예제
│   ├── prd_template.md              PRD 작성 템플릿
│   └── generate_prd_draft.py        AI 응답(JSON)을 PRD 마크다운으로 변환
├── 02_requirements/                 2.4절, 2.6절 - 요구사항 정의/검증 예제
│   ├── requirements_template.csv    요구사항 정의서 템플릿
│   ├── generate_requirements_from_ai.py   AI 응답(JSON)을 요구사항 CSV로 변환
│   └── validate_requirements.py     중복/누락/모호/상충 자동 점검 스크립트
├── 03_rtm/                          2.5절 - 요구사항 추적표(RTM) 예제
│   ├── rtm_template.csv             RTM 템플릿
│   └── build_rtm.py                 요구사항 + 매핑정보 -> RTM 생성 스크립트
├── 04_prioritization/                2.1절 - 기능 우선순위 산정 예제
│   └── score_features.py            RICE 기법 기능 우선순위 계산 스크립트
└── 05_practice/                     장 마무리 실습
    ├── prd_template.md
    ├── requirements_template.csv
    └── practice_checklist.md        실습 진행 체크리스트
```

## 실행 방법

### 1) PRD 초안 생성
```bash
cd ch02/01_prd
python generate_prd_draft.py
```
실행하면 같은 폴더에 `prd_draft_output.md` 파일이 생성됩니다.

### 2) AI 응답으로 요구사항 정의서(CSV) 생성
```bash
cd ch02/02_requirements
python generate_requirements_from_ai.py
```
실행하면 같은 폴더에 `requirements_generated.csv` 파일이 생성됩니다.

### 3) 요구사항 정의서 자동 점검
```bash
cd ch02/02_requirements
python validate_requirements.py
```

### 4) 요구사항 추적표(RTM) 생성
```bash
cd ch02/03_rtm
python build_rtm.py
```
실행하면 같은 폴더에 `rtm_generated.csv` 파일이 생성됩니다.

### 5) 기능 우선순위(RICE 기법) 산정
```bash
cd ch02/04_prioritization
python score_features.py
```

### 6) 장 마무리 실습
`05_practice/practice_checklist.md`의 순서에 따라 `prd_template.md`와
`requirements_template.csv`를 직접 작성해 완성합니다.

## 요구 사항
- Python 3.10 이상 (표준 라이브러리만 사용하므로 별도 설치 불필요)
