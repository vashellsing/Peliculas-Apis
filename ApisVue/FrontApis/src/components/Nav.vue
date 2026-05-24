<script setup>
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

// No necesitas computed() aquí porque los del store ya lo son
// Los usas directamente: authStore.estaAutenticado, authStore.esAdmin

const cerrarSesion = () => {
  authStore.limpiarToken(); // borra el token del store y del localStorage
  router.push("/");         // regresa al inicio
};
</script>

<template>
  <nav class="barra-navegacion">
    <div class="seccion-izquierda">
      <RouterLink to="/">
        <img src="@/assets/logo.png" alt="Logo" class="logo" />
      </RouterLink>

      <ul class="enlaces">
        <li><RouterLink to="/">Peliculas</RouterLink></li>
        <li><RouterLink to="/series">Series</RouterLink></li>
        
        <!-- Favoritos solo tiene sentido estando autenticado -->
        <li v-if="authStore.estaAutenticado">
          <RouterLink to="/favoritos">Favoritos</RouterLink>
        </li>
        
        <li><RouterLink to="/generos">Generos</RouterLink></li>

        <!-- Admin solo aparece si el token dice que el rol es administrador -->
        <li v-if="authStore.esAdmin">
          <RouterLink to="/admin" style="color: #e50914; font-weight: bold">
            Admin
          </RouterLink>
        </li>
      </ul>
    </div>

    <div class="seccion-derecha">
      <!-- Bloque para usuario autenticado -->
      <template v-if="authStore.estaAutenticado">
        <RouterLink to="/perfil" class="btn-secundario" style="border-color: #e50914; color: #e50914">
          Mi Perfil
        </RouterLink>
        <!-- Cerrar sesión es un botón, no un RouterLink, porque ejecuta lógica -->
        <button class="btn-primario" @click="cerrarSesion">
          Cerrar Sesión
        </button>
      </template>

      <!-- Bloque para usuario no autenticado -->
      <RouterLink v-else to="/acceso" class="btn-secundario">
        Iniciar sesión
      </RouterLink>
    </div>
  </nav>
</template>

  <style scoped>

  .barra-navegacion {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 1.2rem; 
  font-family: sans-serif;
}

.seccion-izquierda {
  display: flex;
  align-items: center;
  gap: 2rem; 
}

.logo {
  width: 50px;  
  height: auto;
  display: block;
  cursor: pointer;
  margin-top: -8px;
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

  
  .btn-primario,
  .btn-secundario {
    cursor: pointer;
    padding: 0.5rem 1.2rem;
    border-radius: 4px;
    font-size: 0.9rem;
    font-family: sans-serif;
    text-decoration: none; 
    display: inline-block;
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
