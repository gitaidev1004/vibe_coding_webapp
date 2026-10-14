<script setup>
/**
 * ch04/vue_project/src/components/AppButton.vue
 * Props, Emits, Slots를 모두 보여주는 재사용 가능한 버튼 컴포넌트.
 */
const props = defineProps({
  variant: {
    type: String,
    default: "primary", // 'primary' | 'danger'
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["click"]);

function handleClick(event) {
  if (props.disabled) return;
  emit("click", event);
}
</script>

<template>
  <button
    class="app-button"
    :class="variant"
    :disabled="disabled"
    @click="handleClick"
  >
    <slot>버튼</slot>
  </button>
</template>
