<template>
  <div class="container">
    <div class="row" v-if="movies.length > 0">
      <div v-for="movie in movies" :key="movie.id" class="col-md-4 mb-4">
        <div class="card">
          <div class="row no-gutters">
            <div class="col-md-5 img-container">
              <img
                :src="movie.poster"
                class="card-img-top"
                alt="Movie Poster"
              />
            </div>
            <div class="col-md-7">
              <div class="card-body">
                <h5 class="card-title">{{ movie.title }}</h5>
                <p class="card-text">{{ movie.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>No movies available.</p>
    </div>
    <button @click.prevent="submitForm" class="btn btn-primary mt-4">
      Submit
    </button>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";

let movies = ref([]);

onMounted(() => {
  fetchMovies();
});

const fetchMovies = () => {
  fetch("/api/v1/movies")
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      movies.value = data;
    });
};
</script>

<style>
.img-container {
  display: flex;
  justify-content: center;
  align-items: center;
}
.card {
  width: 100%;
  height: 200px;
  padding: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
