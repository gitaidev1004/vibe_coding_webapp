<script setup>
/**
 * ch04/vue_project/src/views/BoardFormView.vue
 * 게시글 등록/수정 화면 - 4.7(3)(4) 등록/수정: 입력, 유효성 검사, 저장
 * route param(id)이 있으면 수정 모드, 없으면 등록 모드로 동작한다.
 */
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { http } from "../api/http";

const props = defineProps({ id: { type: [String, Number], default: null } });
const router = useRouter();

const title = ref("");
const content = ref("");
const errorMessage = ref("");
const isSaving = ref(false);

const isEditMode = computed(() => props.id !== null);

onMounted(async () => {
  if (isEditMode.value) {
    const post = await http.get(`/posts/${props.id}`);
    title.value = post.title;
    content.value = post.content;
  }
});

// 유효성 검사: 제목은 필수이며 100자를 넘을 수 없다.
function validate() {
  if (!title.value.trim()) return "제목을 입력해 주세요.";
  if (title.value.length > 100) return "제목은 100자를 넘을 수 없습니다.";
  if (!content.value.trim()) return "내용을 입력해 주세요.";
  return "";
}

async function save() {
  errorMessage.value = validate();
  if (errorMessage.value) return;

  isSaving.value = true;
  try {
    const payload = { title: title.value, content: content.value };
    if (isEditMode.value) {
      await http.put(`/posts/${props.id}`, payload);
      router.push({ name: "board-detail", params: { id: props.id } });
    } else {
      const created = await http.post("/posts", payload);
      router.push({ name: "board-detail", params: { id: created.id } });
    }
  } catch (err) {
    errorMessage.value = err.message;
  } finally {
    isSaving.value = false;
  }
}

defineExpose({ validate, save, title, content, errorMessage });
</script>

<template>
  <form class="board-form" @submit.prevent="save">
    <h2>{{ isEditMode ? "게시글 수정" : "게시글 등록" }}</h2>
    <input v-model="title" placeholder="제목" />
    <textarea v-model="content" placeholder="내용"></textarea>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <button type="submit" :disabled="isSaving">저장</button>
  </form>
</template>
