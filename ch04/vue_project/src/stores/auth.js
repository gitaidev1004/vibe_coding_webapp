/**
 * ch04/vue_project/src/stores/auth.js
 * Pinia를 이용한 로그인 상태 전역 관리 스토어.
 */
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { http } from "../api/http";

export const useAuthStore = defineStore("auth", () => {
  const username = ref(null);

  const isLoggedIn = computed(() => username.value !== null);

  async function login(loginId, password) {
    const result = await http.post("/auth/login", { username: loginId, password });
    username.value = result.username;
    return result;
  }

  function logout() {
    username.value = null;
  }

  return { username, isLoggedIn, login, logout };
});
