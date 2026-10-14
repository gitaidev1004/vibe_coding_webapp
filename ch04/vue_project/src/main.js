/**
 * ch04/vue_project/src/main.js
 * 애플리케이션 진입점. Pinia와 Vue Router를 등록한다.
 */
import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import { router } from "./router";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.mount("#app");
