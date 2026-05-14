<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import TarjetaPelicula from '../components/TarjetaPelicula.vue'

const route = useRoute()
const peliculas = ref([])
const cargando = ref(true)
const error = ref(null)

const cargarPeliculas = async () => {
  try {
    cargando.value = true
    error.value = null 

    
    const configuracion = { headers: { 'x-api-key': 'mi_super_api_key_fija_123' } }

    // Asumimos por defecto que traeremos todas
    let url = 'http://127.0.0.1:5000/peliculas'

    // Si la URL tiene un parámetro 'titulo' (ej: /?titulo=Shrek)
    if (route.query.titulo) {
      url = `http://127.0.0.1:5000/peliculas/buscar?q=${route.query.titulo}`
    }
    // Si no tiene título pero tiene 'categoria' (ej: /?categoria=Accion)
    else if (route.query.categoria) {
      url = `http://127.0.0.1:5000/peliculas/categoria?q=${route.query.categoria}`
    }

    const respuesta = await axios.get(url, configuracion)
    peliculas.value = respuesta.data.peliculas
  } catch (err) {
    console.error('Error al cargar cartelera:', err)
    error.value = err.response?.data?.mensaje || 'No se encontraron películas para tu búsqueda.'
    peliculas.value = [] // Vaciamos la lista si hay error (ej: si buscó "asdasd")
  } finally {
    cargando.value = false
  }
}

// 1. Cargar al inicio cuando entras a la página
onMounted(() => {
  cargarPeliculas()
})

// 2. EL TRUCO MAGICO: Escuchar si la URL cambia sin recargar la página
watch(
  () => route.query,
  () => {
    cargarPeliculas() // Si cambia la URL, volvemos a disparar la petición a Flask
  },
)
</script>

<template>
  <div class="contenedor-principal">
    <section class="seccion-cartelera">
      <h2 class="titulo-seccion">Películas Destacadas</h2>

      <!-- Mensajes de Estado -->
      <div v-if="cargando" class="estado-mensaje">
        Cargando películas desde la base de datos... 🍿
      </div>

      <div v-else-if="error" class="estado-mensaje error-texto">
        {{ error }}
      </div>

      <!-- Cuadricula catalogo -->
      <div v-else class="cuadricula-peliculas">
        <!-- Iteramos sobre las películas de MySQL -->
        <TarjetaPelicula
          v-for="pelicula in peliculas"
          :key="pelicula.id"
          :id="pelicula.id"
          :titulo="pelicula.titulo"
          :calificacion="4.5"
          :imagenUrl="pelicula.poster"
        />
       
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

/* El Grid Responsivo que ya tenías */
.cuadricula-peliculas {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
}

/* Estilos para los mensajes de carga y error */
.estado-mensaje {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: #666;
  font-family: sans-serif;
}

.error-texto {
  color: #e50914; /* Rojo tipo Netflix para los errores */
  font-weight: bold;
}
</style>
