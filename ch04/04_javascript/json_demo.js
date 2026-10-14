/**
 * ch04/04_javascript/json_demo.js
 * JSON 구조, 직렬화(stringify), 역직렬화(parse) 데모
 */

// ① JSON 구조: key는 반드시 큰따옴표로 감싼 문자열이어야 한다.
const jsonText = `
{
  "id": 1,
  "title": "첫 게시글",
  "tags": ["공지", "중요"],
  "author": { "username": "hong_gildong" }
}
`;

// ③ 역직렬화(Deserialization): JSON 문자열 -> 자바스크립트 객체
const post = JSON.parse(jsonText);
console.log("=== JSON.parse() 결과 ===");
console.log("title:", post.title);
console.log("author:", post.author.username);
console.log("tags:", post.tags.join(", "));

// ② 직렬화(Serialization): 자바스크립트 객체 -> JSON 문자열
// 서버에 데이터를 보낼 때(fetch의 body)는 반드시 이 과정을 거쳐야 한다.
const newPost = {
  title: "새 게시글",
  content: "반갑습니다",
  createdAt: new Date("2026-03-01"),
};
const serialized = JSON.stringify(newPost);
console.log("\n=== JSON.stringify() 결과 ===");
console.log(serialized);

// 들여쓰기를 적용하면 로그나 파일로 저장할 때 사람이 읽기 좋다.
console.log("\n=== 들여쓰기 적용(JSON.stringify(obj, null, 2)) ===");
console.log(JSON.stringify(newPost, null, 2));
