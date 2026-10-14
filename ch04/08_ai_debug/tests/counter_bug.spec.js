/**
 * ch04/08_ai_debug/tests/counter_bug.spec.js
 * 구조분해로 인한 반응성 상실 버그와, toRefs()를 이용한 수정을
 * 실제 컴포넌트 동작으로 비교 검증한다.
 */
import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import BuggyCounter from "../src/BuggyCounter.vue";
import FixedCounter from "../src/FixedCounter.vue";

describe("BuggyCounter (수정 전)", () => {
  it("[버그 재현] 버튼을 눌러도 화면의 count 표시는 갱신되지 않는다", async () => {
    const wrapper = mount(BuggyCounter);
    expect(wrapper.text()).toContain("count: 0");

    await wrapper.find("button").trigger("click");
    await wrapper.find("button").trigger("click");

    // 내부 상태(state.count)는 2가 되었지만, 화면은 여전히 0을 표시한다.
    expect(wrapper.text()).toContain("count: 0");
  });
});

describe("FixedCounter (AI 수정 후)", () => {
  it("[수정 확인] 버튼을 누르면 화면의 count 표시가 정상적으로 갱신된다", async () => {
    const wrapper = mount(FixedCounter);
    expect(wrapper.text()).toContain("count: 0");

    await wrapper.find("button").trigger("click");
    await wrapper.find("button").trigger("click");

    expect(wrapper.text()).toContain("count: 2");
  });
});
