<script setup>
defineProps({
  id: {             
    type: Number,
    required: true
  },
  titulo: {
    type: String,
    default: 'Título Desconocido',
  },
  calificacion: {
    type: Number,
    default: 0.0,
  },
  imagenUrl: {
    type: String,
    default: 'https://via.placeholder.com/300x450?text=Sin+Portada',
  },
})
</script>

<template>
  <article class="tarjeta-pelicula">
    <div class="contenedor-imagen">
      <img :src="imagenUrl" :alt="titulo" class="imagen-portada" />
      <div class="calificacion">⭐ {{ calificacion }}</div>
    </div>

    <div class="informacion">
      <h3 class="titulo">{{ titulo }}</h3>
      <RouterLink :to="`/pelicula/${id}`" class="btn-detalles">Ver detalles</RouterLink>
    </div>
  </article>
</template>

<style scoped>

/* Estructura de la tarjeta */
.tarjeta-pelicula {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden; 
  background-color: #fff;
  display: flex;
  flex-direction: column;
  font-family: sans-serif;
  transition: transform 0.2s ease; 
}


.tarjeta-pelicula:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.contenedor-imagen {
  position: relative;
  width: 100%;
  aspect-ratio: 2 / 3;
  background-color: #ddd;
}

.imagen-portada {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.calificacion {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: rgba(0, 0, 0, 0.75);
  color: #fff;
  padding: 0.3rem 0.6rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: bold;
}

.informacion {
  padding: 1.2rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1; 
  justify-content: space-between;
}

.titulo {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  color: #333;
  text-align: center;
}

.btn-detalles {
  display: block; 
  width: 100%; 
  padding: 0.8rem;
  background-color: #4a4a4a;
  color: white;
  text-decoration: none;
  text-align: center;
  border-radius: 4px;
  font-weight: bold;
  box-sizing: border-box; 
  transition: background-color 0.2s;
}

.btn-detalles:hover {
  background-color: #333;
}

</style>
