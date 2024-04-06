<template class="container">
  <form
    id="movieForm"
    action=""
    @submit.prevent="saveMovie"
    class="mt-5"
    enctype="multipart/form-data"
  >
    <div v-if="isError" class="alert alert-danger">
      <div v-for="error in errors">
        <li>{{ error }}</li>
      </div>
    </div>
    <div v-if="isSuccess" class="alert alert-success">
      File uploaded successfully
    </div>

    <div class="mb-3">
      <label for="title" class="form-label">Movie Title</label>
      <input type="text" name="title" class="form-control" />
    </div>

    <div class="mb-3">
      <label for="description" class="form-label">Movie Description</label>
      <textarea
        name="description"
        id="description"
        class="form-control"
        rows="4"
      ></textarea>
    </div>

    <div class="mb-3">
      <label for="poster" class="form-label">Movie Poster</label>
      <input type="file" name="poster" id="poster" class="form-control" />
    </div>

    <button type="submit" class="btn btn-primary">Create Movie</button>
  </form>
</template>
<script setup>
import { ref, onMounted } from "vue";

let csrf_token = ref("");
let isError = ref(false);
let isSuccess = ref(false);
let errors = ref([]);

function getCsrfToken() {
  fetch("/api/v1/csrf-token")
    .then((response) => response.json())
    .then((data) => {
      console.log(data)
      csrf_token.value = data.csrf_token;
     
    }).catch((error) => {
      console.log("Error: " + error)
    });
  
}
onMounted(() => {
  getCsrfToken();
});

const saveMovie = async () => {
  let movieForm = document.getElementById("movieForm");
  let form_data = new FormData(movieForm);
  form_data.append("_csrf", csrf_token.value);
  console.log("TOKEN", csrf_token.value)
  await fetch("/api/v1/movies", {
    method: "POST",
    body: form_data,
    headers: {
      "X-CSRFToken": csrf_token.value,
    },
  })
    .then(async function (response) {
      isError.value = !response.ok;
      isSuccess.value = response.ok;

      if (isError.value) {
        const receivedErrors = await response.json();
        errors.value = receivedErrors.errors;
      }

      return response;
    })
    .then(function (data) {
      return data;
    })
    .catch(function (error) {
      isError.value = true;
      isSuccess.value = false;

      return error;
    });
};
</script>
