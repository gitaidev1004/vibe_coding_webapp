/**
 * ch04/04_javascript/async_demo.js
 * Promise, async/await, Fetch API 개념 데모
 * (실제 네트워크 요청 대신, 지연을 흉내 낸 mockFetch로 개념을 확인한다)
 */

// ① Promise: 비동기 작업의 결과(성공/실패)를 나중에 처리할 수 있게 해주는 객체
function delay(ms, value) {
  return new Promise((resolve) => {
    setTimeout(() => resolve(value), ms);
  });
}

// 실제 서버 대신 사용할 가짜 fetch 함수 (Fetch API와 동일한 사용 방식을 흉내 낸다)
function mockFetchPosts() {
  return delay(50, [
    { id: 1, title: "첫 게시글" },
    { id: 2, title: "두 번째 게시글" },
  ]);
}

console.log("=== ① Promise의 then/catch 방식 ===");
mockFetchPosts()
  .then((posts) => {
    console.log("(then) 게시글 목록:", posts.map((p) => p.title));
  })
  .catch((err) => {
    console.error("오류 발생:", err);
  })
  .finally(runAsyncAwaitDemo);

// ② async/await: Promise를 동기 코드처럼 읽기 쉽게 작성하는 문법
async function runAsyncAwaitDemo() {
  console.log("\n=== ② async/await 방식 ===");
  try {
    const posts = await mockFetchPosts();
    console.log("(await) 게시글 목록:", posts.map((p) => p.title));
  } catch (err) {
    console.error("오류 발생:", err);
  }
  runFetchApiDemo();
}

// ③ Fetch API: 브라우저/Node에 내장된 HTTP 요청 함수. 실제 서버가 있다면
// fetch("/api/posts")처럼 호출하지만, 여기서는 동작 방식만 의사 코드로 보여준다.
async function runFetchApiDemo() {
  console.log("\n=== ③ Fetch API 사용 예시(의사 코드) ===");
  console.log(`
async function loadPosts() {
  const response = await fetch("/api/posts");
  if (!response.ok) {
    throw new Error("게시글을 불러오지 못했습니다.");
  }
  const posts = await response.json();
  return posts;
}
  `.trim());
}
