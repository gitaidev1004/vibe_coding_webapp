<script setup>
/**
 * ch04/vue_project/src/App.vue
 * 최상위 컴포넌트. 상단 네비게이션과 라우트별 화면(RouterView)을 배치한다.
 */
import { useAuthStore } from "./stores/auth";

const authStore = useAuthStore();
</script>

<template>
  <header class="app-header">
    <RouterLink to="/posts">게시판</RouterLink>
    <span v-if="authStore.isLoggedIn">{{ authStore.username }}님</span>
    <RouterLink v-else to="/login">로그인</RouterLink>
  </header>
  <main>
    <RouterView />
  </main>
</template>
