<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import TarjetaPelicula from "../components/TarjetaPelicula.vue";

const route = useRoute();
const peliculas = ref([]);
const cargando = ref(true);
const error = ref(null);

// --- VARIABLES DE PAGINACIÓN ---
const paginaActual = ref(1);
const elementosPorPagina = 8; // Puedes ajustar cuántas películas quieres ver por página

const cargarPeliculas = async () => {
  try {
    cargando.value = true;
    error.value = null;

    const configuracion = {
      headers: { "x-api-key": "mi_super_api_key_fija_123" },
    };
    let url = "http://127.0.0.1:5000/peliculas";

    if (route.query.titulo) {
      url = `http://127.0.0.1:5000/peliculas/buscar?q=${route.query.titulo}`;
    } else if (route.query.categoria) {
      url = `http://127.0.0.1:5000/peliculas/categoria?q=${route.query.categoria}`;
    }

    const respuesta = await axios.get(url, configuracion);
    peliculas.value = respuesta.data.peliculas;
  } catch (err) {
    console.error("Error al cargar cartelera:", err);
    error.value =
      err.response?.data?.mensaje ||
      "No se encontraron películas para tu búsqueda.";
    peliculas.value = [];
  } finally {
    cargando.value = false;
  }
};

// --- LÓGICA COMPUTADA PARA PAGINACIÓN ---
const totalPaginas = computed(() => {
  return Math.ceil(peliculas.value.length / elementosPorPagina);
});

const peliculasPaginadas = computed(() => {
  const inicio = (paginaActual.value - 1) * elementosPorPagina;
  const fin = inicio + elementosPorPagina;
  return peliculas.value.slice(inicio, fin);
});

const cambiarPagina = (nuevaPagina) => {
  if (nuevaPagina >= 1 && nuevaPagina <= totalPaginas.value) {
    paginaActual.value = nuevaPagina;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
};

// 1. Cargar al inicio
onMounted(() => {
  cargarPeliculas();
});

// 2. Escuchar cambios en la URL (Nueva búsqueda o filtro)
watch(
  () => route.query,
  () => {
    paginaActual.value = 1; // ¡CRUCIAL! Regresamos a la página 1 al buscar algo nuevo
    cargarPeliculas();
  },
);
</script>

<template>
  <div class="contenedor-principal">
    <section class="seccion-cartelera">
      <h2 class="titulo-seccion">Películas Destacadas</h2>

      <div v-if="cargando" class="estado-mensaje">
        Cargando películas desde la base de datos... 🍿
      </div>

      <div v-else-if="error" class="estado-mensaje error-texto">
        {{ error }}
      </div>

      <div v-else>
        <div class="cuadricula-peliculas">
          <TarjetaPelicula
            v-for="pelicula in peliculasPaginadas"
            :key="pelicula.id"
            :id="pelicula.id"
            :titulo="pelicula.titulo"
            :calificacion="4.5"
            :imagenUrl="pelicula.poster"
          />
        </div>

        <div class="paginacion" v-if="totalPaginas > 1">
          <button
            class="btn-paginacion"
            :disabled="paginaActual === 1"
            @click="cambiarPagina(paginaActual - 1)"
          >
            &laquo; Anterior
          </button>

          <div class="numeros-pagina">
            <button
              v-for="numero in totalPaginas"
              :key="numero"
              class="btn-numero"
              :class="{ activo: paginaActual === numero }"
              @click="cambiarPagina(numero)"
            >
              {{ numero }}
            </button>
          </div>

          <button
            class="btn-paginacion"
            :disabled="paginaActual === totalPaginas"
            @click="cambiarPagina(paginaActual + 1)"
          >
            Siguiente &raquo;
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.seccion-cartelera {
  padding: 3rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.titulo-seccion {
  font-family: sans-serif;
  color: #333;
  margin-bottom: 2rem;
}

.cuadricula-peliculas {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem; /* Espacio para la paginación */
}

.estado-mensaje {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: #666;
  font-family: sans-serif;
}

.error-texto {
  color: #e50914;
  font-weight: bold;
}

/* ========================================== */
/* ESTILOS DE PAGINACIÓN */
/* ========================================== */
.paginacion {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #eaeaea;
}

.numeros-pagina {
  display: flex;
  gap: 0.5rem;
}

.btn-paginacion,
.btn-numero {
  background-color: white;
  border: 1px solid #ccc;
  color: #333;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-family: sans-serif;
  font-weight: bold;
  transition: all 0.2s;
}

.btn-numero {
  padding: 0.5rem 0.8rem;
}

.btn-paginacion:hover:not(:disabled),
.btn-numero:hover:not(.activo) {
  background-color: #f5f5f5;
  border-color: #999;
}

.btn-numero.activo {
  background-color: #e50914;
  color: white;
  border-color: #e50914;
}

.btn-paginacion:disabled {
  background-color: #f9f9f9;
  color: #aaa;
  border-color: #eee;
  cursor: not-allowed;
}
</style>
