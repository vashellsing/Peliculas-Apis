<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

// ==========================================
// nUESTRA LISTA FIJA DE GENEROS POR SI LA BASE DE DATOS NO TIENE ALGUNA XD
// ==========================================

const generos = ref([
  {
    nombre: "Accion",
    titulo: "Acción",
    imagenUrl:
      "https://image.tmdb.org/t/p/w500/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg",
  },
  {
    nombre: "Comedia",
    titulo: "Comedia",
    imagenUrl:
      "https://image.tmdb.org/t/p/w500/8kOWDBK6XlPUzckuHDo3wwVRFwt.jpg",
  },
  {
    nombre: "Drama",
    titulo: "Drama",
    imagenUrl:
      "https://image.tmdb.org/t/p/w500/rSPw7tgCH9c6NqICZef4kZjFOQ5.jpg",
  },
  {
    nombre: "Ciencia Ficcion",
    titulo: "Ciencia Ficción",
    imagenUrl:
      "https://image.tmdb.org/t/p/original/d1QKiYtceF3GDtxvTFXFAqwwah9.jpg",
  },
  {
    nombre: "Terror",
    titulo: "Terror",
    imagenUrl:
      "https://image.tmdb.org/t/p/original/ecKQlAEG95k62SMGhvX83oEqANK.jpg",
  },
  {
    nombre: "Romance",
    titulo: "Romance",
    imagenUrl:
      "https://image.tmdb.org/t/p/original/rBTJZrf5UWaxzg5YJd2eqpeaSvm.jpg",
  },
  {
    nombre: "Animacion",
    titulo: "Animación",
    imagenUrl:
      "https://image.tmdb.org/t/p/w500/qA5kPYZA7FkVvqcEfJRoOy4kpHg.jpg",
  },
  {
    nombre: "Fantasia",
    titulo: "Fantasía",
    imagenUrl:
      "https://image.tmdb.org/t/p/original/pNeqCBGdEOhdaMTPlwdy1oJLG75.jpg",
  },
  {
    nombre: "Documental",
    titulo: "Documental",
    imagenUrl:
      "https://image.tmdb.org/t/p/original/awIrfoe6e1SUh5bCSI7cbcLdpEs.jpg",
  },
]);

// ==========================================
// FUNCION PARA BUSCAR POSTERS DINAMICOS
// ==========================================
const cargarImagenesDePeliculas = () => {
  const configuracion = {
    headers: { "x-api-key": "mi_super_api_key_fija_123" },
  };

  // Recorremos cada genero uno por uno
  generos.value.forEach(async (genero) => {
    try {
      // Le pedimos a Flask las peliculas de este genero en especifico
      const url = `http://127.0.0.1:5000/peliculas/categoria?q=${genero.nombre}`;
      const respuesta = await axios.get(url, configuracion);

      // Si nos devolvio peliculas y la lista no esta vacia...
      const peliculasEncontradas = respuesta.data.peliculas;
      if (peliculasEncontradas && peliculasEncontradas.length > 0) {
        // Elegimos una pelicula al azar de las que nos llegaron
        const numeroAlAzar = Math.floor(
          Math.random() * peliculasEncontradas.length,
        );
        const peliculaElegida = peliculasEncontradas[numeroAlAzar];

        // Cambiamos la imagen del "Plan B" por el poster de nuestra pelicula
        if (peliculaElegida.poster) {
          genero.imagenUrl = peliculaElegida.poster;
        }
      }
    } catch (error) {}
  });
};

onMounted(() => {
  cargarImagenesDePeliculas();
});
</script>

<template>
  <div class="vista-generos">
    <div class="contenedor-principal">
      <h1 class="titulo-pagina">Explorar por Géneros</h1>
      <p class="subtitulo">
        Descubre tu próxima historia favorita según tu estado de ánimo.
      </p>

      <div class="cuadricula-generos">
        <RouterLink
          v-for="genero in generos"
          :key="genero.nombre"
          :to="{ path: '/', query: { categoria: genero.nombre } }"
          class="tarjeta-genero"
          :style="{ backgroundImage: `url(${genero.imagenUrl})` }"
        >
          <div class="capa-oscura">
            <h2 class="nombre-genero">{{ genero.titulo }}</h2>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.vista-generos {
  padding: 3rem 2rem;
  font-family: sans-serif;
  background-color: #fafafa;
  min-height: 70vh;
}

.contenedor-principal {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.titulo-pagina {
  font-size: 2.5rem;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
}

.subtitulo {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 3rem;
}

.cuadricula-generos {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

/* Estilos de la tarjeta con imagen de fondo */
.tarjeta-genero {
  position: relative;
  height: 180px;
  border-radius: 12px;
  text-decoration: none;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  background-size: cover;
  background-position: center;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.tarjeta-genero:hover {
  transform: scale(1.03);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  z-index: 2;
}

.capa-oscura {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease;
}

.tarjeta-genero:hover .capa-oscura {
  background-color: rgba(0, 0, 0, 0.3);
}

.nombre-genero {
  margin: 0;
  font-size: 1.8rem;
  color: white;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 2px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
}
</style>
