<script setup>
/**
 * ch04/vue_project/src/views/LoginView.vue
 * 로그인 화면. Composition API의 ref와 async/await를 이용해 폼을 처리한다.
 */
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const username = ref("");
const password = ref("");
const errorMessage = ref("");
const isSubmitting = ref(false);

const authStore = useAuthStore();
const router = useRouter();

async function handleSubmit() {
  errorMessage.value = "";
  if (!username.value || !password.value) {
    errorMessage.value = "아이디와 비밀번호를 모두 입력해 주세요.";
    return;
  }

  isSubmitting.value = true;
  try {
    await authStore.login(username.value, password.value);
    router.push({ name: "board-list" });
  } catch (err) {
    errorMessage.value = err.message;
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <form class="login-form" @submit.prevent="handleSubmit">
    <h2>로그인</h2>
    <input v-model="username" type="text" placeholder="아이디" />
    <input v-model="password" type="password" placeholder="비밀번호" />
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <button type="submit" :disabled="isSubmitting">
      {{ isSubmitting ? "로그인 중..." : "로그인" }}
    </button>
  </form>
</template>
