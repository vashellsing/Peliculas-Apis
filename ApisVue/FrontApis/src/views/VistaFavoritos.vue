<script setup>
// ==========================================
// HERRAMIENTAS NECESARIAS
// ==========================================
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import TarjetaPelicula from "../components/TarjetaPelicula.vue";

// ==========================================
// CAJAS PARA GUARDAR NUESTRA INFORMACION
// ==========================================

// Lista donde pondremos las peliculas favoritas del usuario
const peliculasFavoritas = ref([]);

// Nos avisa si la pagina sigue pensando
const cargando = ref(true);

// Para guardar un mensaje si algo sale mal
const errorMensaje = ref("");

// ==========================================
// FUNCION PARA BUSCAR LAS PELICULAS FAVORITAS
// ==========================================

const cargarFavoritos = async () => {
  // Empezamos a pensar y borramos cualquier error viejo
  cargando.value = true;
  errorMensaje.value = "";

  try {
    // Buscamos el pase de entrada del usuario para saber quien es
    const token = localStorage.getItem("token_cine");

    // Si no tiene pase, le pedimos que inicie sesion
    if (!token) {
      errorMensaje.value = "Debes iniciar sesion para ver tus favoritos.";
      cargando.value = false;
      return; // Detenemos la busqueda aqui mismo
    }

    // Preparamos las llaves y el pase para que el servidor nos deje entrar
    const configuracion = {
      headers: {
        "x-api-key": "mi_super_api_key_fija_123",
        Authorization: `Bearer ${token}`,
      },
    };

    // Pedimos favoritos
    const respuesta = await axios.get(
      "http://127.0.0.1:5000/favoritos/mio",
      configuracion,
    );

    // Acomodamos la informacion que nos manda el servidor para usarla en nuestras tarjetas
    peliculasFavoritas.value = respuesta.data.favoritos.map((fav) => ({
      id: fav.id_pelicula,
      titulo: fav.titulo,
      calificacion: fav.calificacion,
      imagenUrl: fav.poster,
    }));
  } catch (error) {
    // Si hay un error, revisamos si es porque su pase de entrada ya vencio
    if (error.response && error.response.status === 401) {
      errorMensaje.value =
        "Tu sesion ha expirado. Por favor, inicia sesion de nuevo.";
    } else {
      // Si es otro problema distinto, mostramos un mensaje general
      errorMensaje.value = "Hubo un problema al cargar tus favoritos.";
    }
  } finally {
    // Al final avisamos que ya terminamos de pensar, pase lo que pase
    cargando.value = false;
  }
};

// ==========================================
// CONTROL DE LAS PAGINAS
// ==========================================
// Empezamos siempre en la primera pagina
const paginaActual = ref(1);

// Cuantas peliculas favoritas queremos mostrar a la vez en pantalla
const elementosPorPagina = 4;

// Calculamos cuantas paginas necesitamos en total
const totalPaginas = computed(() => {
  return Math.ceil(peliculasFavoritas.value.length / elementosPorPagina);
});

// Recortamos la gran lista para mostrar solo las peliculas de esta pagina
const PeliculasPaginadas = computed(() => {
  const inicio = (paginaActual.value - 1) * elementosPorPagina;
  const fin = inicio + elementosPorPagina;
  return peliculasFavoritas.value.slice(inicio, fin);
});

// Funcion para pasar a la siguiente pagina o a la anterior
const cambiarPagina = (nuevaPagina) => {
  // Solo cambiamos si la pagina a la que queremos ir realmente existe
  if (nuevaPagina >= 1 && nuevaPagina <= totalPaginas.value) {
    paginaActual.value = nuevaPagina;

    // Subimos la pantalla suavemente hasta la parte de arriba
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
};

// ==========================================
// EVENTOS AL ABRIR LA PAGINA
// ==========================================
// Le decimos a la pagina que busque los favoritos en cuanto se abra
onMounted(() => {
  cargarFavoritos();
});
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
