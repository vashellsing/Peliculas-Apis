<script setup>
import BarraBusqueda from "@/components/BarraBusqueda.vue";
import { ref } from "vue";

// json futuro de la api
const serie = ref({
  titulo: "The Boys",
  lema: "Nunca conozcas a tus héroes.",
  sinopsis:
    'En un mundo donde los superhéroes son celebridades corruptas controladas por una poderosa corporación, un grupo de vigilantes conocidos como "The Boys" decide enfrentarlos y revelar la verdad detrás de su falsa imagen.',
  calificacion: 8.8,
  idioma: "Inglés",
  imagenUrl:
    "https://www.themoviedb.org/t/p/w600_and_h900_face/5kgY14oisiHcJ4zq0Xgq1e97PHm.jpg",
});

// Temporadas y episodios
const temporadas = ref([
  {
    id: 1,
    numero: 1,
    titulo: "Temporada 1",
    episodios: [
      { numero: 1, titulo: "El nombre del juego", duracion: "62 min" },
      { numero: 2, titulo: "Cherry", duracion: "55 min" },
      { numero: 3, titulo: "Trío de cuerdas", duracion: "58 min" },
      { numero: 4, titulo: "La gran cabalgata", duracion: "54 min" },
      { numero: 5, titulo: "Buenas para el negocio", duracion: "51 min" },
      { numero: 6, titulo: "La soga", duracion: "53 min" },
      { numero: 7, titulo: "La bola de nieve", duracion: "57 min" },
      { numero: 8, titulo: "La fuerza de voluntad", duracion: "60 min" },
    ],
  },
  {
    id: 2,
    numero: 2,
    titulo: "Temporada 2",
    episodios: [
      { numero: 1, titulo: "El que siembra vientos", duracion: "63 min" },
      { numero: 2, titulo: "Verdad", duracion: "56 min" },
      { numero: 3, titulo: "Sang Froid", duracion: "54 min" },
      { numero: 4, titulo: "Vought Rising", duracion: "59 min" },
      { numero: 5, titulo: "Necesidad de velocidad", duracion: "52 min" },
      { numero: 6, titulo: "El espejo", duracion: "55 min" },
      { numero: 7, titulo: "Nunca conozcas a tus héroes", duracion: "58 min" },
      { numero: 8, titulo: "Lo que se rompe", duracion: "62 min" },
    ],
  },
  {
    id: 3,
    numero: 3,
    titulo: "Temporada 3",
    episodios: [
      { numero: 1, titulo: "Payback", duracion: "65 min" },
      { numero: 2, titulo: "El primero en su clase", duracion: "57 min" },
      { numero: 3, titulo: "Herogasm", duracion: "61 min" },
      { numero: 4, titulo: "Hombre vs. héroe", duracion: "54 min" },
      {
        numero: 5,
        titulo: "The Last Time to Look on This World of Lies",
        duracion: "56 min",
      },
      { numero: 6, titulo: "Temporada de brujas", duracion: "58 min" },
      {
        numero: 7,
        titulo: "Here Comes a Candle to Light You to Bed",
        duracion: "60 min",
      },
      { numero: 8, titulo: "El arma más grande", duracion: "70 min" },
    ],
  },
]);

// Temporada actualmente expandida (null = todas cerradas)
const temporadaAbierta = ref(null);

const toggleTemporada = (id) => {
  temporadaAbierta.value = temporadaAbierta.value === id ? null : id;
};

// los actores
const actores = ref([
  {
    id: 1,
    nombre: "Karl Urban",
    personaje: "Billy Butcher",
    foto: "https://media.themoviedb.org/t/p/w300_and_h450_face/6CkZLwEJxfqqcJHyeXegMAvOlPh.jpg",
  },
  {
    id: 2,
    nombre: "Jack Quaid",
    personaje: "Hughie Campbell",
    foto: "https://media.themoviedb.org/t/p/w300_and_h450_face/320qW5yEbxpmyxQ3evmClJbtKag.jpg",
  },
  {
    id: 3,
    nombre: "Antony Starr",
    personaje: "Homelander",
    foto: "https://media.themoviedb.org/t/p/w300_and_h450_face/b0T56GMrHM24hDDjJ4DNPJcEUp6.jpg",
  },
]);

// Simulamos comentarios reales de usuarios
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
      <!-- ── INFO PRINCIPAL ────────────────────────────────────── -->
      <section class="info-principal">
        <div class="contenedor-poster">
          <img :src="serie.imagenUrl" :alt="serie.titulo" class="poster" />
        </div>

        <div class="datos-pelicula">
          <h1 class="titulo">{{ serie.titulo }}</h1>
          <p class="subtitulo">{{ serie.lema }}</p>

          <div class="sinopsis">
            <h3>Sinopsis</h3>
            <p>{{ serie.sinopsis }}</p>
          </div>

          <!-- IDIOMA -->
          <div class="idioma-badge">
            <span class="idioma-etiqueta">Idioma original:</span>
            <span class="idioma-valor">{{ serie.idioma }}</span>
          </div>

          <div class="acciones-calificacion">
            <a
              class="btn-primario"
              href="https://youtu.be/AD0qUhZpbfc"
              target="_blank"
              ><span>▶</span>Ver Tráiler</a
            >
            <div class="calificacion">
              <span class="estrella">★</span> {{ serie.calificacion }} / 10.0
            </div>
          </div>
        </div>
      </section>

      <!-- ── TEMPORADAS Y EPISODIOS ────────────────────────────── -->
      <section class="seccion-temporadas">
        <h2 class="titulo-seccion">Temporadas y Episodios</h2>

        <div class="resumen-temporadas">
          <span class="chip">{{ temporadas.length }} temporadas</span>
          <span class="chip">
            {{
              temporadas.reduce((acc, t) => acc + t.episodios.length, 0)
            }}
            episodios en total
          </span>
        </div>

        <div class="acordeon">
          <div
            v-for="temporada in temporadas"
            :key="temporada.id"
            class="acordeon-item"
            :class="{ abierto: temporadaAbierta === temporada.id }"
          >
            <!-- Cabecera clickeable -->
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

            <!-- Lista de episodios (desplegable) -->
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

      <!-- ── REPARTO ────────────────────────────────────────────── -->
      <section class="seccion-reparto">
        <h2 class="titulo-seccion">Reparto Principal</h2>
        <div class="contenedor-columnas">
          <div class="tarjeta-actor" v-for="actor in actores" :key="actor.id">
            <img :src="actor.foto" :alt="actor.nombre" class="foto-actor" />
            <div class="info-actor">
              <span class="nombre">{{ actor.nombre }}</span>
              <span class="personaje">{{ actor.personaje }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- ── COMENTARIOS ────────────────────────────────────────── -->
      <section class="seccion-comentarios">
        <h2 class="titulo-seccion text-center">Comentarios de la Comunidad</h2>
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
              <span class="usuario"
                >Por: <strong>@{{ comentario.usuario }}</strong></span
              >
            </div>
          </div>
        </div>
      </section>
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

/* ── INFO PRINCIPAL ─────────────────────────────────────────────── */
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

/* ── REPARTO ──────────────────────────────────────────────────────── */
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

/* ── COMENTARIOS ──────────────────────────────────────────────────── */
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

/* ── RESPONSIVE ───────────────────────────────────────────────────── */
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
</style>
