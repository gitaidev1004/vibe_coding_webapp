/**
 * ch04/vue_project/tests/BoardListView.spec.js
 * 게시글 목록의 검색·페이징 로직을 mock API로 검증한다.
 */
import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createRouter, createWebHistory } from "vue-router";

vi.mock("../src/api/http", () => ({
  http: { get: vi.fn(), delete: vi.fn() },
}));
import { http } from "../src/api/http";
import BoardListView from "../src/views/BoardListView.vue";

const samplePosts = Array.from({ length: 7 }, (_, i) => ({
  id: i + 1,
  title: i === 0 ? "공지: 환영합니다" : `게시글 ${i + 1}`,
  viewCount: i,
}));

async function setupWrapper() {
  const router = createRouter({
    history: createWebHistory(),
    routes: [
      { path: "/posts", name: "board-list", component: { template: "<div/>" } },
      { path: "/posts/new", name: "board-new", component: { template: "<div/>" } },
      { path: "/posts/:id", name: "board-detail", component: { template: "<div/>" } },
    ],
  });
  router.push("/posts");
  await router.isReady();
  const wrapper = mount(BoardListView, { global: { plugins: [router] } });
  await new Promise((resolve) => setTimeout(resolve, 0));
  return wrapper;
}

describe("BoardListView", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    http.get.mockResolvedValue(samplePosts);
  });

  it("한 페이지에는 5건만 표시된다 (전체 7건)", async () => {
    const wrapper = await setupWrapper();
    expect(wrapper.findAll("li")).toHaveLength(5);
    expect(wrapper.text()).toContain("1 / 2");
  });

  it("검색어로 제목을 필터링하면 결과와 페이지 수가 갱신된다", async () => {
    const wrapper = await setupWrapper();
    await wrapper.find(".search-bar input").setValue("공지");
    await wrapper.find(".search-bar button").trigger("click");

    expect(wrapper.findAll("li")).toHaveLength(1);
    expect(wrapper.text()).toContain("공지: 환영합니다");
  });
});
