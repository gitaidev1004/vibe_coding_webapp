/**
 * ch04/04_javascript/js_basics_demo.js
 * JavaScript 기본 문법(변수, 자료형, 함수, 객체, 배열) 데모
 */

// ① 변수: let은 재할당 가능, const는 재할당 불가능한 변수를 선언한다.
let count = 1;
count = 2;
const MAX_COUNT = 10;

// ② 자료형: 문자열, 숫자, 불리언, undefined, null, 객체 등이 있다.
const username = "홍길동";       // string
const age = 25;                  // number
const isActive = true;           // boolean
const nickname = undefined;      // undefined (값이 할당되지 않음)
const profileImage = null;       // null (의도적으로 비어 있음)

// ③ 함수: 함수 선언식과 화살표 함수(Arrow Function)로 정의할 수 있다.
function add(a, b) {
  return a + b;
}
const multiply = (a, b) => a * b;

// ④ 객체: 관련된 데이터를 key-value 쌍으로 묶어서 표현한다.
const member = {
  username: "hong_gildong",
  email: "hong@example.com",
  introduce() {
    return `안녕하세요, ${this.username}입니다.`;
  },
};

// ⑤ 배열: 여러 값을 순서대로 담는 자료구조이며, map/filter 같은 메서드를 제공한다.
const posts = [
  { id: 1, title: "첫 게시글", viewCount: 10 },
  { id: 2, title: "두 번째 게시글", viewCount: 3 },
  { id: 3, title: "공지사항", viewCount: 25 },
];
const titles = posts.map((p) => p.title);
const popularPosts = posts.filter((p) => p.viewCount >= 10);

console.log("=== 변수/자료형 ===");
console.log("count:", count, ", MAX_COUNT:", MAX_COUNT);
console.log("username:", username, typeof username);
console.log("age:", age, typeof age);
console.log("isActive:", isActive, typeof isActive);
console.log("nickname:", nickname, typeof nickname);
console.log("profileImage:", profileImage, typeof profileImage);

console.log("\n=== 함수 ===");
console.log("add(2, 3) =", add(2, 3));
console.log("multiply(2, 3) =", multiply(2, 3));

console.log("\n=== 객체 ===");
console.log(member.introduce());

console.log("\n=== 배열 ===");
console.log("titles:", titles);
console.log("popularPosts:", popularPosts);
