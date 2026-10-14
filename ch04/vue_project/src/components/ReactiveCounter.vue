<script setup>
/**
 * ch04/vue_project/src/components/ReactiveCounter.vue
 * ref, reactive, computed, watch를 모두 보여주는 예제 컴포넌트.
 */
import { ref, reactive, computed, watch } from "vue";

// ref: 하나의 원시값을 반응형으로 다룬다.
const count = ref(0);

// reactive: 객체 전체를 반응형으로 다룬다.
const state = reactive({ history: [] });

// computed: count 값을 바탕으로 자동 계산되는 파생 값.
const doubled = computed(() => count.value * 2);

// watch: count 값이 바뀔 때마다 부가 작업(이력 기록)을 수행한다.
watch(count, (newValue, oldValue) => {
  state.history.push(`${oldValue} -> ${newValue}`);
});

function increment() {
  count.value++;
}
</script>

<template>
  <div>
    <p>count: {{ count }} / doubled: {{ doubled }}</p>
    <button @click="increment">+1</button>
    <ul>
      <li v-for="(log, idx) in state.history" :key="idx">{{ log }}</li>
    </ul>
  </div>
</template>
