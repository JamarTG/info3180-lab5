<template>
  <form id="movieForm" action="" @submit.prevent="saveMovie">
    <div class="form-group mb-3">
      <label for="title" class="form-label">Movie Title</label>
      <input type="text" name="title" class="formcontrol" />
      <label for="description" class="form-label">Movie Description</label>
      <input
        type="text"
        name="description"
        id="description"
        class="formcontrol"
      />
      <label for="poster" class="form-label">Movie Poster</label>
      <input type="file" name="poster" id="poster" class="formcontrol" />

      <button type="submit">Create Movie</button>
    </div>
  </form>
</template>
<script setup>
import { ref, onMounted } from "vue";
let csrf_token = ref("");
function getCsrfToken() {
  fetch("/api/v1/csrf-token")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      csrf_token.value = data.csrf_token;
    });
}
onMounted(() => {
  getCsrfToken();
});

const saveMovie = async () => {
  let movieForm = document.getElementById("movieForm");
  let form_data = new FormData(movieForm);
  form_data.append('_csrf', csrf_token.value);
  await fetch("/api/v1/movies", {
    method: "POST",
    body: form_data,
    headers: {
      "X-CSRFToken": csrf_token.value,
    },
  })
    .then(function (response) {
      return response
    })
    .then(function (data) {
      console.log(data);
    })
    .catch(function (error) {
      console.log(error);
    });
};
</script>
