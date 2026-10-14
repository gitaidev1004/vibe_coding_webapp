<script setup>
/**
 * ch04/vue_project/src/views/BoardListView.vue
 * 게시글 목록 화면 - 4.7(1) 목록: 데이터 조회, 검색, 페이징
 */
import { ref, computed, onMounted } from "vue";
import { http } from "../api/http";

const posts = ref([]);
const keyword = ref("");
const page = ref(1);
const pageSize = 5;
const isLoading = ref(true);
const loadError = ref("");

async function fetchPosts() {
  isLoading.value = true;
  loadError.value = "";
  try {
    posts.value = await http.get("/posts");
  } catch (err) {
    loadError.value = "게시글 목록을 불러오지 못했습니다.";
  } finally {
    isLoading.value = false;
  }
}

onMounted(fetchPosts);

// 검색: 제목에 검색어가 포함된 게시글만 필터링한다.
const filteredPosts = computed(() => {
  if (!keyword.value) return posts.value;
  return posts.value.filter((p) => p.title.includes(keyword.value));
});

// 페이징: 필터링된 결과를 pageSize 단위로 잘라낸다.
const totalPages = computed(() =>
  Math.max(1, Math.ceil(filteredPosts.value.length / pageSize))
);
const pagedPosts = computed(() => {
  const start = (page.value - 1) * pageSize;
  return filteredPosts.value.slice(start, start + pageSize);
});

function search() {
  page.value = 1; // 검색 시 첫 페이지로 리셋
}

async function removePost(id) {
  if (!confirm("정말 삭제하시겠습니까?")) return;
  await http.delete(`/posts/${id}`);
  await fetchPosts();
}

defineExpose({ filteredPosts, pagedPosts, totalPages, search, removePost });
</script>

<template>
  <div class="board-list">
    <h2>게시판</h2>
    <div class="search-bar">
      <input v-model="keyword" placeholder="제목 검색" @keyup.enter="search" />
      <button @click="search">검색</button>
      <RouterLink to="/posts/new">글쓰기</RouterLink>
    </div>

    <p v-if="isLoading">불러오는 중...</p>
    <p v-else-if="loadError" class="error">{{ loadError }}</p>
    <ul v-else>
      <li v-for="post in pagedPosts" :key="post.id">
        <RouterLink :to="`/posts/${post.id}`">{{ post.title }}</RouterLink>
        <span>조회 {{ post.viewCount }}</span>
        <button @click="removePost(post.id)">삭제</button>
      </li>
    </ul>

    <div class="pagination">
      <button :disabled="page <= 1" @click="page--">이전</button>
      <span>{{ page }} / {{ totalPages }}</span>
      <button :disabled="page >= totalPages" @click="page++">다음</button>
    </div>
  </div>
</template>
