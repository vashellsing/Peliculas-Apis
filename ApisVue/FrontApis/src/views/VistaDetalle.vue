<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'


const route = useRoute()

// Variables reactivas
const pelicula = ref(null)
const cargando = ref(true)
const error = ref(null)

// Variables para el Modal del Tráiler
const mostrarModal = ref(false)

// Esta función "traduce" el link de YouTube al formato Embed que permite la web
const trailerEmbedUrl = computed(() => {
  if (!pelicula.value || !pelicula.value.trailer) return ''

  // Extraemos el ID del video de la URL normal
  const urlParams = new URLSearchParams(new URL(pelicula.value.trailer).search)
  const videoId = urlParams.get('v')

  // Le agregamos ?autoplay=1 para que se reproduzca solito al abrir el modal
  return videoId ? `https://www.youtube.com/embed/${videoId}?autoplay=1` : ''
})

const cargarDetalles = async () => {
  try {
    // 
    const configuracion = { headers: { 'x-api-key': 'mi_super_api_key_fija_123' } }
    const idUrl = route.params.id

    const respuesta = await axios.get(`http://127.0.0.1:5000/peliculas/${idUrl}`, configuracion)
    pelicula.value = respuesta.data.pelicula
  } catch (err) {
    console.error('Error al cargar la película:', err)
    error.value = 'No pudimos encontrar esta película.'
  } finally {
    cargando.value = false
  }
}

// Abre el modal en lugar de salir de la página
const abrirTrailer = () => {
  if (pelicula.value.trailer) {
    mostrarModal.value = true
  } else {
    alert('Lo sentimos, no hay tráiler disponible para esta película.')
  }
}

// Cierra el modal
const cerrarModal = () => {
  mostrarModal.value = false
}

const comentarios = ref([
  {
    id: 1,
    usuario: 'Cinefilo99',
    titulo: 'Una montaña rusa de emociones',
    texto: 'Lloré, reí y grité en el cine. El manejo de la nostalgia es perfecto.',
    fecha: '15 Dic 2021',
  },
  {
    id: 2,
    usuario: 'MarvelFan',
    titulo: 'Puro fanservice, pero del bueno',
    texto: 'Logra integrar todos los elementos clásicos sin perder el enfoque.',
    fecha: '16 Dic 2021',
  },
])

onMounted(() => {
  cargarDetalles()
})
</script>

<template>
  <div class="vista-detalle">

    <div class="contenedor-contenido">
      <!-- ESTADO: CARGANDO O ERROR -->
      <div v-if="cargando" class="estado-mensaje">Cargando detalles de la película... 🎬</div>
      <div v-else-if="error" class="estado-mensaje error-texto">{{ error }}</div>

      
      <template v-else-if="pelicula">
        <section class="info-principal">
          <div class="contenedor-poster">
            <img :src="pelicula.poster" :alt="pelicula.titulo" class="poster" />
          </div>

          <div class="datos-pelicula">
            <h1 class="titulo">
              {{ pelicula.titulo }} <span class="anio">({{ pelicula.anio }})</span>
            </h1>
            <p class="subtitulo">{{ pelicula.lema || 'El cine en su máxima expresión.' }}</p>

            <div class="sinopsis">
              <h3>Sinopsis</h3>
              <p>{{ pelicula.sinopsis || 'No hay sinopsis disponible para esta película.' }}</p>
            </div>

            <div class="detalles-tecnicos">
              <span class="etiqueta">{{ pelicula.genero }}</span>
              <span class="etiqueta">{{ pelicula.idioma }}</span>
            </div>

            <div class="acciones-calificacion">
              <!-- El botón ahora llama a la función que abre el Modal -->
              <button @click="abrirTrailer" class="btn-primario"><span>▶</span> Ver Tráiler</button>
              <button class="btn-secundario"><span>❤️</span> Añadir a Favoritos</button>

              <div class="calificacion"><span class="estrella">★</span> 4.5 / 5.0</div>
            </div>
          </div>
        </section>

        <!-- Reparto -->
        <section class="seccion-reparto" v-if="pelicula.actores && pelicula.actores.length > 0">
          <h2 class="titulo-seccion">Reparto Principal</h2>
          <div class="contenedor-columnas">
            <div class="tarjeta-actor" v-for="(actor, index) in pelicula.actores" :key="index">
              <img v-if="actor.foto" :src="actor.foto" :alt="actor.nombre" class="foto-actor" />
              <div v-else class="foto-actor-vacia">{{ actor.nombre.charAt(0) }}</div>
              <div class="info-actor">
                <span class="nombre">{{ actor.nombre }}</span>
                <span class="personaje">{{ actor.personaje }}</span>
              </div>
            </div>
          </div>
        </section>

        <!-- Comentarios  -->
        <section class="seccion-comentarios">
          <h2 class="titulo-seccion text-center">Comentarios de la Comunidad</h2>
          <div class="lista-comentarios">
            <div class="comentario-item" v-for="comentario in comentarios" :key="comentario.id">
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

    <!-- ========================================== -->
    <!-- VENTANA MODAL PARA EL TRÁILER -->
    <!-- ========================================== -->
    <!-- @click.self hace que si haces click en el fondo negro, se cierre -->
    <div v-if="mostrarModal" class="modal-overlay" @click.self="cerrarModal">
      <div class="modal-contenido">
        <button class="btn-cerrar" @click="cerrarModal">✖</button>

        <!-- Contenedor para que el video mantenga formato 16:9 -->
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
/* (Aquí sigue TODO tu CSS anterior intacto) */
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

/* ========================================== */
/* CSS NUEVO PARA LA VENTANA MODAL Y EL VIDEO */
/* ========================================== */

/* Fondo oscuro que cubre toda la pantalla */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.85); /* Negro casi opaco */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000; /* Asegura que el modal esté por encima de todo */
}

/* La caja donde va el video */
.modal-contenido {
  position: relative;
  width: 90%;
  max-width: 900px; /* Tamaño máximo para que no se vea gigante en PC */
  background-color: #000;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  padding: 2.5rem 1rem 1rem 1rem; /* Espacio arriba para el botón de cerrar */
}

/* Botón de cerrar la X */
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
  color: #e50914; /* Se pone rojo Netflix al pasar el mouse */
  transform: scale(1.1);
}

/* Truco CSS para que los iFrames de YouTube siempre sean responsivos (16:9) */
.video-responsive {
  position: relative;
  padding-bottom: 56.25%; /* Proporción 16:9 (9 / 16 = 0.5625) */
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
