<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const route = useRoute();

const pelicula = ref(null);
const cargando = ref(true);
const error = ref(null);

// Variables para el Modal del Trailer
const mostrarModal = ref(false);

const funcionesDisponibles = ref([
  {
    id_cartelera: 1,
    nombreCine: "Cine Colombia",
    ciudadCine: "Popayán",
    direccionCine: "C.C. Campanario",
    fecha_hora: "2026-05-20 a las 18:30",
    idioma: "Doblada al Espanol",
  },
]);

// Convertimos el link para que funcione a embed
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

// Abre el modal en lugar de salir de la vista
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
// Aqui estaran los comentariso cuando se conecte el api
const comentarios = ref([]);

////////// COMENTARIOS

const cargarComentarios = async () => {
  try {
    const configuracion = {
      headers: { "x-api-key": "mi_super_api_key_fija_123" },
    };
    const idUrl = route.params.id;

    // Llamamos al puerto 5003
    const respuesta = await axios.get(
      `http://127.0.0.1:5003/resenas/${idUrl}`,
      configuracion,
    );
    // Asignamos la respuesta a la variable reactiva
    comentarios.value = respuesta.data.comentarios;
  } catch (err) {
    console.error("Error al cargar los comentarios:", err);
  }
};

const nuevoComentario = ref({
  titulo: "",
  comentario: "",
  calificacion: 5,
});
const mensajeFormulario = ref({ texto: "", tipo: "" }); // Para mostrar éxito o error
const enviandoComentario = ref(false);

// --- NUEVAS VARIABLES PARA LA UI Y LA EDICIÓN ---
const mostrarFormulario = ref(false);
const editandoId = ref(null); // Guardará el ID de la reseña si estamos editando
const usuarioActualId = ref(null);

// Función para extraer el ID del usuario desde el JWT
const obtenerUsuarioDeToken = () => {
  const token = localStorage.getItem("token_cine");
  if (token) {
    try {
      // El payload del JWT es la segunda parte separada por punto
      const payload = JSON.parse(atob(token.split(".")[1]));
      usuarioActualId.value = payload.id; // Asegúrate de que el JWT traiga 'id'
    } catch (e) {
      console.error("Error al decodificar token", e);
    }
  }
};

const alternarFormulario = () => {
  mostrarFormulario.value = !mostrarFormulario.value;
  if (!mostrarFormulario.value) {
    limpiarFormulario(); // Si lo cierra, limpiamos todo
  }
};

const limpiarFormulario = () => {
  nuevoComentario.value = { titulo: "", comentario: "", calificacion: 5 };
  editandoId.value = null;
  mensajeFormulario.value = { texto: "", tipo: "" };
};

const prepararEdicion = (comentario) => {
  nuevoComentario.value = {
    titulo: comentario.titulo,
    comentario: comentario.texto,
    calificacion: comentario.calificacion,
  };
  editandoId.value = comentario.id;
  mostrarFormulario.value = true;
  window.scrollTo({
    top: document.querySelector(".formulario-comentario")?.offsetTop,
    behavior: "smooth",
  });
};

// --- NUEVAS VARIABLES PARA EL MODAL DE ELIMINACIÓN ---
const mostrarModalEliminar = ref(false);
const comentarioAEliminar = ref(null);

// 1. Función para abrir el modal y guardar qué vamos a borrar
const confirmarEliminacion = (id_comentario) => {
  comentarioAEliminar.value = id_comentario;
  mostrarModalEliminar.value = true;
};

// 2. Función para cerrar el modal sin hacer nada
const cerrarModalEliminar = () => {
  mostrarModalEliminar.value = false;
  comentarioAEliminar.value = null;
};

// 3. Función que realmente va al backend a borrar
const ejecutarEliminacion = async () => {
  if (!comentarioAEliminar.value) return;

  const token = localStorage.getItem("token_cine");
  try {
    const config = {
      headers: {
        "x-api-key": "mi_super_api_key_fija_123",
        Authorization: `Bearer ${token}`,
      },
    };

    await axios.delete(
      `http://127.0.0.1:5003/resenas/${comentarioAEliminar.value}`,
      config,
    );
    await cargarComentarios(); // Recargamos la lista
    cerrarModalEliminar(); // Cerramos el modal al terminar con éxito
  } catch (err) {
    console.error("Error eliminando comentario", err);
    alert(err.response?.data?.error || "No se pudo eliminar el comentario");
  }
};

