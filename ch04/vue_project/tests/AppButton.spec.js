/**
 * ch04/vue_project/tests/AppButton.spec.js
 * AppButton 컴포넌트의 Props, Emits, Slots가 의도대로 동작하는지 검증한다.
 */
import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import AppButton from "../src/components/AppButton.vue";

describe("AppButton", () => {
  it("slot으로 전달한 내용을 버튼 텍스트로 렌더링한다", () => {
    const wrapper = mount(AppButton, {
      slots: { default: "저장하기" },
    });
    expect(wrapper.text()).toBe("저장하기");
  });

  it("variant prop에 따라 클래스가 붙는다", () => {
    const wrapper = mount(AppButton, {
      props: { variant: "danger" },
    });
    expect(wrapper.classes()).toContain("danger");
  });

  it("클릭하면 click 이벤트를 emit한다", async () => {
    const wrapper = mount(AppButton);
    await wrapper.trigger("click");
    expect(wrapper.emitted("click")).toBeTruthy();
  });

  it("disabled 상태에서는 click 이벤트를 emit하지 않는다", async () => {
    const wrapper = mount(AppButton, { props: { disabled: true } });
    await wrapper.trigger("click");
    expect(wrapper.emitted("click")).toBeFalsy();
  });
});
