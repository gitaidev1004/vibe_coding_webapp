<script setup>
/**
 * ch04/08_ai_debug/src/FixedCounter.vue
 * [AI가 제안한 수정 코드] toRefs()로 각 속성을 반응형 참조(ref)로
 * 변환한 뒤 구조분해하면, 원본과의 연결이 유지되어 정상적으로 갱신된다.
 */
import { reactive, toRefs } from "vue";

const state = reactive({ count: 0 });
const { count } = toRefs(state); // count는 이제 반응형 ref이다.

function increment() {
  state.count++;
}
</script>

<template>
  <div>
    <p>count: {{ count }}</p>
    <button @click="increment">+1</button>
  </div>
</template>
