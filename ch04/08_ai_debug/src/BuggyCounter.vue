<script setup>
/**
 * ch04/08_ai_debug/src/BuggyCounter.vue
 * [버그가 있는 코드] reactive()로 만든 객체를 구조분해할당하면
 * 각 속성이 반응형을 잃어버려 값이 바뀌어도 화면이 갱신되지 않는다.
 */
import { reactive } from "vue";

const state = reactive({ count: 0 });
// 버그: 구조분해하는 순간 count는 그 시점의 '값'만 복사되어
// 이후 state.count가 바뀌어도 아래 count 변수는 영향을 받지 않는다.
const { count } = state;

function increment() {
  state.count++; // 원본은 바뀌지만, 화면은 count(복사본)를 보고 있다.
}
</script>

<template>
  <div>
    <p>count: {{ count }}</p>
    <button @click="increment">+1</button>
  </div>
</template>
