# 5장 실습 체크리스트 - 하나의 애플리케이션을 Spring Boot / FastAPI / Flask로 각각 구현하고 비교하기

## 진행 순서
- [ ] 1. backend_fastapi를 pip install -r requirements.txt 후 pytest로 전체 테스트를 통과시킨다.
- [ ] 2. backend_flask를 pip install -r requirements.txt 후 pytest로 전체 테스트를 통과시킨다.
- [ ] 3. backend_springboot를 로컬 Maven 환경에서 mvn spring-boot:run 으로 직접 실행해 보고,
      curl 또는 Postman으로 회원가입 -> 로그인 -> 게시글 등록 -> 접근제어(403) 흐름을 확인한다.
- [ ] 4. 세 프레임워크의 동일한 계층(Entity/Model, Repository, Service, Controller/Router)
      코드를 나란히 비교하며 comparison_template.md를 작성한다.
- [ ] 5. 4장에서 만든 Vue 프론트엔드의 http.js baseURL을 세 백엔드로 각각 바꾸어 실행해 보고,
      동일한 화면이 세 백엔드 모두와 정상적으로 연동되는지 확인한다.

## 완료 기준
- 세 프레임워크 모두에서 "일반 회원이 관리자 API에 접근하면 403이 반환되고,
  ACCESS_DENIED 로그가 남는다"는 동일한 시나리오가 성립한다.
- comparison_template.md의 모든 항목이 채워져 있다.
