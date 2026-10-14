/**
 * ch04/vue_project/src/api/http.js
 * 백엔드 API 호출을 위한 공통 fetch 래퍼.
 * 3장에서 설계한 REST API(예: /api/posts)를 호출하는 데 사용한다.
 */
const BASE_URL = "/api";

async function request(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    const error = new Error(body.detail || `요청 실패 (status: ${response.status})`);
    error.status = response.status;
    throw error;
  }

  if (response.status === 204) return null;
  return response.json();
}

export const http = {
  get: (path) => request(path),
  post: (path, data) => request(path, { method: "POST", body: JSON.stringify(data) }),
  put: (path, data) => request(path, { method: "PUT", body: JSON.stringify(data) }),
  delete: (path) => request(path, { method: "DELETE" }),
};
