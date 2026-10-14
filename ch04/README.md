# ch04. AI와 UI/UX 및 Vue.js 프론트엔드 개발 - 실습 소스 코드

## 폴더 구성

```
ch04/
├── 04_javascript/           4.4절 - JavaScript 기본 문법 예제
│   ├── js_basics_demo.js     변수·자료형·함수·객체·배열
│   ├── async_demo.js         Promise·async/await·Fetch API
│   └── json_demo.js          JSON 구조·직렬화·역직렬화
├── vue_project/               4.5~4.7절 - Vue.js 3 + Vite 실전 프로젝트
│   ├── src/
│   │   ├── main.js, App.vue
│   │   ├── api/http.js        공통 fetch 래퍼
│   │   ├── stores/auth.js     Pinia 로그인 상태 스토어
│   │   ├── router/index.js    Vue Router + Navigation Guard
│   │   ├── components/
│   │   │   ├── AppButton.vue      Props/Emits/Slots 예제
│   │   │   └── ReactiveCounter.vue ref/reactive/computed/watch 예제
│   │   └── views/
│   │       ├── LoginView.vue
│   │       ├── BoardListView.vue   목록/검색/페이징
│   │       ├── BoardDetailView.vue 상세 조회
│   │       └── BoardFormView.vue   등록/수정/유효성 검사
│   └── tests/                 Vitest + @vue/test-utils 컴포넌트 테스트
├── 08_ai_debug/               4.8절 - AI 디버깅 예제(버그 재현 -> 수정)
│   ├── src/BuggyCounter.vue   구조분해로 반응성이 깨지는 버그
│   ├── src/FixedCounter.vue   toRefs()로 수정한 버전
│   └── tests/counter_bug.spec.js  버그 재현과 수정 확인을 모두 테스트로 검증
└── practice/                  장 마무리 실습 템플릿
    ├── screen_list_template.csv
    ├── storyboard_template.md
    └── practice_checklist.md
```

## 실행 방법

### JavaScript 기본 예제
```bash
cd ch04/04_javascript
node js_basics_demo.js
node async_demo.js
node json_demo.js
```

### Vue 프로젝트 (개발 서버 실행)
```bash
cd ch04/vue_project
npm install
npm run dev
```
브라우저에서 http://localhost:5173 으로 접속하면 화면을 확인할 수 있습니다.
(단, /api 로 시작하는 API는 3장의 백엔드 예제 서버가 함께 실행되어야 정상적으로
데이터를 불러옵니다. 백엔드 없이도 `npm run build`, `npx vitest run` 은 정상 동작합니다.)

### Vue 프로젝트 빌드 검증
```bash
cd ch04/vue_project
npm run build
```

### Vue 컴포넌트 테스트
```bash
cd ch04/vue_project
npx vitest run
```

### AI 디버깅 예제(버그 재현/수정 테스트)
```bash
cd ch04/08_ai_debug
npm install
npx vitest run
```

## 요구 사항
- Node.js 18 이상