// --- NUEVO: Función para enviar el comentario ---
// --- FUNCIÓN ACTUALIZADA: ENVIAR O EDITAR RESEÑA ---
const enviarResena = async () => {
  mensajeFormulario.value = { texto: "", tipo: "" };
  const token = localStorage.getItem("token_cine");

  if (!token) {
    mensajeFormulario.value = {
      texto: "Debes iniciar sesión para dejar una reseña.",
      tipo: "error",
    };
    return;
  }

  enviandoComentario.value = true;

  try {
    const configuracion = {
      headers: {
        "x-api-key": "mi_super_api_key_fija_123",
        Authorization: `Bearer ${token}`,
      },
    };

    const payload = {
      id_pelicula: Number(route.params.id),
      titulo: nuevoComentario.value.titulo,
      comentario: nuevoComentario.value.comentario,
      calificacion: nuevoComentario.value.calificacion,
    };

    if (editandoId.value) {
      // Si hay un ID guardado, significa que ESTAMOS EDITANDO (PUT)
      await axios.put(
        `http://127.0.0.1:5003/resenas/${editandoId.value}`,
        payload,
        configuracion,
      );
      mensajeFormulario.value = {
        texto: "¡Comentario actualizado con éxito!",
        tipo: "exito",
      };
    } else {
      // Si no hay ID, ESTAMOS CREANDO UNO NUEVO (POST)
      await axios.post("http://127.0.0.1:5003/resenas", payload, configuracion);
      mensajeFormulario.value = {
        texto: "¡Comentario publicado con éxito!",
        tipo: "exito",
      };
    }

    limpiarFormulario();
    mostrarFormulario.value = false; // Ocultamos el formulario al terminar
    await cargarComentarios();
  } catch (err) {
    console.error(err);
    const mensajeError =
      err.response?.data?.error || "Ocurrió un error al enviar tu reseña.";
    mensajeFormulario.value = { texto: mensajeError, tipo: "error" };
  } finally {
    enviandoComentario.value = false;
  }
};

// --- NUEVO: Función para dibujar las estrellas ---
const mostrarEstrellas = (calificacion) => {
  const puntos = Number(calificacion) || 0;
  // Repite la estrella llena 'puntos' veces y la vacía el resto hasta llegar a 5
  return "★".repeat(puntos) + "☆".repeat(5 - puntos);
};

