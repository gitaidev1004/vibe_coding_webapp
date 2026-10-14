/**
 * ch04/vue_project/tests/BoardFormView.spec.js
 * 게시글 등록 폼의 유효성 검사와 저장 로직을 mock API로 검증한다.
 */
import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createRouter, createWebHistory } from "vue-router";

vi.mock("../src/api/http", () => ({
  http: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
  },
}));
import { http } from "../src/api/http";
import BoardFormView from "../src/views/BoardFormView.vue";

async function setupWrapper(props = {}) {
  const router = createRouter({
    history: createWebHistory(),
    routes: [
      { path: "/posts/:id", name: "board-detail", component: { template: "<div/>" } },
      { path: "/posts/new", name: "board-new", component: { template: "<div/>" } },
    ],
  });
  router.push("/posts/new");
  await router.isReady();
  return mount(BoardFormView, { props, global: { plugins: [router] } });
}

describe("BoardFormView", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("제목이 비어 있으면 저장되지 않고 오류 메시지를 표시한다", async () => {
    const wrapper = await setupWrapper();
    await wrapper.find("textarea").setValue("내용입니다");
    await wrapper.find("form").trigger("submit.prevent");

    expect(http.post).not.toHaveBeenCalled();
    expect(wrapper.text()).toContain("제목을 입력해 주세요.");
  });

  it("제목과 내용을 모두 입력하면 저장 API가 호출된다", async () => {
    http.post.mockResolvedValue({ id: 1 });
    const wrapper = await setupWrapper();

    await wrapper.find("input").setValue("첫 게시글");
    await wrapper.find("textarea").setValue("반갑습니다");
    await wrapper.find("form").trigger("submit.prevent");
    await new Promise((resolve) => setTimeout(resolve, 0));

    expect(http.post).toHaveBeenCalledWith("/posts", {
      title: "첫 게시글",
      content: "반갑습니다",
    });
  });
});
