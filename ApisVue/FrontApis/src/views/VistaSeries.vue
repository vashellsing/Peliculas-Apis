<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import TarjetaSerie from "@/components/TarjetaSerie.vue";

// 1. Variables para los datos reales y el estado de carga
const seriesBackend = ref([]);
const cargando = ref(true);

// 2. FUNCIÓN MÁGICA: Conecta al backend
const cargarSeries = async () => {
  try {
    // Configuración con tu API KEY
    const config = {
      headers: { "x-api-key": "mi_super_api_key_fija_123" },
    };

    // Llamamos al puerto 5001 que me confirmaste que funciona
    const url = "http://127.0.0.1:5001/series";

    const respuesta = await axios.get(url, config);

    // Guardamos los datos que nos envía Flask
    seriesBackend.value = respuesta.data.series;
  } catch (error) {
    console.error("Error al cargar las series:", error);
  } finally {
    // Ya terminó de cargar (sea éxito o error)
    cargando.value = false;
  }
};

// 3. Ejecutar la función apenas se abra la página
onMounted(() => {
  cargarSeries();
});

// ==========================================
// LÓGICA DE PAGINACIÓN
// ==========================================
const paginaActual = ref(1);
const elementosPorPagina = 8; // Subí a 8 para que se vean dos filas completas

const totalPaginas = computed(() => {
  return Math.ceil(seriesBackend.value.length / elementosPorPagina);
});

const seriesPaginadas = computed(() => {
  const inicio = (paginaActual.value - 1) * elementosPorPagina;
  const fin = inicio + elementosPorPagina;
  return seriesBackend.value.slice(inicio, fin);
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
      <h2 class="titulo-seccion">Series Destacadas</h2>

      <!-- FEEDBACK: Mientras está esperando al backend -->
      <div v-if="cargando" class="estado-mensaje">
        Cargando el catálogo de series... 🍿
      </div>

      <!-- FEEDBACK: Si el backend respondió, pero la lista está vacía -->
      <div
        v-else-if="seriesBackend.length === 0"
        class="estado-mensaje error-texto"
      >
        No se encontraron series en la base de datos.
      </div>

      <!-- LA CUADRÍCULA REAL: Si todo salió bien -->
      <div v-else>
        <div class="cuadricula-series">
          <!-- OJO AQUÍ: Usamos seriesPaginadas, que viene del backend -->
          <TarjetaSerie
            v-for="serie in seriesPaginadas"
            :key="serie.id"
            :id="serie.id"
            :titulo="serie.titulo"
            :calificacion="4.5"
            :imagenUrl="serie.imagenUrl"
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

.cuadricula-series {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

/* ========================================== */
/* ESTILOS DE FEEDBACK (NUEVO)                */
/* ========================================== */
.estado-mensaje {
  text-align: center;
  padding: 4rem;
  font-size: 1.2rem;
  color: #666;
  background-color: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 3rem;
}

.error-texto {
  color: #e50914;
  font-weight: bold;
}

/* ========================================== */
/* ESTILOS DE PAGINACIÓN                      */
/* ========================================== */
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