// No olvides ejecutar obtenerUsuarioDeToken en el onMounted:
onMounted(() => {
  cargarDetalles();
  cargarComentarios();
  obtenerUsuarioDeToken(); // Agregamos esto
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
                <span class="estrella">★</span>
                {{ Number(pelicula.calificacion).toFixed(1) }} / 5.0
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

              <a
                class="btn-boletos"
                href="https://www.cinecolombia.com/"
                target="_blank"
                >Ir al cine</a
              >
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

          <div class="acciones-cabecera-comentarios">
            <button @click="alternarFormulario" class="btn-primario">
              {{ mostrarFormulario ? "❌ Cancelar" : "✍️ Agregar comentario" }}
            </button>
          </div>

          <div v-if="mostrarFormulario" class="formulario-comentario">
            <h3>{{ editandoId ? "Editar tu reseña" : "Deja tu reseña" }}</h3>

            <div
              v-if="mensajeFormulario.texto"
              :class="['alerta', mensajeFormulario.tipo]"
            >
              {{ mensajeFormulario.texto }}
            </div>

            <form @submit.prevent="enviarResena">
              <div class="grupo-input">
                <label>Calificación:</label>
                <select v-model="nuevoComentario.calificacion" required>
                  <option value="5">⭐⭐⭐⭐⭐ (5) ¡Excelente!</option>
                  <option value="4">⭐⭐⭐⭐ (4) Muy buena</option>
                  <option value="3">⭐⭐⭐ (3) Buena</option>
                  <option value="2">⭐⭐ (2) Regular</option>
                  <option value="1">⭐ (1) Mala</option>
                </select>
              </div>

              <div class="grupo-input">
                <label>Título de tu reseña:</label>
                <input
                  type="text"
                  v-model="nuevoComentario.titulo"
                  placeholder="Ej: Me encantó esta película"
                  required
                  maxlength="150"
                />
              </div>

              <div class="grupo-input">
                <label>Comentario:</label>
                <textarea
                  v-model="nuevoComentario.comentario"
                  placeholder="¿Qué te pareció la película?..."
                  rows="4"
                  required
                ></textarea>
              </div>

              <button
                type="submit"
                class="btn-primario btn-enviar"
                :disabled="enviandoComentario"
              >
                {{
                  enviandoComentario
                    ? "Guardando..."
                    : editandoId
                      ? "Guardar Cambios"
                      : "Publicar Reseña"
                }}
              </button>
            </form>
          </div>

          <div class="lista-comentarios">
            <div
              class="comentario-item"
              v-for="comentario in comentarios"
              :key="comentario.id"
            >
              <div class="cabecera-comentario">
                <div class="info-cabecera">
                  <h4 class="titulo-comentario">{{ comentario.titulo }}</h4>
                  <span
                    class="estrellas-comentario"
                    :title="'Calificación: ' + comentario.calificacion + '/5'"
                  >
                    {{ mostrarEstrellas(comentario.calificacion) }}
                  </span>
                </div>
                <span class="fecha">{{ comentario.fecha }}</span>
              </div>
              <p class="texto-comentario">{{ comentario.texto }}</p>

              <div class="pie-comentario">
                <span class="usuario"
                  >Por: <strong>@{{ comentario.usuario }}</strong></span
                >

                <div
                  class="acciones-propias"
                  v-if="usuarioActualId === comentario.id_usuario"
                >
                  <button
                    class="btn-accion editar"
                    @click="prepararEdicion(comentario)"
                  >
                    ✏️ Editar
                  </button>
                  <button
                    class="btn-accion eliminar"
                    @click="confirmarEliminacion(comentario.id)"
                  >
                    🗑️ Eliminar
                  </button>
                </div>
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
    <div
      v-if="mostrarModalEliminar"
      class="modal-overlay"
      @click.self="cerrarModalEliminar"
    >
      <div class="modal-confirmacion">
        <h3>¿Eliminar comentario?</h3>
        <p>
          Esta acción no se puede deshacer. ¿Estás seguro de que quieres borrar
          tu reseña?
        </p>
        <div class="acciones-modal">
          <button class="btn-secundario" @click="cerrarModalEliminar">
            Cancelar
          </button>
          <button class="btn-primario btn-peligro" @click="ejecutarEliminacion">
            Sí, eliminar
          </button>
        </div>
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

/* CARTELERA */
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

/* ESTILOS PARA EL FORMULARIO DE COMENTARIOS */
.formulario-comentario {
  background-color: #f8fafc;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  margin-bottom: 2rem;
}
.formulario-comentario h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #1a1a1a;
}
.grupo-input {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}
.grupo-input label {
  font-weight: bold;
  margin-bottom: 0.3rem;
  color: #333;
  font-size: 0.9rem;
}
.grupo-input input,
.grupo-input select,
.grupo-input textarea {
  padding: 0.8rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-family: inherit;
  font-size: 1rem;
}
.btn-enviar {
  width: 100%;
  justify-content: center;
  margin-top: 0.5rem;
}
.alerta {
  padding: 0.8rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-weight: bold;
  text-align: center;
}
.alerta.error {
  background-color: #fee2e2;
  color: #b91c1c;
  border: 1px solid #f87171;
}
.alerta.exito {
  background-color: #dcfce7;
  color: #15803d;
  border: 1px solid #4ade80;
}

/* NUEVOS ESTILOS PARA ACCIONES DE COMENTARIOS */
.acciones-cabecera-comentarios {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}
.pie-comentario {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding-top: 0.8rem;
  border-top: 1px solid #f1f1f1;
}
.acciones-propias {
  display: flex;
  gap: 0.5rem;
}
.btn-accion {
  background: none;
  border: none;
  font-size: 0.85rem;
  font-weight: bold;
  cursor: pointer;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}
.btn-accion.editar {
  color: #0ea5e9;
  background-color: #e0f2fe;
}
.btn-accion.editar:hover {
  background-color: #bae6fd;
}
.btn-accion.eliminar {
  color: #e50914;
  background-color: #fee2e2;
}
.btn-accion.eliminar:hover {
  background-color: #fecaca;
}

/* ESTILOS PARA EL MODAL DE CONFIRMACIÓN */
.modal-confirmacion {
  background-color: white;
  padding: 2.5rem 2rem;
  border-radius: 8px;
  max-width: 400px;
  width: 90%;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  /* Aseguramos que quede por encima del overlay */
  position: relative;
  z-index: 1001;
}

.modal-confirmacion h3 {
  margin-top: 0;
  color: #1a1a1a;
  font-size: 1.4rem;
  margin-bottom: 1rem;
}

.modal-confirmacion p {
  color: #555;
  margin-bottom: 2rem;
  line-height: 1.5;
  font-size: 1rem;
}

.acciones-modal {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.btn-peligro {
  background-color: #e50914;
}

.btn-peligro:hover {
  background-color: #b8070f;
}

/* ESTILOS PARA LAS ESTRELLAS EN LOS COMENTARIOS */
.info-cabecera {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.estrellas-comentario {
  color: #f5c518; /* Amarillo clásico de cine */
  font-size: 1.1rem;
  letter-spacing: 2px; /* Un poco de espacio entre estrellas */
}
</style>
