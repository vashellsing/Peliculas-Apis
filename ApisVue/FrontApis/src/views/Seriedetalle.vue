<script setup>
// ==========================================
// HERRAMIENTAS NECESARIAS
// ==========================================
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

// Para saber la direccion web en la que estamos y sacar el ID de la serie
const route = useRoute();

// ==========================================
// CONFIGURACION PARA CONECTARNOS AL SERVIDOR
// ==========================================
const config = {
  headers: { "x-api-key": "mi_super_api_key_fija_123" },
};

// ==========================================
// CAJAS PARA GUARDAR LOS DATOS DE LA SERIE
// ==========================================
const serie = ref(null);
const cargando = ref(true);
const error = ref("");
const mostrarModal = ref(false);
const temporadaAbierta = ref(null);

// ==========================================
// CAJAS PARA COMENTARIOS Y FORMULARIOS
// ==========================================
const comentarios = ref([]);
const mostrarFormulario = ref(false);
const editandoId = ref(null);
const enviandoComentario = ref(false);
const mensajeFormulario = ref({ texto: "", tipo: "" });

const nuevoComentario = ref({
  titulo: "",
  comentario: "",
  calificacion: "serie.calificacion",
});

// ==========================================
// CAJAS PARA CONTROL DEL USUARIO Y ELIMINACION
// ==========================================
const usuarioActualId = ref(null);
const mostrarModalEliminar = ref(false);
const comentarioAEliminar = ref(null);

// ==========================================
// CALCULOS AUTOMATICOS DE LA PAGINA
// ==========================================
// Revisa si el usuario tiene su pase de entrada guardado
const usuarioLogueado = computed(() => {
  return !!localStorage.getItem("token_cine");
});

// Acomoda el enlace del video para poder verlo dentro de la pagina
const trailerSerieEmbedUrl = computed(() => {
  if (!serie.value || !serie.value.trailer) return "";
  const urlParams = new URLSearchParams(new URL(serie.value.trailer).search);
  const videoId = urlParams.get("v");
  return videoId ? `https://www.youtube.com/embed/${videoId}?autoplay=1` : "";
});

// Organiza las temporadas y los episodios para que se vean bonitos
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

// Suma todos los episodios de todas las temporadas
const totalEpisodios = computed(() =>
  temporadas.value.reduce((acc, t) => acc + t.episodios.length, 0),
);

// Saca la lista de actores de la serie
const actores = computed(() => {
  return Array.isArray(serie.value?.actores) ? serie.value.actores : [];
});

// ==========================================
// CONTROL DE LAS PANTALLAS Y MENUS
// ==========================================
// Abre la pantalla oscura para ver el video
const abrirTrailer = () => {
  if (serie.value?.trailer) {
    mostrarModal.value = true;
  } else {
    alert("Esta serie no tiene trailer disponible.");
  }
};

// Cierra la pantalla del video
const cerrarModal = () => {
  mostrarModal.value = false;
};

// Abre o cierra la lista de episodios de una temporada al hacer clic
const toggleTemporada = (id) => {
  temporadaAbierta.value = temporadaAbierta.value === id ? null : id;
};

// Muestra o esconde la zona para escribir una opinion
const alternarFormulario = () => {
  mostrarFormulario.value = !mostrarFormulario.value;
  if (!mostrarFormulario.value) {
    resetFormulario();
  }
};

// Vacia el texto del formulario para dejarlo limpio
const resetFormulario = () => {
  nuevoComentario.value = { titulo: "", comentario: "", calificacion: "5" };
  editandoId.value = null;
  mensajeFormulario.value = { texto: "", tipo: "" };
};

// ==========================================
// DIBUJAR ESTRELLAS Y LEER EL PASE
// ==========================================
// Transforma la nota en estrellitas pintadas y vacias
const mostrarEstrellas = (calificacion) => {
  const puntos = Number(calificacion) || 0;
  return "★".repeat(puntos) + "☆".repeat(5 - puntos);
};

// Lee el pase secreto del usuario para saber quien es
const obtenerUsuarioDeToken = () => {
  const token = localStorage.getItem("token_cine");
  if (token) {
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      usuarioActualId.value = payload.id;
    } catch (e) {
      console.error("Error al decodificar token", e);
    }
  }
};

// ==========================================
// CORREGIR Y EDITAR OPINIONES
// ==========================================
// Pone el texto que ya habias escrito en el formulario para modificarlo
const prepararEdicion = (comentario) => {
  nuevoComentario.value = {
    titulo: comentario.titulo,
    comentario: comentario.texto || comentario.comentario,
    calificacion: comentario.calificacion,
  };
  editandoId.value = comentario.id;
  mostrarFormulario.value = true;
};

