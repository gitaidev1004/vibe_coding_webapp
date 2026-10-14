/**
 * ch04/vue_project/tests/ReactiveCounter.spec.js
 * ref, computed, watch가 서로 맞물려 동작하는지 검증한다.
 */
import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import ReactiveCounter from "../src/components/ReactiveCounter.vue";

describe("ReactiveCounter", () => {
  it("버튼을 누르면 count와 computed(doubled) 값이 함께 갱신된다", async () => {
    const wrapper = mount(ReactiveCounter);
    expect(wrapper.text()).toContain("count: 0");
    expect(wrapper.text()).toContain("doubled: 0");

    await wrapper.find("button").trigger("click");
    await wrapper.find("button").trigger("click");

    expect(wrapper.text()).toContain("count: 2");
    expect(wrapper.text()).toContain("doubled: 4");
  });

  it("watch가 count 변화 이력을 기록한다", async () => {
    const wrapper = mount(ReactiveCounter);
    await wrapper.find("button").trigger("click");
    const items = wrapper.findAll("li");
    expect(items).toHaveLength(1);
    expect(items[0].text()).toBe("0 -> 1");
  });
});
