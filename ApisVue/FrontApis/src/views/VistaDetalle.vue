<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const route = useRoute();

// Variables reactivas
const pelicula = ref(null);
const cargando = ref(true);
const error = ref(null);

// Variables para el Modal del Tráiler
const mostrarModal = ref(false);

// NUEVO: Variables para la Cartelera (simuladas por ahora)
// En el futuro, esto podría venir dentro de la respuesta de tu API (ej. pelicula.value.carteleras)
const funcionesDisponibles = ref([
  {
    id_cartelera: 1,
    nombreCine: "Cine Colombia",
    ciudadCine: "Popayán",
    direccionCine: "C.C. Campanario",
    fecha_hora: "2026-05-20 a las 18:30",
    idioma: "Doblada al Espanol",
  }
]);

// Esta función "traduce" el link de YouTube al formato Embed que permite la web
const trailerEmbedUrl = computed(() => {
  if (!pelicula.value || !pelicula.value.trailer) return "";

  // Extraemos el ID del video de la URL normal
  const urlParams = new URLSearchParams(new URL(pelicula.value.trailer).search);
  const videoId = urlParams.get("v");

  // Le agregamos ?autoplay=1 para que se reproduzca solito al abrir el modal
  return videoId ? `https://www.youtube.com/embed/${videoId}?autoplay=1` : "";
});

const cargarDetalles = async () => {
  try {
    const configuracion = {
      headers: { "x-api-key": "mi_super_api_key_fija_123" },
    };
    const idUrl = route.params.id;

    const respuesta = await axios.get(
      `http://127.0.0.1:5000/peliculas/${idUrl}`,
      configuracion,
    );
    pelicula.value = respuesta.data.pelicula;
  } catch (err) {
    console.error("Error al cargar la película:", err);
    error.value = "No pudimos encontrar esta película.";
  } finally {
    cargando.value = false;
  }
};

// Abre el modal en lugar de salir de la página
const abrirTrailer = () => {
  if (pelicula.value.trailer) {
    mostrarModal.value = true;
  } else {
    alert("Lo sentimos, no hay tráiler disponible para esta película.");
  }
};

// Cierra el modal
const cerrarModal = () => {
  mostrarModal.value = false;
};

const comentarios = ref([
  {
    id: 1,
    usuario: "Cinefilo99",
    titulo: "Una montaña rusa de emociones",
    texto:
      "Lloré, reí y grité en el cine. El manejo de la nostalgia es perfecto.",
    fecha: "15 Dic 2021",
  },
  {
    id: 2,
    usuario: "MarvelFan",
    titulo: "Puro fanservice, pero del bueno",
    texto: "Logra integrar todos los elementos clásicos sin perder el enfoque.",
    fecha: "16 Dic 2021",
  },
]);

onMounted(() => {
  cargarDetalles();
});
</script>

<template>
  <div class="vista-detalle">
    <div class="contenedor-contenido">
      <div v-if="cargando" class="estado-mensaje">
        Cargando detalles de la película... 🎬
      </div>
      <div v-else-if="error" class="estado-mensaje error-texto">
        {{ error }}
      </div>

      <template v-else-if="pelicula">
        <section class="info-principal">
          <div class="contenedor-poster">
            <img :src="pelicula.poster" :alt="pelicula.titulo" class="poster" />
          </div>

          <div class="datos-pelicula">
            <h1 class="titulo">
              {{ pelicula.titulo }}
              <span class="anio">({{ pelicula.anio }})</span>
            </h1>
            <p class="subtitulo">
              {{ pelicula.lema || "El cine en su máxima expresión." }}
            </p>

            <div class="sinopsis">
              <h3>Sinopsis</h3>
              <p>
                {{
                  pelicula.sinopsis ||
                  "No hay sinopsis disponible para esta película."
                }}
              </p>
            </div>

            <div class="detalles-tecnicos">
              <span class="etiqueta">{{ pelicula.genero }}</span>
              <span class="etiqueta">{{ pelicula.idioma }}</span>
            </div>

            <div class="acciones-calificacion">
              <button @click="abrirTrailer" class="btn-primario">
                <span>▶</span> Ver Tráiler
              </button>
              <RouterLink to="/favoritos" class="btn-secundario"
                ><span>❤️</span> Añadir a Favoritos</RouterLink
              >
              <div class="calificacion">
                <span class="estrella">★</span> 4.5 / 5.0
              </div>
            </div>
          </div>
        </section>

        <section class="seccion-cartelera-pelicula">
          <h2 class="titulo-seccion">Funciones Disponibles en Cines</h2>

          <div
            class="contenedor-funciones"
            v-if="funcionesDisponibles.length > 0"
          >
            <div
              class="tarjeta-funcion"
              v-for="funcion in funcionesDisponibles"
              :key="funcion.id_cartelera"
            >
              <div class="info-cine">
                <span class="icono-cine">🍿</span>
                <div>
                  <h4 class="nombre-cine">{{ funcion.nombreCine }}</h4>
                  <p class="ubicacion-cine">
                    {{ funcion.direccionCine }} ({{ funcion.ciudadCine }})
                  </p>
                </div>
              </div>

              <div class="detalles-proyeccion">
                <div class="dato-proyeccion">
                  <span class="etiqueta-proyeccion">Fecha y Hora:</span>
                  <span class="valor-proyeccion"
                    >📅 {{ funcion.fecha_hora }}</span
                  >
                </div>
                <div class="dato-proyeccion">
                  <span class="etiqueta-proyeccion">Idioma:</span>
                  <span class="badge-idioma">{{ funcion.idioma }}</span>
                </div>
              </div>

              <a class="btn-boletos" href="https://www.cinecolombia.com/" target="_blank">Ir al cine</a>
            </div>
          </div>

          <div class="sin-funciones" v-else>
            <p>
              Lo sentimos, esta película no se encuentra programada en ninguna
              cartelera actualmente.
            </p>
          </div>
        </section>

        <section
          class="seccion-reparto"
          v-if="pelicula.actores && pelicula.actores.length > 0"
        >
          <h2 class="titulo-seccion">Reparto Principal</h2>
          <div class="contenedor-columnas">
            <div
              class="tarjeta-actor"
              v-for="(actor, index) in pelicula.actores"
              :key="index"
            >
              <img
                v-if="actor.foto"
                :src="actor.foto"
                :alt="actor.nombre"
                class="foto-actor"
              />
              <div v-else class="foto-actor-vacia">
                {{ actor.nombre.charAt(0) }}
              </div>
              <div class="info-actor">
                <span class="nombre">{{ actor.nombre }}</span>
                <span class="personaje">{{ actor.personaje }}</span>
              </div>
            </div>
          </div>
        </section>

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
                <span class="usuario"
                  >Por: <strong>@{{ comentario.usuario }}</strong></span
                >
              </div>
            </div>
          </div>
        </section>
      </template>
    </div>

    <div v-if="mostrarModal" class="modal-overlay" @click.self="cerrarModal">
      <div class="modal-contenido">
        <button class="btn-cerrar" @click="cerrarModal">✖</button>
        <div class="video-responsive">
          <iframe
            :src="trailerEmbedUrl"
            frameborder="0"
            allow="autoplay; encrypted-media"
            allowfullscreen
          >
          </iframe>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* (Tu CSS anterior intacto) */
