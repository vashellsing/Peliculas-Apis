<script setup>
import { ref } from "vue";
import BarraBusqueda from "@/components/BarraBusqueda.vue";
import TarjetaPelicula from "@/components/TarjetaPelicula.vue";

// Simulamos los datos que en un futuro vendran de la api get peliculas api
const seriesMock = ref([
  {
    id: 1,
    titulo: "El Origen",
    calificacion: 8.8,
    imagenUrl:
      "https://via.placeholder.com/300x450/1a1a1a/ffffff?text=El+Origen",
  },
  {
    id: 2,
    titulo: "Interestelar",
    calificacion: 8.6,
    imagenUrl:
      "https://via.placeholder.com/300x450/1a1a1a/ffffff?text=Interestelar",
  },
  {
    id: 3,
    titulo: "Matrix",
    calificacion: 8.7,
    imagenUrl: "https://via.placeholder.com/300x450/1a1a1a/ffffff?text=Matrix",
  },
  {
    id: 4,
    titulo: "El Padrino",
    calificacion: 9.2,
    imagenUrl:
      "https://via.placeholder.com/300x450/1a1a1a/ffffff?text=El+Padrino",
  },
  {
    id: 5,
    titulo: "Pulp Fiction",
    calificacion: 8.9,
    imagenUrl:
      "https://via.placeholder.com/300x450/1a1a1a/ffffff?text=Pulp+Fiction",
  },
]);
</script>

<template>
  <div class="contenedor-principal">
    <section class="seccion-cartelera">
      <h2 class="titulo-seccion">Series Destacadas</h2>

      <div class="cuadricula-peliculas">
        <TarjetaPelicula
          v-for="serie in seriesMock"
          :key="serie.id"
          :titulo="serie.titulo"
          :calificacion="serie.calificacion"
          :imagenUrl="serie.imagenUrl"
        />
      </div>
    </section>
  </div>
</template>

<style scoped>
.seccion-cartelera {
  padding: 3rem 2rem;
  max-width: 1200px;
  margin: 0 auto; /* Centra la sección en pantallas grandes */
}

.titulo-seccion {
  font-family: sans-serif;
  color: #333;
  margin-bottom: 2rem;
}

/* ----------------Aui esta la cuadricula de las peliculas */
.cuadricula-peliculas {
  display: grid;

  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
}
</style>
