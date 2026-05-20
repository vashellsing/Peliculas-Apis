<script setup>
import { ref, onMounted } from 'vue' 
import { useRouter } from 'vue-router'

const router = useRouter()

const textoBusqueda = ref('')
const generoSeleccionado = ref('')


const urlPoster = ref(null)
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const cargarPosterAleatorio = async () => {
  try {
    const respuesta = await fetch(`${API_BASE}/peliculas/poster-aleatorio`, {
      headers: { "x-api-key": "mi_super_api_key_fija_123" } 
    })
    if (!respuesta.ok) return

    const datos = await respuesta.json()
    if (!datos.poster) return

    const img = new Image()
    img.onload = () => { urlPoster.value = datos.poster }
    img.onerror = () => { }
    img.src = datos.poster

  } catch (error) {
    console.error('Poster aleatorio no disponible:', error)
  }
}

onMounted(() => {
  cargarPosterAleatorio()
})


const realizarBusqueda = () => {
  const queryParams = {}

  if (textoBusqueda.value.trim() !== '') {
    queryParams.titulo = textoBusqueda.value.trim()
  }

  if (generoSeleccionado.value !== '') {
    queryParams.categoria = generoSeleccionado.value
  }

  router.push({ path: '/', query: queryParams })
  textoBusqueda.value = ''
}
</script>

<template>

  <section
    class="seccion-busqueda"
    :style="urlPoster ? {
      backgroundImage: `url(${urlPoster})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat'
    } : {}"
  >
    <!-- solo aparece cuando hay imagen, para mantener el texto legible -->
    <div v-if="urlPoster" class="overlay"></div>

    <div class="contenedor-buscador">
      <h2>Encuentra tu próxima película favorita</h2>

      <form @submit.prevent="realizarBusqueda" class="formulario-busqueda">
        <input
          type="text"
          v-model="textoBusqueda"
          placeholder="Buscar por título..."
          class="input-busqueda"
        />

        <select v-model="generoSeleccionado" class="select-genero">
          <option value="">Todos los géneros</option>
          <option value="Accion">Acción</option>
          <option value="Comedia">Comedia</option>
          <option value="Drama">Drama</option>
          <option value="Ciencia Ficcion">Ciencia Ficción</option>
          <option value="Terror">Terror</option>
          <option value="Romance">Romance</option>
          <option value="Animacion">Animación</option>
          <option value="Fantasia">Fantasía</option>
          <option value="Documental">Documental</option>
        </select>

        <button type="submit" class="btn-buscar">Buscar</button>
      </form>
    </div>
  </section>
</template>

<style scoped>
.seccion-busqueda {
  padding: 3rem 2rem;
  background-color: #f5f5f5; 
  display: flex;
  justify-content: center;
  font-family: sans-serif;
  position: relative; 
}

/* Overlay oscuro solo cuando hay imagen de fondo */
.overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
}

.contenedor-buscador {
  width: 100%;
  max-width: 800px;
  text-align: center;
  position: relative;
  z-index: 1;
}

.contenedor-buscador h2 {
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
  color: v-bind("urlPoster ? '#ffffff' : '#333'");
  text-shadow: v-bind("urlPoster ? '0 2px 8px rgba(0,0,0,0.7)' : 'none'");
}

.formulario-busqueda {
  display: flex;
  gap: 0.5rem;
}
.input-busqueda {
  flex: 1;
  padding: 0.8rem 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}
.select-genero {
  padding: 0.8rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  background-color: white;
  cursor: pointer;
}
.btn-buscar {
  padding: 0.8rem 1.5rem;
  background-color: #e50914;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
  font-weight: bold;
}
.btn-buscar:hover {
  background-color: #b8070f;
}
</style>