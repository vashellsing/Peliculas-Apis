<script setup>

import { ref, onMounted, watch, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import TarjetaPelicula from "../components/TarjetaPelicula.vue";

// Esto nos sirve para leer la direccion de arriba (la URL)
const route = useRoute();

// ==========================================
// CAJAS PARA GUARDAR NUESTRA INFORMACION
// ==========================================

// Lista donde pondremos todas las peliculas
const peliculas = ref([]);

// Nos avisa si la pagina sigue pensando/cargando
const cargando = ref(true);

// Para guardar un mensaje si algo sale mal
const error = ref(null);

// ==========================================
// DATOS PARA EL CONTROL DE PAGINAS
// ==========================================

// Empezamos siempre leyendo la pagina 1
const paginaActual = ref(1);

// Cuantas peliculas mostramos por cada pagina
const elementosPorPagina = 8;

// ==========================================
// FUNCION PARA PEDIR LAS PELICULAS
// ==========================================

const cargarPeliculas = async () => {
  try {
    // Empezamos a pensar y borramos cualquier error viejo
    cargando.value = true;
    error.value = null;

    // La llave secreta para que el servidor nos deje entrar
    const configuracion = {
      headers: { "x-api-key": "mi_super_api_key_fija_123" },
    };

    // Direccion basica para pedir TODAS las peliculas
    let url = "http://127.0.0.1:5000/peliculas";

    // Si arriba en la direccion web dice que buscamos un titulo...
    if (route.query.titulo) {
      url = `http://127.0.0.1:5000/peliculas/buscar?q=${route.query.titulo}`;
    }
    // O si dice que buscamos por una categoria en especial...
    else if (route.query.categoria) {
      url = `http://127.0.0.1:5000/peliculas/categoria?q=${route.query.categoria}`;
    }

    // Tocamos la puerta del servidor y esperamos respuesta
    const respuesta = await axios.get(url, configuracion);

    // Guardamos las peliculas en nuestra caja vacia
    peliculas.value = respuesta.data.peliculas;
  } catch (err) {
    // Si algo falla, lo anotamos y ponemos un mensaje en pantalla
    console.error("Error al cargar cartelera:", err);
    error.value =
      err.response?.data?.mensaje ||
      "No se encontraron peliculas para tu busqueda.";

    // Vaciamos la caja porque no encontramos nada
    peliculas.value = [];
  } finally {
    // Al final, haya salido bien o mal, avisamos que ya no estamos pensando
    cargando.value = false;
  }
};

// ==========================================
// LOGICA PARA MOSTRAR LAS PAGINAS 
// ==========================================

// Calcula cuantas paginas necesitamos en total para todas las peliculas
const totalPaginas = computed(() => {
  return Math.ceil(peliculas.value.length / elementosPorPagina);
});

// Recorta la gran lista para mostrar solo las de la pagina que estamos viendo
const peliculasPaginadas = computed(() => {
  const inicio = (paginaActual.value - 1) * elementosPorPagina;
  const fin = inicio + elementosPorPagina;
  return peliculas.value.slice(inicio, fin);
});

// Funcion para que los botones de Siguiente/Anterior cambien de pagina
const cambiarPagina = (nuevaPagina) => {
  // Solo cambiamos si la pagina realmente existe
  if (nuevaPagina >= 1 && nuevaPagina <= totalPaginas.value) {
    paginaActual.value = nuevaPagina;

    // Deslizamos la pantalla suavemente hacia arriba
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
};

// ==========================================
// EVENTOS QUE PONEN TODO A FUNCIONAR
// ==========================================
// Le decimos a la pagina: "Apenas te abras, ve a traer las peliculas"
onMounted(() => {
  cargarPeliculas();
});

// El vigilante: se queda mirando si la direccion de arriba cambia
// (Esto pasa cuando usamos la barra de busqueda)
watch(
  () => route.query,
  () => {
    // Si la URL cambia, volvemos a la pagina 1 y buscamos de nuevo
    paginaActual.value = 1;
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
            :calificacion="pelicula.calificacion"
            :imagenUrl="pelicula.poster"
          />
        </div>
        <div class="paginacion" v-if="totalPaginas > 1">
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
  margin-bottom: 3rem;
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

/* PAGINACION */

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

/* RESPONSIVE */
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