// ==========================================
// BORRAR OPINIONES
// ==========================================
// Abre el aviso preguntando si estas seguro de borrar
const confirmarEliminacion = (id_comentario) => {
  comentarioAEliminar.value = id_comentario;
  mostrarModalEliminar.value = true;
};

// Cierra el aviso sin borrar nada
const cerrarModalEliminar = () => {
  mostrarModalEliminar.value = false;
  comentarioAEliminar.value = null;
};

// Va al servidor y quita el comentario para siempre
const ejecutarEliminacion = async () => {
  if (!comentarioAEliminar.value) return;

  const token = localStorage.getItem("token_cine");
  try {
    const configHeaders = {
      headers: {
        "x-api-key": "mi_super_api_key_fija_123",
        Authorization: `Bearer ${token}`,
      },
    };

    await axios.delete(
      `http://127.0.0.1:5003/resenas/${comentarioAEliminar.value}`,
      configHeaders,
    );
    await cargarResenas();
    cerrarModalEliminar();
  } catch (err) {
    console.error("Error eliminando comentario", err);
    alert(err.response?.data?.error || "No se pudo eliminar el comentario");
  }
};

// ==========================================
// PEDIR DATOS AL SERVIDOR
// ==========================================
// Trae toda la informacion de la serie
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

// Trae las opiniones de la gente sobre esta serie
const cargarResenas = async () => {
  try {
    const id = route.params.id;
    const url = `http://127.0.0.1:5003/resenas/serie/${id}`;

    const respuesta = await axios.get(url, config);
    comentarios.value = respuesta.data.comentarios;
  } catch (err) {
    console.error("Error al cargar las resenas de la serie:", err);
    comentarios.value = [];
  }
};

// ==========================================
// ENVIAR O GUARDAR TU OPINION
// ==========================================
const enviarResena = async () => {
  try {
    enviandoComentario.value = true;
    mensajeFormulario.value = { texto: "", tipo: "" };

    const token = localStorage.getItem("token_cine");
    if (!token) {
      mensajeFormulario.value = {
        texto: "Debes iniciar sesion para comentar.",
        tipo: "error",
      };
      return;
    }

    const configAuth = {
      headers: {
        "x-api-key": "mi_super_api_key_fija_123",
        Authorization: `Bearer ${token}`,
      },
    };

    const payload = {
      id_serie: Number(route.params.id),
      titulo: nuevoComentario.value.titulo,
      comentario: nuevoComentario.value.comentario,
      calificacion: parseInt(nuevoComentario.value.calificacion),
    };

    if (editandoId.value) {
      // Si estamos corrigiendo una opinion vieja
      const urlPut = `http://127.0.0.1:5003/resenas/${editandoId.value}`;
      await axios.put(urlPut, payload, configAuth);
      mensajeFormulario.value = {
        texto: "¡Resena actualizada con exito!",
        tipo: "exito",
      };
    } else {
      // Si estamos escribiendo una opinion nueva
      const urlPost = "http://127.0.0.1:5003/resenas";
      await axios.post(urlPost, payload, configAuth);
      mensajeFormulario.value = {
        texto: "¡Comentario publicado con exito!",
        tipo: "exito",
      };
    }

    cargarResenas();

    // Esperamos un momento breve antes de cerrar el formulario solito
    setTimeout(() => {
      alternarFormulario();
    }, 1500);
  } catch (err) {
    console.error("Error al guardar el comentario:", err);
    mensajeFormulario.value = {
      texto:
        err?.response?.data?.error || "Ocurrio un error al guardar tu resena.",
      tipo: "error",
    };
  } finally {
    enviandoComentario.value = false;
  }
};

