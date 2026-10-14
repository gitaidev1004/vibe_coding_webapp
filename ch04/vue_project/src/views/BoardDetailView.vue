<script setup>
/**
 * ch04/vue_project/src/views/BoardDetailView.vue
 * 게시글 상세 화면 - 4.7(2) 상세: 데이터 조회, 상세 표시
 */
import { ref, onMounted } from "vue";
import { http } from "../api/http";

const props = defineProps({ id: { type: [String, Number], required: true } });

const post = ref(null);
const loadError = ref("");

async function fetchPost() {
  try {
    post.value = await http.get(`/posts/${props.id}`);
  } catch (err) {
    loadError.value = "게시글을 찾을 수 없습니다.";
  }
}

onMounted(fetchPost);
</script>

<template>
  <div class="board-detail">
    <p v-if="loadError" class="error">{{ loadError }}</p>
    <article v-else-if="post">
      <h2>{{ post.title }}</h2>
      <p class="meta">조회수 {{ post.viewCount }}</p>
      <p class="content">{{ post.content }}</p>
      <RouterLink :to="`/posts/${post.id}/edit`">수정</RouterLink>
      <RouterLink to="/posts">목록으로</RouterLink>
    </article>
  </div>
</template>