.vista-detalle {
  font-family: sans-serif;
  color: #333;
  background-color: #fafafa;
  padding-bottom: 4rem;
}
.contenedor-contenido {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
  background-color: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  margin-top: 2rem;
}
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
  margin: 0 0 0.5rem 0;
  color: #1a1a1a;
  line-height: 1.1;
}
.anio {
  color: #777;
  font-weight: normal;
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
  margin-bottom: 1.5rem;
}
.detalles-tecnicos {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
}
.etiqueta {
  background-color: #eee;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: bold;
  color: #555;
}
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
  cursor: pointer;
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
  cursor: pointer;
  text-decoration: none;
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

/* NUEVO CSS: CARTELERA */
.seccion-cartelera-pelicula {
  margin-bottom: 4rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 3rem;
}
.contenedor-funciones {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1.5rem;
}
.tarjeta-funcion {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8fafc;
  padding: 1.2rem 1.5rem;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  flex-wrap: wrap;
  gap: 1.5rem;
}
.info-cine {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.icono-cine {
  font-size: 2rem;
}
.nombre-cine {
  margin: 0 0 0.2rem 0;
  font-size: 1.1rem;
  color: #1e293b;
}
.ubicacion-cine {
  margin: 0;
  font-size: 0.85rem;
  color: #64748b;
}
.detalles-proyeccion {
  display: flex;
  gap: 2rem;
}
.dato-proyeccion {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}
.etiqueta-proyeccion {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: bold;
  text-transform: uppercase;
}
.valor-proyeccion {
  font-size: 0.95rem;
  color: #334155;
  font-weight: 500;
}
.badge-idioma {
  background-color: #e2e8f0;
  color: #334155;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: bold;
  width: fit-content;
}
.btn-boletos {
  background-color: #1a1a1a;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  font-size: 0.9rem;
  border-radius: 4px;
  text-decoration: none;
}
.btn-boletos:hover {
  background-color: #333;
}
.sin-funciones {
  text-align: center;
  padding: 2rem;
  color: #64748b;
  background-color: #f8fafc;
  border-radius: 8px;
  font-style: italic;
}

/* Resto de tu CSS original */
.seccion-reparto {
  margin-bottom: 4rem;
}
.titulo-seccion {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: #1a1a1a;
  border-left: 4px solid #e50914;
  padding-left: 0.8rem;
}
.text-center {
  text-align: center;
  border: none;
  padding: 0;
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
.foto-actor-vacia {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
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

/* MODAL Y VIDEO */
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
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  padding: 2.5rem 1rem 1rem 1rem;
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
  padding: 0;
}
.btn-cerrar:hover {
  color: #e50914;
  transform: scale(1.1);
}
.video-responsive {
  position: relative;
  padding-bottom: 56.25%;
  height: 0;
  overflow: hidden;
  border-radius: 4px;
}
.video-responsive iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
