# 4장 실습 체크리스트 - Vue.js 3로 로그인·회원관리·게시판 화면 구현하기

## 진행 순서
- [ ] 1. screen_list_template.csv 형식으로 이 장에서 구현할 화면 목록을 정리한다.
- [ ] 2. 각 화면에 대해 storyboard_template.md 형식으로 스토리보드를 작성한다.
- [ ] 3. vue_project를 참고하여 로그인 화면(LoginView.vue)을 완성하고 Pinia 스토어와
      연동한다.
- [ ] 4. 회원가입 화면을 LoginView.vue 구조를 참고하여 직접 작성해 본다.
- [ ] 5. BoardListView.vue / BoardDetailView.vue / BoardFormView.vue 를 참고하여
      게시판 목록·상세·등록·수정 화면을 완성한다.
- [ ] 6. npm run build 로 전체 프로젝트가 오류 없이 빌드되는지 확인한다.
- [ ] 7. npx vitest run 으로 작성한 컴포넌트의 테스트가 모두 통과하는지 확인한다.

## 완료 기준
- 로그인하지 않은 상태로 글쓰기(/posts/new)에 접근하면 로그인 화면으로 이동한다.
  (Navigation Guard 동작 확인)
- 게시글 목록에서 검색과 페이징이 정상적으로 동작한다.
- 게시글 등록/수정 시 제목이 비어 있으면 저장되지 않고 오류 메시지가 표시된다.
- `npm run build` 와 `npx vitest run` 이 모두 오류 없이 통과한다.
