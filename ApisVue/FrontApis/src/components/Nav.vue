<script setup>
// Aquí más adelante podremos agregar la lógica para saber si el usuario inició sesión
</script>

<template>
  <nav class="barra-navegacion">
    <div class="seccion-izquierda">
      <svg class="logo" viewBox="0 0 24 24" fill="currentColor">
        <path
          d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"
        />
      </svg>

      <ul class="enlaces">
        <li><RouterLink to="/">Peliculas</RouterLink></li>
        <li><RouterLink to="/series">Series</RouterLink></li>
        <li><RouterLink to="/favoritos">Favoritos</RouterLink></li>
        <li><RouterLink to="/generos">Generos</RouterLink></li>

        <li>
          <RouterLink
            to="/admin"
            style="text-decoration: none; color: #e50914; font-weight: bold"
            >Admin</RouterLink
          >
        </li>
      </ul>
    </div>

    <div class="seccion-derecha">
      <RouterLink
        to="/perfil"
        class="btn-secundario"
        style="border-color: #e50914; color: #e50914"
        >Mi Perfil</RouterLink
      >
      <RouterLink
        to="/acceso"
        class="btn-secundario"
        style="text-decoration: none"
        >Iniciar sesion</RouterLink
      >
      <!-- <RouterLink to="/acceso" class="btn-primario" style="text-decoration: none;">Registrarse</RouterLink> -->
    </div>
  </nav>
</template>

<style scoped>
/* Estilos para que se vea como en tu diseño */
.barra-navegacion {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  font-family: sans-serif;
}

.seccion-izquierda {
  display: flex;
  align-items: center;
  gap: 2.5rem; /* Espacio entre el logo y los enlaces */
}

.logo {
  width: 35px;
  height: 35px;
  color: #4a4a4a; /* Gris oscuro */
}

.enlaces {
  display: flex;
  list-style: none;
  gap: 1.5rem;
  margin: 0;
  padding: 0;
}

.enlaces a {
  text-decoration: none;
  color: #666;
  font-size: 0.95rem;
}

.enlaces a:hover {
  color: #000;
}

.seccion-derecha {
  display: flex;
  gap: 1rem;
}

/* Unificamos los estilos base para ambos botones/enlaces */
.btn-primario,
.btn-secundario {
  cursor: pointer;
  padding: 0.5rem 1.2rem;
  border-radius: 4px;
  font-size: 0.9rem;
  font-family: sans-serif;
  text-decoration: none; /* Quita la línea de abajo típica de los enlaces */
  display: inline-block; /* Hace que respeten el padding y se vean cuadrados */
  text-align: center;
  box-sizing: border-box;
}

.btn-secundario {
  background-color: transparent;
  border: 1px solid #666;
  color: #666;
}

.btn-secundario:hover {
  background-color: #f5f5f5;
}

.btn-primario {
  background-color: #4a4a4a;
  border: 1px solid #4a4a4a;
  color: white;
}

.btn-primario:hover {
  background-color: #333;
}
</style>
