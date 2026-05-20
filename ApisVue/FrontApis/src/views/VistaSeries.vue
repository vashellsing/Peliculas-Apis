<script setup>
import { ref, computed } from "vue";
import BarraBusqueda from "@/components/BarraBusqueda.vue";
import TarjetaSerie from "@/components/TarjetaSerie.vue";

// Simulamos los datos que en un futuro vendran de la api get peliculas api
const seriesMock = ref([
  {
    id: 1,
    titulo: "The boys",
    calificacion: 8.8,
    imagenUrl:
      "https://www.themoviedb.org/t/p/w600_and_h900_face/5kgY14oisiHcJ4zq0Xgq1e97PHm.jpg",
  },
  {
    id: 2,
    titulo: "Sobrenarutal",
    calificacion: 8.6,
    imagenUrl:
      "https://www.themoviedb.org/t/p/w600_and_h900_face/58Qaj36FZDz54H36LsUI8mGiW9y.jpg",
  },
  {
    id: 3,
    titulo: "El mentalista",
    calificacion: 8.7,
    imagenUrl:
      "https://www.themoviedb.org/t/p/w600_and_h900_face/snKUzvCl3kGv0RWBjEjnOXMGvdl.jpg",
  },
  {
    id: 4,
    titulo: "Dr. House",
    calificacion: 3.2,
    imagenUrl:
      "https://www.themoviedb.org/t/p/w600_and_h900_face/lW7MvZ4m49IUj2UrUu4z0xVVl81.jpg",
  },
  {
    id: 5,
    titulo: "Pulp Fiction",
    calificacion: 4.5,
    imagenUrl:
      "https://via.placeholder.com/300x450/1a1a1a/ffffff?text=Pulp+Fiction",
  },
]);

// PAGINACION

const paginaActual = ref(1);
const elementosPorPagina = 4;

const totalPaginas = computed(() => {
  return Math.ceil(seriesMock.value.length / elementosPorPagina);
});

const seriesPaginadas = computed(() => {
  const inicio = (paginaActual.value - 1) * elementosPorPagina;
  const fin = inicio + elementosPorPagina;
  return seriesMock.value.slice(inicio, fin);
});

// FunciOn para navegar entre pAginas
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

      <div class="cuadricula-series">
        <TarjetaSerie
          v-for="serie in seriesPaginadas"
          :key="serie.id"
          :id="serie.id"
          :titulo="serie.titulo"
          :calificacion="serie.calificacion"
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

/* RESPONSIVE APGINACION        */

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
