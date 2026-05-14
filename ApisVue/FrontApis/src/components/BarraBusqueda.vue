<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router' // <-- Importamos el Router

const router = useRouter()

const textoBusqueda = ref('')
const generoSeleccionado = ref('')

const realizarBusqueda = () => {
  // 1. Preparamos un objeto con lo que vamos a poner en la URL
  const queryParams = {}

  if (textoBusqueda.value.trim() !== '') {
    queryParams.titulo = textoBusqueda.value.trim()
  }

  if (generoSeleccionado.value !== '') {
    queryParams.categoria = generoSeleccionado.value
  }

  // 2. Le decimos al Router que vaya a la página de inicio (/)
  // y le pegue los parámetros en la URL (ej: /?titulo=Shrek&categoria=Comedia)
  router.push({ path: '/', query: queryParams })

  // Opcional: Limpiar el campo de texto después de buscar
  textoBusqueda.value = ''
}
</script>

<template>
  <section class="seccion-busqueda">
    <div class="contenedor-buscador">
      <h2>Encuentra tu próxima película favorita</h2>

      <form @submit.prevent="realizarBusqueda" class="formulario-busqueda">
        <input
          type="text"
          v-model="textoBusqueda"
          placeholder="Buscar por título..."
          class="input-busqueda"
        />

        <!-- LOS VALUES AHORA COINCIDEN EXACTAMENTE CON TU BD -->
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
/* Tu CSS original se mantiene igual, no lo toqué porque está perfecto */
.seccion-busqueda {
  padding: 3rem 2rem;
  background-color: #f5f5f5;
  display: flex;
  justify-content: center;
  font-family: sans-serif;
}
.contenedor-buscador {
  width: 100%;
  max-width: 800px;
  text-align: center;
}
.contenedor-buscador h2 {
  margin-bottom: 1.5rem;
  color: #333;
  font-size: 1.8rem;
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
