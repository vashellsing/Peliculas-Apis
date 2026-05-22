<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import TarjetaPelicula from "../components/TarjetaPelicula.vue";

// Variables reactivas para el estado de la vista
const peliculasFavoritas = ref([]);
const cargando = ref(true);
const errorMensaje = ref("");

// ==========================================
// FUNCIÓN PARA TRAER LOS FAVORITOS DE LA API
// ==========================================
const cargarFavoritos = async () => {
  cargando.value = true;
  errorMensaje.value = "";

  try {
    const token = localStorage.getItem("token_cine");

    if (!token) {
      errorMensaje.value = "Debes iniciar sesión para ver tus favoritos.";
      cargando.value = false;
      return;
    }

    const configuracion = {
      headers: {
        "x-api-key": "mi_super_api_key_fija_123", // Usa tu API Key real
        Authorization: `Bearer ${token}`,
      },
    };

    // Petición al backend (Ajusta el puerto 5001 si es necesario)
    const respuesta = await axios.get(
      "http://127.0.0.1:5000/favoritos/mio",
      configuracion,
    );

    // Mapeamos los datos que ahora sí vienen directo de tu tabla Películas
    peliculasFavoritas.value = respuesta.data.favoritos.map(fav => ({
      id: fav.id_pelicula,
      titulo: fav.titulo,
      calificacion: fav.calificacion, // ¡Ya lee el promedio dinámico!
      imagenUrl: fav.poster
    }));
  } catch (error) {
    console.error("Error al cargar favoritos:", error);
    if (error.response && error.response.status === 401) {
      errorMensaje.value =
        "Tu sesión ha expirado. Por favor, inicia sesión de nuevo.";
    } else {
      errorMensaje.value = "Hubo un problema al cargar tus favoritos.";
    }
  } finally {
    cargando.value = false;
  }
};

// Disparamos la carga cuando el componente se monta en pantalla
onMounted(() => {
  cargarFavoritos();
});

// ==========================================
// LÓGICA DE PAGINACIÓN CORREGIDA
// ==========================================
const paginaActual = ref(1);
const elementosPorPagina = 4;

// Ahora apunta correctamente a peliculasFavoritas
const totalPaginas = computed(() => {
  return Math.ceil(peliculasFavoritas.value.length / elementosPorPagina);
});

// Ahora corta el arreglo de datos reales
const PeliculasPaginadas = computed(() => {
  const inicio = (paginaActual.value - 1) * elementosPorPagina;
  const fin = inicio + elementosPorPagina;
  return peliculasFavoritas.value.slice(inicio, fin);
});

const cambiarPagina = (nuevaPagina) => {
  if (nuevaPagina >= 1 && nuevaPagina <= totalPaginas.value) {
    paginaActual.value = nuevaPagina;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
};
</script>

<template>
  <div class="contenedor-principal">
    <section class="seccion-cartelera">
      <h2 class="titulo-seccion">Mis favoritos</h2>

      <div v-if="cargando" class="mensaje-estado">
        Cargando tus películas favoritas...
      </div>

      <div v-else-if="errorMensaje" class="mensaje-estado error">
        {{ errorMensaje }}
      </div>

      <div v-else-if="peliculasFavoritas.length === 0" class="mensaje-estado">
        Aún no tienes películas en tu lista de favoritos.
      </div>

      <div v-else class="cuadricula-peliculas">
        <TarjetaPelicula
          v-for="pelicula in PeliculasPaginadas"
          :key="pelicula.id"
          :titulo="pelicula.titulo"
          :calificacion="pelicula.calificacion"
          :imagenUrl="pelicula.imagenUrl"
          :id="pelicula.id"
        />
      </div>

      <div
        class="paginacion"
        v-if="totalPaginas > 1 && peliculasFavoritas.length > 0"
      >
        <button
          class="btn-paginacion"
          :disabled="paginaActual === 1"
          @click="cambiarPagina(paginaActual - 1)"
        >
          &laquo; <span class="texto-btn">Anterior</span>
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
          <span class="texto-btn">Siguiente</span> &raquo;
        </button>
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

.mensaje-estado {
  text-align: center;
  font-size: 1.2rem;
  color: #666;
  padding: 3rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.mensaje-estado.error {
  color: #e50914;
  background-color: #fde8e9;
}

.cuadricula-peliculas {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.paginacion {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #eaeaea;
}

.numeros-pagina {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
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
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.btn-numero {
  padding: 0.5rem 0.8rem;
  min-width: 40px;
  justify-content: center;
}

.btn-paginacion:hover:not(:disabled),
.btn-numero:hover:not(.activo) {
  background-color: #f5f5f5;
  border-color: #999;
  transform: translateY(-2px);
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
  transform: none;
}

@media (max-width: 600px) {
  .paginacion {
    gap: 0.8rem;
  }

  .btn-paginacion {
    padding: 0.5rem 0.8rem;
  }

  .btn-numero {
    padding: 0.4rem 0.6rem;
    min-width: 35px;
    font-size: 0.9rem;
  }

  .texto-btn {
    display: none;
  }
}
</style>
