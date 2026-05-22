<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const route = useRoute();

const serie = ref(null);
const cargando = ref(true);
const error = ref("");
const mostrarModal = ref(false);

const abrirTrailer = () => {
  if (serie.value?.trailer) {
    mostrarModal.value = true;
  } else {
    alert("Esta serie no tiene tráiler disponible.");
  }
};

const cerrarModal = () => {
  mostrarModal.value = false;
};

const trailerSerieEmbedUrl = computed(() => {
  if (!serie.value || !serie.value.trailer) return "";

  const urlParams = new URLSearchParams(new URL(serie.value.trailer).search);
  const videoId = urlParams.get("v");

  return videoId ? `https://www.youtube.com/embed/${videoId}?autoplay=1` : "";
});

// Configuración de API
const config = {
  headers: { "x-api-key": "mi_super_api_key_fija_123" },
};

// Traer detalle real desde el backend
const cargarSerie = async () => {
  try {
    cargando.value = true;
    error.value = "";

    const id = route.params.id;
    const url = `http://127.0.0.1:5001/series/${id}`;

    const respuesta = await axios.get(url, config);
    serie.value = respuesta.data.serie;
  } catch (err) {
    console.error("Error al cargar el detalle de la serie:", err);
    error.value =
      err?.response?.data?.error || "No se pudo cargar el detalle de la serie.";
  } finally {
    cargando.value = false;
  }
};

onMounted(() => {
  cargarSerie();
});

// Normaliza temporadas/episodios para que el front no se rompa
const temporadas = computed(() => {
  const data = serie.value?.temporadas_info;

  if (!Array.isArray(data)) return [];

  return data.map((t, index) => ({
    id: t.id ?? index + 1,
    numero: t.numero ?? t.temporada ?? index + 1,
    titulo: t.titulo ?? `Temporada ${t.numero ?? index + 1}`,
    episodios: Array.isArray(t.episodios)
      ? t.episodios.map((e, i) => ({
          numero: e.numero ?? i + 1,
          titulo: e.titulo ?? `Episodio ${i + 1}`,
          duracion: e.duracion ?? "",
        }))
      : [],
  }));
});

const totalEpisodios = computed(() =>
  temporadas.value.reduce((acc, t) => acc + t.episodios.length, 0),
);

const actores = computed(() => {
  return Array.isArray(serie.value?.actores) ? serie.value.actores : [];
});

// Temporada actualmente abierta
const temporadaAbierta = ref(null);

const toggleTemporada = (id) => {
  temporadaAbierta.value = temporadaAbierta.value === id ? null : id;
};

// Comentarios de ejemplo
const comentarios = ref([
  {
    id: 1,
    usuario: "SerieAdicto",
    titulo: "La serie de superhéroes más diferente",
    texto:
      "Una mezcla brutal de acción, humor negro y crítica social. Homelander da muchísimo miedo.",
    fecha: "12 Jun 2024",
  },
  {
    id: 2,
    usuario: "FanPrime",
    titulo: "Violenta pero increíble",
    texto:
      "Cada temporada mejora más. Los personajes están muy bien construidos y las escenas impactan bastante.",
    fecha: "20 Jul 2024",
  },
  {
    id: 3,
    usuario: "CineSeries",
    titulo: "Antony Starr se roba la pantalla",
    texto:
      "La actuación de Homelander es de las mejores que he visto en televisión. Tremendo villano.",
    fecha: "05 Ago 2024",
  },
]);
</script>

