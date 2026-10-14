/**
 * ch04/vue_project/src/router/index.js
 * Vue Router 설정. 로그인 여부에 따라 접근을 제어하는 Navigation Guard를 포함한다.
 */
import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";

import LoginView from "../views/LoginView.vue";
import BoardListView from "../views/BoardListView.vue";
import BoardDetailView from "../views/BoardDetailView.vue";
import BoardFormView from "../views/BoardFormView.vue";

const routes = [
  { path: "/", redirect: "/posts" },
  { path: "/login", name: "login", component: LoginView },
  { path: "/posts", name: "board-list", component: BoardListView },
  { path: "/posts/new", name: "board-new", component: BoardFormView, meta: { requiresAuth: true } },
  { path: "/posts/:id", name: "board-detail", component: BoardDetailView, props: true },
  { path: "/posts/:id/edit", name: "board-edit", component: BoardFormView, props: true, meta: { requiresAuth: true } },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard: 로그인이 필요한 라우트는 로그인 여부를 확인한다.
router.beforeEach((to) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    return { name: "login" };
  }
  return true;
});