// ==========================================
// TAREAS AL ABRIR LA PANTALLA
// ==========================================
// Apenas arranca la pagina, busca toda la informacion de golpe
onMounted(() => {
  cargarSerie();
  cargarResenas();
  obtenerUsuarioDeToken();
});
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
                <span class="estrella">★</span> {{ serie.calificacion }} / 5
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

          <div v-if="usuarioLogueado" class="acciones-cabecera-comentarios">
            <button @click="alternarFormulario" class="btn-primario">
              {{ mostrarFormulario ? "❌ Cancelar" : "✍️ Agregar comentario" }}
            </button>
          </div>

          <div v-else class="estado pequeño">
            Inicia sesión para dejar tu comentario sobre esta serie.
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
                  placeholder="Ej: Me encantó esta serie"
                  required
                  maxlength="150"
                />
              </div>

              <div class="grupo-input">
                <label>Comentario:</label>
                <textarea
                  v-model="nuevoComentario.comentario"
                  placeholder="¿Qué te pareció la serie?..."
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
          <div v-if="comentarios.length === 0" class="estado pequeño">
            Aún no hay comentarios. ¡Sé el primero en opinar!
          </div>

          <div v-else class="lista-comentarios">
            <div
              v-for="comentario in comentarios"
              :key="comentario.id || comentario.id_comentario"
              class="comentario-item"
            >
              <div class="cabecera-comentario">
                <div class="info-cabecera">
                  <h4 class="titulo-comentario">
                    {{ comentario.titulo || "Sin título" }}
                  </h4>

                  <span
                    class="estrellas-comentario"
                    :title="`Calificación: ${comentario.calificacion || comentario.puntuacion || 'N/A'}/5`"
                  >
                    {{
                      mostrarEstrellas(
                        comentario.calificacion || comentario.puntuacion,
                      )
                    }}
                  </span>
                </div>

                <span class="fecha">
                  {{
                    comentario.fecha ||
                    comentario.fecha_creacion ||
                    comentario.creado_en ||
                    "Reciente"
                  }}
                </span>
              </div>

              <p class="texto-comentario">
                {{ comentario.comentario || comentario.texto }}
              </p>

              <div class="pie-comentario">
                <span class="usuario">
                  Por: @{{
                    comentario.nombre_usuario ||
                    comentario.username ||
                    comentario.usuario ||
                    "Anónimo"
                  }}
                </span>

                <div
                  v-if="comentario.id_usuario === usuarioActualId"
                  class="acciones-propias"
                >
                  <button
                    @click="prepararEdicion(comentario)"
                    class="btn-accion editar"
                  >
                    ✏️ Editar
                  </button>
                  <button
                    @click="
                      confirmarEliminacion(
                        comentario.id || comentario.id_comentario,
                      )
                    "
                    class="btn-accion eliminar"
                  >
                    🗑️ Eliminar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>
        <div v-if="mostrarModalEliminar" class="modal-overlay">
          <div class="modal-confirmacion">
            <h3>¿Eliminar reseña?</h3>
            <p>
              ¿Estás seguro de que deseas eliminar este comentario? Esta acción
              no se puede deshacer.
            </p>
            <div class="acciones-modal">
              <button @click="cerrarModalEliminar" class="btn-secundario">
                Cancelar
              </button>
              <button @click="ejecutarEliminacion" class="btn-peligro">
                Sí, eliminar
              </button>
            </div>
          </div>
        </div>
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
/* ==========================================================================
   1. CONTENEDORES GLOBALES Y TIPOGRAFÍA
   ========================================================================== */
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

/* ==========================================================================
   2. ELEMENTOS UI GLOBALES (Botones y Alertas)
   ========================================================================== */
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

.btn-peligro {
  background-color: #e50914;
  color: white;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-peligro:hover {
  background-color: #b8070f;
}

.alerta {
  padding: 0.8rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-weight: bold;
  text-align: center;
}

.alerta.exito {
  background-color: #dcfce7;
  color: #15803d;
  border: 1px solid #4ade80;
}

.alerta.error {
  background-color: #fee2e2;
  color: #b91c1c;
  border: 1px solid #f87171;
}

/* ==========================================================================
   3. CABECERA E INFO PRINCIPAL
   ========================================================================== */
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

.acciones-calificacion {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: auto;
  flex-wrap: wrap;
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

/* ==========================================================================
   4. SECCIÓN: TEMPORADAS Y EPISODIOS
   ========================================================================== */
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

/* ==========================================================================
   5. SECCIÓN: REPARTO
   ========================================================================== */
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

/* ==========================================================================
   6. SECCIÓN: COMENTARIOS Y FORMULARIO
   ========================================================================== */
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

.info-cabecera {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.estrellas-comentario {
  color: #f5c518;
  font-size: 1.1rem;
  letter-spacing: 2px;
  margin-bottom: 0.8rem;
}

.texto-comentario {
  color: #555;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.pie-comentario {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding-top: 0.8rem;
  border-top: 1px solid #f1f1f1;
}

.usuario {
  font-size: 0.9rem;
  color: #666;
}

.acciones-cabecera-comentarios {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
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
  display: flex;
  align-items: center;
  gap: 0.3rem;
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

/* Formulario de comentarios */
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

/* ==========================================================================
   7. MODALES (Tráiler y Confirmación)
   ========================================================================== */
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
  transition:
    transform 0.2s,
    color 0.2s;
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

.modal-confirmacion {
  background-color: white;
  padding: 2.5rem 2rem;
  border-radius: 8px;
  max-width: 400px;
  width: 90%;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  position: relative;
  z-index: 1001;
}

.modal-confirmacion h3 {
  margin-top: 0;
  color: #1a1a1a;
  font-size: 1.4rem;
  margin-bottom: 1rem;
}

.modal-confirmacion.error h3 {
  color: #e50914;
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
</style>