<template>
  <div class="vista-detalle">
    <div class="contenedor-contenido">
      <div v-if="cargando" class="estado">Cargando detalle de la serie...</div>

      <div v-else-if="error" class="estado error">
        {{ error }}
      </div>

      <template v-else-if="serie">
        <!-- INFO PRINCIPAL -->
        <section class="info-principal">
          <div class="contenedor-poster">
            <img :src="serie.imagenUrl" :alt="serie.titulo" class="poster" />
          </div>

          <div class="datos-pelicula">
            <h1 class="titulo">{{ serie.titulo }}</h1>
            <p class="subtitulo">{{ serie.titulo_original || "" }}</p>

            <div class="sinopsis">
              <h3>Sinopsis</h3>
              <p>{{ serie.sinopsis }}</p>
            </div>

            <div class="idioma-badge">
              <span class="idioma-etiqueta">Idioma original:</span>
              <span class="idioma-valor">{{ serie.idioma }}</span>
            </div>

            <div class="acciones-calificacion">
              <button
                v-if="serie.trailer"
                class="btn-primario"
                @click="abrirTrailer"
              >
                <span>▶</span> Ver Tráiler
              </button>

              <div class="calificacion">
                <span class="estrella">★</span> {{ serie.calificacion }} / 10
              </div>
            </div>
          </div>
        </section>

        <!-- TEMPORADAS Y EPISODIOS -->
        <section class="seccion-temporadas">
          <h2 class="titulo-seccion">Temporadas y Episodios</h2>

          <div class="resumen-temporadas">
            <span class="chip">{{ temporadas.length }} temporadas</span>
            <span class="chip">{{ totalEpisodios }} episodios en total</span>
          </div>

          <div v-if="temporadas.length === 0" class="estado pequeño">
            Esta serie no tiene temporadas cargadas todavía.
          </div>

          <div v-else class="acordeon">
            <div
              v-for="temporada in temporadas"
              :key="temporada.id"
              class="acordeon-item"
              :class="{ abierto: temporadaAbierta === temporada.id }"
            >
              <button
                class="acordeon-cabecera"
                @click="toggleTemporada(temporada.id)"
              >
                <div class="cabecera-izq">
                  <span class="num-temporada">T{{ temporada.numero }}</span>
                  <span class="nombre-temporada">{{ temporada.titulo }}</span>
                  <span class="badge-eps"
                    >{{ temporada.episodios.length }} eps.</span
                  >
                </div>

                <span
                  class="icono-flecha"
                  :class="{ girado: temporadaAbierta === temporada.id }"
                >
                  ›
                </span>
              </button>

              <div
                class="acordeon-cuerpo"
                v-show="temporadaAbierta === temporada.id"
              >
                <div
                  v-for="episodio in temporada.episodios"
                  :key="episodio.numero"
                  class="fila-episodio"
                >
                  <span class="ep-numero">{{ episodio.numero }}</span>
                  <span class="ep-titulo">{{ episodio.titulo }}</span>
                  <span class="ep-duracion">{{ episodio.duracion }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- REPARTO -->
        <section class="seccion-reparto">
          <h2 class="titulo-seccion">Reparto Principal</h2>

          <div v-if="actores.length === 0" class="estado pequeño">
            No hay actores registrados para esta serie.
          </div>

          <div v-else class="contenedor-columnas">
            <div
              class="tarjeta-actor"
              v-for="actor in actores"
              :key="actor.id || actor.nombre"
            >
              <img
                :src="
                  actor.foto ||
                  'https://via.placeholder.com/300x450?text=Sin+Foto'
                "
                :alt="actor.nombre"
                class="foto-actor"
              />
              <div class="info-actor">
                <span class="nombre">{{ actor.nombre }}</span>
                <span class="personaje">{{ actor.personaje }}</span>
              </div>
            </div>
          </div>
        </section>

        <!-- COMENTARIOS -->
        <section class="seccion-comentarios">
          <h2 class="titulo-seccion text-center">
            Comentarios de la Comunidad
          </h2>

          <div class="lista-comentarios">
            <div
              class="comentario-item"
              v-for="comentario in comentarios"
              :key="comentario.id"
            >
              <div class="cabecera-comentario">
                <h4 class="titulo-comentario">{{ comentario.titulo }}</h4>
                <span class="fecha">{{ comentario.fecha }}</span>
              </div>

              <p class="texto-comentario">{{ comentario.texto }}</p>

              <div class="pie-comentario">
                <span class="usuario">
                  Por: <strong>@{{ comentario.usuario }}</strong>
                </span>
              </div>
            </div>
          </div>
        </section>
      </template>
    </div>
  </div>

  <div v-if="mostrarModal" class="modal-overlay" @click.self="cerrarModal">
    <div class="modal-contenido">
      <button class="btn-cerrar" @click="cerrarModal">✖</button>

      <div class="video-responsive">
        <iframe
          :src="trailerSerieEmbedUrl"
          frameborder="0"
          allow="autoplay; encrypted-media"
          allowfullscreen
        ></iframe>
      </div>
    </div>
  </div>
</template>

<style scoped>
.vista-detalle {
  font-family: sans-serif;
  color: #333;
  background-color: #fafafa;
  padding-bottom: 4rem;
}

.contenedor-contenido {
  max-width: 1000px;
  margin: 2rem auto 0;
  padding: 2rem;
  background-color: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
}

/* INFO PRINCIPAL */
.info-principal {
  display: flex;
  gap: 3rem;
  margin-bottom: 3rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 3rem;
}

.contenedor-poster {
  flex: 0 0 320px;
}

.poster {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.datos-pelicula {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.titulo {
  font-size: 2.5rem;
  margin: 0 0 0.5rem;
  color: #1a1a1a;
  line-height: 1.1;
}
.subtitulo {
  font-size: 1.2rem;
  color: #666;
  font-style: italic;
  margin-bottom: 1.5rem;
}

.sinopsis h3 {
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
  color: #4a4a4a;
}
.sinopsis p {
  color: #555;
  line-height: 1.6;
  margin-bottom: 1rem;
}

/* ── IDIOMA ─────────────────────────────────────────────────────── */
.idioma-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background-color: #f5f5f5;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  padding: 0.35rem 0.9rem;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
  width: fit-content;
}

.idioma-etiqueta {
  color: #777;
}
.idioma-valor {
  font-weight: bold;
  color: #333;
}

/* ── ACCIONES ────────────────────────────────────────────────────── */
.acciones-calificacion {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: auto;
  flex-wrap: wrap;
}

button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: bold;
  font-size: 1rem;
  transition:
    transform 0.2s,
    background-color 0.2s;
  cursor: pointer;
}
button:hover {
  transform: translateY(-2px);
}

.btn-primario {
  background-color: #e50914;
  color: white;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 6px;
  text-decoration: none;
}
.btn-primario:hover {
  background-color: #b8070f;
}

.btn-secundario {
  background-color: transparent;
  color: #333;
  padding: 0.8rem 1.5rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}
.btn-secundario:hover {
  background-color: #f5f5f5;
  border-color: #999;
}

.calificacion {
  margin-left: auto;
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
}
.estrella {
  color: #f5c518;
}

/* ── TITULO SECCIÓN ──────────────────────────────────────────────── */
.titulo-seccion {
  font-size: 1.5rem;
  margin-bottom: 1.2rem;
  color: #1a1a1a;
  border-left: 4px solid #e50914;
  padding-left: 0.8rem;
}
.text-center {
  text-align: center;
  border: none;
  padding: 0;
}

/* ── TEMPORADAS ─────────────────────────────────────────────────── */
.seccion-temporadas {
  margin-bottom: 3rem;
}

.resumen-temporadas {
  display: flex;
  gap: 0.6rem;
  margin-bottom: 1.2rem;
  flex-wrap: wrap;
}

.chip {
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 20px;
  padding: 0.3rem 0.9rem;
  font-size: 0.85rem;
  font-weight: bold;
  color: #555;
}

.acordeon {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.acordeon-item {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  transition: box-shadow 0.2s;
}
.acordeon-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
.acordeon-item.abierto {
  border-color: #e50914;
}

.acordeon-cabecera {
  width: 100%;
  background-color: #f9f9f9;
  border: none;
  padding: 1rem 1.2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  text-align: left;
  transition: background-color 0.2s;
  transform: none !important; /* anula el hover global de button */
}
.acordeon-cabecera:hover {
  background-color: #f0f0f0;
}
.acordeon-item.abierto .acordeon-cabecera {
  background-color: #fff5f5;
}

.cabecera-izq {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.num-temporada {
  background-color: #e50914;
  color: white;
  border-radius: 4px;
  padding: 0.2rem 0.6rem;
  font-size: 0.8rem;
  font-weight: bold;
  letter-spacing: 0.5px;
}

.nombre-temporada {
  font-weight: bold;
  font-size: 1rem;
  color: #1a1a1a;
}

.badge-eps {
  background-color: #eee;
  color: #666;
  border-radius: 20px;
  padding: 0.15rem 0.6rem;
  font-size: 0.8rem;
}

.icono-flecha {
  font-size: 1.6rem;
  color: #999;
  line-height: 1;
  transition: transform 0.25s ease;
  display: inline-block;
}
.icono-flecha.girado {
  transform: rotate(90deg);
}

/* Lista de episodios */
.acordeon-cuerpo {
  border-top: 1px solid #eee;
  background-color: #fff;
}

.fila-episodio {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.7rem 1.2rem;
  border-bottom: 1px solid #f5f5f5;
  transition: background-color 0.15s;
}
.fila-episodio:last-child {
  border-bottom: none;
}
.fila-episodio:hover {
  background-color: #fafafa;
}

.ep-numero {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background-color: #f0f0f0;
  color: #555;
  font-size: 0.8rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ep-titulo {
  flex: 1;
  font-size: 0.95rem;
  color: #333;
}
.ep-duracion {
  font-size: 0.85rem;
  color: #999;
  white-space: nowrap;
}

/* REPARTO */
.seccion-reparto {
  margin-bottom: 3rem;
}

.contenedor-columnas {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.tarjeta-actor {
  display: flex;
  align-items: center;
  gap: 1rem;
  background-color: #f9f9f9;
  padding: 1rem;
  border-radius: 8px;
}

.foto-actor {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
}
.info-actor {
  display: flex;
  flex-direction: column;
}
.nombre {
  font-weight: bold;
  color: #333;
}
.personaje {
  font-size: 0.85rem;
  color: #777;
}

/*  COMENTARIOS  */
.seccion-comentarios {
  max-width: 800px;
  margin: 0 auto;
}

.lista-comentarios {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: 2rem;
}

.comentario-item {
  border: 1px solid #eaeaea;
  padding: 1.5rem;
  border-radius: 8px;
  background-color: #fff;
  transition: box-shadow 0.2s;
}
.comentario-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.cabecera-comentario {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
}
.titulo-comentario {
  margin: 0;
  font-size: 1.1rem;
  color: #1a1a1a;
}
.fecha {
  font-size: 0.85rem;
  color: #999;
}
.texto-comentario {
  color: #555;
  line-height: 1.5;
  margin-bottom: 1rem;
}
.usuario {
  font-size: 0.9rem;
  color: #666;
}

/* RESPONSIVE */
@media (max-width: 680px) {
  .info-principal {
    flex-direction: column;
    align-items: center;
  }
  .contenedor-poster {
    flex: unset;
    width: 200px;
  }
  .contenedor-columnas {
    grid-template-columns: 1fr;
  }
  .acciones-calificacion {
    justify-content: center;
  }
  .calificacion {
    margin-left: 0;
  }
}
/* -----El modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-contenido {
  position: relative;
  width: 90%;
  max-width: 900px;
  background-color: #000;
  border-radius: 8px;
  padding: 2.5rem 1rem 1rem;
}

.btn-cerrar {
  position: absolute;
  top: 5px;
  right: 15px;
  background: none;
  border: none;
  color: white;
  font-size: 1.8rem;
  cursor: pointer;
}

.video-responsive {
  position: relative;
  padding-bottom: 56.25%;
  height: 0;
}

.video-responsive iframe {
  position: absolute;
  width: 100%;
  height: 100%;
}
</style>
