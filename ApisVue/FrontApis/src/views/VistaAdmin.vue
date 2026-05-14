<script setup>
import { ref } from 'vue'

// Datos simulados de la base de datos
const peliculasAdmin = ref([
  { id: 1, titulo: 'El Origen', calificacion: 8.8, genero: 'Ciencia Ficción' },
  { id: 2, titulo: 'Interestelar', calificacion: 8.6, genero: 'Ciencia Ficción' },
  { id: 3, titulo: 'Matrix', calificacion: 8.7, genero: 'Acción' },
  { id: 4, titulo: 'El Padrino', calificacion: 9.2, genero: 'Drama' },
  { id: 5, titulo: 'Pulp Fiction', calificacion: 8.9, genero: 'Crimen' },
])

// Funciones simuladas
const agregarPelicula = () => {
  alert('Abriendo formulario para AGREGAR nueva película...')
}

const editarPelicula = (pelicula) => {
  alert(`Abriendo formulario para EDITAR: ${pelicula.titulo}`)
}

const eliminarPelicula = (id) => {
  const confirmacion = confirm('¿Estás seguro de que deseas eliminar esta película?')
  if (confirmacion) {
    // Filtramos el arreglo para simular que se borró
    peliculasAdmin.value = peliculasAdmin.value.filter((p) => p.id !== id)
    console.log(`Película ${id} eliminada`)
  }
}
</script>

<template>
  <div class="vista-admin">
    <div class="contenedor-dashboard">
      <header class="cabecera-admin">
        <div>
          <h1 class="titulo-admin">Panel de Administración</h1>
          <p class="subtitulo-admin">Gestiona el catálogo de películas</p>
        </div>
        <button @click="agregarPelicula" class="btn-agregar">+ Agregar Película</button>
      </header>

      <div class="tabla-contenedor">
        <table class="tabla-peliculas">
          <thead>
            <tr>
              <th>ID</th>
              <th>Título</th>
              <th>Género</th>
              <th>Calificación</th>
              <th class="texto-centro">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="pelicula in peliculasAdmin" :key="pelicula.id">
              <td>#{{ pelicula.id }}</td>
              <td class="font-bold">{{ pelicula.titulo }}</td>
              <td>{{ pelicula.genero }}</td>
              <td>⭐ {{ pelicula.calificacion }}</td>
              <td class="celda-acciones">
                <button @click="editarPelicula(pelicula)" class="btn-accion btn-editar">
                  Editar
                </button>
                <button @click="eliminarPelicula(pelicula.id)" class="btn-accion btn-eliminar">
                  Eliminar
                </button>
              </td>
            </tr>
            <!-- Mensaje si no hay películas -->
            <tr v-if="peliculasAdmin.length === 0">
              <td colspan="5" class="texto-centro sin-datos">No hay películas en el catálogo.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.vista-admin {
  padding: 3rem 2rem;
  font-family: sans-serif;
  background-color: #f9f9f9;
  min-height: 70vh;
}

.contenedor-dashboard {
  max-width: 1000px;
  margin: 0 auto;
}

.cabecera-admin {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.titulo-admin {
  font-size: 2rem;
  color: #333;
  margin: 0 0 0.5rem 0;
}

.subtitulo-admin {
  color: #666;
  margin: 0;
}

.btn-agregar {
  background-color: #4a4a4a;
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.btn-agregar:hover {
  background-color: #333;
}

/* Estilos de la tabla */
.tabla-contenedor {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  overflow: hidden; /* Para que los bordes redondeados apliquen a la tabla */
}

.tabla-peliculas {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.tabla-peliculas th,
.tabla-peliculas td {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #eee;
}

.tabla-peliculas th {
  background-color: #f1f1f1;
  color: #333;
  font-weight: bold;
}

.tabla-peliculas tbody tr:hover {
  background-color: #fdfdfd;
}

.font-bold {
  font-weight: bold;
  color: #1a1a1a;
}

.texto-centro {
  text-align: center;
}

.sin-datos {
  padding: 3rem;
  color: #999;
  font-style: italic;
}

/* Botones de acción */
.celda-acciones {
  display: flex;
  justify-content: center;
  gap: 0.8rem;
}

.btn-accion {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: bold;
}

.btn-editar {
  background-color: #e0e0e0;
  color: #333;
}

.btn-editar:hover {
  background-color: #ccc;
}

.btn-eliminar {
  background-color: #ffe6e6;
  color: #cc0000;
}

.btn-eliminar:hover {
  background-color: #ffcccc;
}
</style>
