<script setup>
import { ref, computed, onMounted, watch } from "vue";
import Swal from "sweetalert2";
import axios from "axios";


// Esta variable nos dice en que pestana esta el administrador (peliculas, series, etc)
const menuActivo = ref("peliculas");

// ==========================================
// CONTROL DE PAGINAS (PAGINACION)
// ==========================================
const paginaActual = ref(1);
const elementosPorPagina = 20;

// Si el administrador cambia de seccion, lo regresamos a la pagina uno automaticamente
watch(menuActivo, () => {
  paginaActual.value = 1;
});

// ==========================================
// CAJONES PARA GUARDAR LA INFORMACION
// ==========================================
// Aqui guardaremos lo que nos entregue el servidor
const datosPeliculas = ref([]);
const datosSeries = ref([]);
const datosCines = ref([]);
const datosCarteleras = ref([]);

// Atajos para que la pantalla encuentre las listas facilmente
const peliculas = computed(() => datosPeliculas.value);
const cines = computed(() => datosCines.value);

// Herramienta para saber cual de los cajones estamos mirando en este momento
const getArrayActivo = () => {
  if (menuActivo.value === "peliculas") return datosPeliculas;
  if (menuActivo.value === "series") return datosSeries;
  if (menuActivo.value === "cines") return datosCines;
  if (menuActivo.value === "cartelera") return datosCarteleras;
};

// Herramienta para saber el nombre de la identificacion segun la seccion
// const getIdKey = () => {
//   if (menuActivo.value === "peliculas") return "id";
//   if (menuActivo.value === "series") return "id";
//   if (menuActivo.value === "cines") return "id_cine";
//   if (menuActivo.value === "cartelera") return "id_cartelera";
// };

// La lista completa de lo que estamos viendo
const listaActual = computed(() => getArrayActivo().value);

// Recortamos la lista completa para mostrar solo 20 elementos a la vez
const listaPaginada = computed(() => {
  const inicio = (paginaActual.value - 1) * elementosPorPagina;
  const fin = inicio + elementosPorPagina;
  return listaActual.value.slice(inicio, fin);
});

// Calculamos cuantas paginas en total se necesitan
const totalPaginas = computed(() => {
  return Math.ceil(listaActual.value.length / elementosPorPagina);
});

// ==========================================
// TRAER INFORMACION DEL SERVIDOR
// ==========================================
const cargarPeliculas = async () => {
  try {
    const paseDeSeguridad = localStorage.getItem("token_cine");
    if (!paseDeSeguridad) return;

    const opciones = {
      headers: {
        "x-api-key": "mi_super_api_key_fija_123",
        Authorization: `Bearer ${paseDeSeguridad}`,
      },
    };

    const direccion = "http://127.0.0.1:5000/peliculas";
    const respuesta = await axios.get(direccion, opciones);
    datosPeliculas.value = respuesta.data.peliculas;
  } catch (problema) {
    console.error("Fallo al traer las peliculas:", problema);
  }
};

const cargarSeries = async () => {
  try {
    const paseDeSeguridad = localStorage.getItem("token_cine");
    if (!paseDeSeguridad) return;

    const opciones = {
      headers: {
        "x-api-key": "mi_super_api_key_fija_123",
        Authorization: `Bearer ${paseDeSeguridad}`,
      },
    };

    const direccion = "http://127.0.0.1:5001/series";
    const respuesta = await axios.get(direccion, opciones);
    datosSeries.value = respuesta.data.series;
  } catch (problema) {
    console.error("Fallo al traer las series:", problema);
  }
};

const cargarCines = async () => {
  try {
    const paseDeSeguridad = localStorage.getItem("token_cine");
    const opciones = {
      headers: {
        "x-api-key": "mi_super_api_key_fija_123",
        Authorization: paseDeSeguridad ? `Bearer ${paseDeSeguridad}` : "",
      },
    };

    const direccion = "http://127.0.0.1:5002/cines";
    const respuesta = await axios.get(direccion, opciones);
    datosCines.value = respuesta.data.cines;
  } catch (problema) {
    console.error("Fallo al traer los cines:", problema);
  }
};

const cargarCarteleras = async () => {
  try {
    const paseDeSeguridad = localStorage.getItem("token_cine");
    const opciones = {
      headers: {
        "x-api-key": "mi_super_api_key_fija_123",
        Authorization: paseDeSeguridad ? `Bearer ${paseDeSeguridad}` : "",
      },
    };

    const direccion = "http://127.0.0.1:5002/cartelera";
    const respuesta = await axios.get(direccion, opciones);

    // Ajustamos la informacion para que sea facil de leer en la pantalla
    datosCarteleras.value = respuesta.data.cartelera.map((elemento) => ({
      id_cartelera: elemento.id_cartelera,
      id_peliculaCartelera: elemento.pelicula,
      id_cineCartelera: elemento.cine,
      linkCine: elemento.link_cine,
      fecha_horaCartelera: elemento.fecha_hora,
      idioma_proyeccionCartelera: elemento.idioma,
    }));
  } catch (problema) {
    console.error("Fallo al traer las carteleras:", problema);
  }
};

// Apenas se abra la pantalla, traemos toda la informacion
onMounted(() => {
  cargarPeliculas();
  cargarSeries();
  cargarCines();
  cargarCarteleras();
});

// ==========================================
// CONTROL DE LA VENTANA EMERGENTE (FORMULARIO)
// ==========================================
const modalVisible = ref(false);
const esEdicion = ref(false); // Nos dice si estamos creando algo nuevo o modificando algo viejo
const formulario = ref({}); // Aqui guardamos lo que el usuario escribe

// Prepara un formulario en blanco para crear algo nuevo
const abrirModalAgregar = () => {
  esEdicion.value = false;

  if (menuActivo.value === "peliculas") {
    formulario.value = {
      id: null,
      titulo: "",
      titulo_original: "",
      sinopsis: "",
      anio: new Date().getFullYear(),
      actores: [],
      genero: "Otro",
      idioma: "Otro",
      poster: "",
      lema: "",
      trailer: "",
    };
  } else if (menuActivo.value === "series") {
    formulario.value = {
      id: null,
      titulo: "",
      titulo_original: "",
      sinopsis: "",
      anio: new Date().getFullYear(),
      episodiosSerie: [],
      actores: [],
      genero: "Otro",
      idioma: "Otro",
      poster: "",
      trailer: "",
    };
  } else if (menuActivo.value === "cines") {
    formulario.value = {
      id_cine: null,
      nombreCine: "",
      direccionCine: "",
      ciudadCine: "",
      linkWeb: "",
    };
  } else if (menuActivo.value === "cartelera") {
    formulario.value = {
      id_cartelera: null,
      id_peliculaCartelera: "",
      id_cineCartelera: "",
      fecha_horaCartelera: "",
      idioma_proyeccionCartelera: "Doblada al Espanol",
    };
  }

  modalVisible.value = true;
};

// Prepara el formulario con la informacion de un elemento que queremos modificar
const abrirModalEditar = (elemento) => {
  esEdicion.value = true;
  // Hacemos una copia exacta para no alterar la lista original por accidente
  formulario.value = JSON.parse(JSON.stringify(elemento));

  // Ajustes especiales para que la informacion se vea bien en el formulario

  // Convertimos el texto de actores en una lista real
  let actoresBorrador = formulario.value.actores;
  if (typeof actoresBorrador === "string") {
    try {
      actoresBorrador = JSON.parse(actoresBorrador);
    } catch (e) {
      actoresBorrador = [];
    }
  }
  formulario.value.actores = Array.isArray(actoresBorrador)
    ? actoresBorrador
    : [];

  //  Ajustes exclusivos para las series
  if (menuActivo.value === "series") {
    let episodiosBorrador = formulario.value.temporadas_info || [];
    if (typeof episodiosBorrador === "string") {
      try {
        episodiosBorrador = JSON.parse(episodiosBorrador);
      } catch (e) {
        episodiosBorrador = [];
      }
    }
    formulario.value.episodiosSerie = Array.isArray(episodiosBorrador)
      ? episodiosBorrador
      : [];
    formulario.value.poster = formulario.value.imagenUrl || "";
  }

  //  Ajustes exclusivos para las funciones de cine
  if (menuActivo.value === "cartelera") {
    // Buscamos a que pelicula y a que cine corresponden los textos
    const peliEncontrada = datosPeliculas.value.find(
      (p) => p.titulo === elemento.id_peliculaCartelera,
    );
    const cineEncontrado = datosCines.value.find(
      (c) => c.nombreCine === elemento.id_cineCartelera,
    );

    // Asignamos los numeros correspondientes para que las listas desplegables funcionen
    formulario.value.id_peliculaCartelera = peliEncontrada
      ? peliEncontrada.id
      : "";
    formulario.value.id_cineCartelera = cineEncontrado
      ? cineEncontrado.id_cine
      : "";

    // Ponemos una letra T en la fecha para que el calendario del navegador la entienda
    if (formulario.value.fecha_horaCartelera) {
      formulario.value.fecha_horaCartelera =
        formulario.value.fecha_horaCartelera.replace(" ", "T");
    }
  }

  modalVisible.value = true;
};

const cerrarModal = () => (modalVisible.value = false);

// ==========================================
// GUARDAR LOS CAMBIOS EN EL SERVIDOR
// ==========================================
const guardarCambios = async () => {
  try {
    const paseDeSeguridad = localStorage.getItem("token_cine");
    if (!paseDeSeguridad) {
      alert("No tienes permisos de administrador.");
      return;
    }

    const opciones = {
      headers: {
        "x-api-key": "mi_super_api_key_fija_123",
        Authorization: `Bearer ${paseDeSeguridad}`,
      },
    };

    if (menuActivo.value === "peliculas") {
      const datosAEnviar = {
        titulo: formulario.value.titulo,
        titulo_original: formulario.value.titulo_original,
        sinopsis: formulario.value.sinopsis,
        anio: formulario.value.anio,
        actores: formulario.value.actores,
        genero: formulario.value.genero,
        idioma: formulario.value.idioma,
        poster: formulario.value.poster,
        lema: formulario.value.lema,
        trailer: formulario.value.trailer,
      };

      if (!esEdicion.value) {
        const direccion = "http://127.0.0.1:5000/peliculas/agregar";
        const respuesta = await axios.post(direccion, datosAEnviar, opciones);
        alert(respuesta.data.mensaje || "Pelicula creada exitosamente");
      } else {
        const direccion = `http://127.0.0.1:5000/peliculas/editar/${formulario.value.id}`;
        const respuesta = await axios.put(direccion, datosAEnviar, opciones);
        alert(respuesta.data.mensaje || "Pelicula actualizada");
      }
      cerrarModal();
      cargarPeliculas();
    } else if (menuActivo.value === "series") {
      const datosAEnviar = {
        titulo: formulario.value.titulo,
        titulo_original: formulario.value.titulo_original,
        sinopsis: formulario.value.sinopsis,
        anio: formulario.value.anio,
        temporadas: formulario.value.temporadas,
        episodiosSerie: formulario.value.episodiosSerie,
        actores: formulario.value.actores,
        genero: formulario.value.genero,
        idioma: formulario.value.idioma,
        poster: formulario.value.poster,
        trailer: formulario.value.trailer,
      };

      if (!esEdicion.value) {
        const direccion = "http://127.0.0.1:5001/series";
        const respuesta = await axios.post(direccion, datosAEnviar, opciones);
        alert(respuesta.data.mensaje || "Serie creada exitosamente");
      } else {
        const direccion = `http://127.0.0.1:5001/series/${formulario.value.id}`;
        const respuesta = await axios.put(direccion, datosAEnviar, opciones);
        alert(respuesta.data.mensaje || "Serie actualizada");
      }
      cerrarModal();
      cargarSeries();
    } else if (menuActivo.value === "cines") {
      const datosAEnviar = {
        nombreCine: formulario.value.nombreCine,
        direccionCine: formulario.value.direccionCine,
        ciudadCine: formulario.value.ciudadCine,
        linkWeb: formulario.value.linkWeb,
      };

      if (!esEdicion.value) {
        const direccion = "http://127.0.0.1:5002/cines";
        const respuesta = await axios.post(direccion, datosAEnviar, opciones);
        alert(respuesta.data.mensaje || "Cine creado exitosamente");
      } else {
        const direccion = `http://127.0.0.1:5002/cines/${formulario.value.id_cine}`;
        const respuesta = await axios.put(direccion, datosAEnviar, opciones);
        alert(respuesta.data.mensaje || "Cine actualizado");
      }
      cerrarModal();
      cargarCines();
    } else if (menuActivo.value === "cartelera") {
      const datosAEnviar = {
        id_pelicula: formulario.value.id_peliculaCartelera,
        id_cine: formulario.value.id_cineCartelera,
        // Quitamos la letra T de la fecha para que la base de datos no tenga problemas
        fecha_hora: formulario.value.fecha_horaCartelera.replace("T", " "),
        idioma: formulario.value.idioma_proyeccionCartelera,
      };

      if (!esEdicion.value) {
        const direccion = "http://127.0.0.1:5002/cartelera";
        const respuesta = await axios.post(direccion, datosAEnviar, opciones);
        alert(respuesta.data.mensaje || "Funcion programada exitosamente");
      } else {
        const direccion = `http://127.0.0.1:5002/cartelera/${formulario.value.id_cartelera}`;
        const respuesta = await axios.put(direccion, datosAEnviar, opciones);
        alert(respuesta.data.mensaje || "Funcion en cartelera actualizada");
      }
      cerrarModal();
      cargarCarteleras();
    }
  } catch (problema) {
    console.error("Error al guardar:", problema);
    alert(
      "Error: " + (problema.response?.data?.error || "Ocurrio un problema"),
    );
  }
};

// ==========================================
// 7. BORRAR INFORMACION (ELIMINAR)
// ==========================================
const modalEliminarVisible = ref(false);
const idAEliminar = ref(null);

// Muestra el mensaje para estar seguros antes de borrar
const solicitarEliminar = (identificacion) => {
  idAEliminar.value = identificacion;
  modalEliminarVisible.value = true;
};

const cancelarEliminar = () => {
  modalEliminarVisible.value = false;
  idAEliminar.value = null;
};

// Borra definitivamente la informacion seleccionada
const confirmarEliminar = async () => {
  if (idAEliminar.value) {
    try {
      const paseDeSeguridad = localStorage.getItem("token_cine");
      const opciones = {
        headers: {
          "x-api-key": "mi_super_api_key_fija_123",
          Authorization: `Bearer ${paseDeSeguridad}`,
        },
      };

      if (menuActivo.value === "peliculas") {
        const direccion = `http://127.0.0.1:5000/peliculas/eliminar/${idAEliminar.value}`;
        const respuesta = await axios.delete(direccion, opciones);
        alert(respuesta.data.mensaje || "Pelicula eliminada");
        cargarPeliculas();
      } else if (menuActivo.value === "series") {
        const direccion = `http://127.0.0.1:5001/series/${idAEliminar.value}`;
        const respuesta = await axios.delete(direccion, opciones);
        alert(respuesta.data.mensaje || "Serie eliminada");
        cargarSeries();
      } else if (menuActivo.value === "cines") {
        const direccion = `http://127.0.0.1:5002/cines/${idAEliminar.value}`;
        const respuesta = await axios.delete(direccion, opciones);
        alert(respuesta.data.mensaje || "Cine eliminado");
        cargarCines();
      } else if (menuActivo.value === "cartelera") {
        const direccion = `http://127.0.0.1:5002/cartelera/${idAEliminar.value}`;
        const respuesta = await axios.delete(direccion, opciones);
        alert(respuesta.data.mensaje || "Funcion eliminada");
        cargarCarteleras();
      }

      cancelarEliminar();
    } catch (problema) {
      console.error("Error al eliminar:", problema);
      alert(
        "No se pudo eliminar: " +
          (problema.response?.data?.error || "Ocurrio un problema"),
      );
    }
  }
};

// ==========================================
//  HERRAMIENTAS PARA ACTORES
// ==========================================
// aGREGA un espacio en blanco para registrar un nuevo actor
const agregarActor = () => {
  if (formulario.value.actores.length < 3) {
    formulario.value.actores.push({ nombre: "", personaje: "", foto: "" });
  }
};

// Quita un actor de la lista
const eliminarActor = (posicion) => {
  formulario.value.actores.splice(posicion, 1);
};

// Convierte la lista de actores en un texto ordenado por comas para mostrarlo en pantalla
const formatearActores = (actores) => {
  if (Array.isArray(actores)) {
    return actores.map((actor) => actor.nombre).join(", ");
  }
  return actores || "";
};

// ==========================================
// HERRAMIENTAS PARA SERIES Y CAPITULOS
// ==========================================
const agregarTemporada = () => {
  const nuevoNumero = formulario.value.episodiosSerie.length + 1;
  formulario.value.episodiosSerie.push({
    id: nuevoNumero,
    numero: nuevoNumero,
    titulo: `Temporada ${nuevoNumero}`,
    episodios: [],
  });
};

const eliminarTemporada = (posicion) => {
  formulario.value.episodiosSerie.splice(posicion, 1);
};

const agregarEpisodio = (posicionTemporada) => {
  const temporada = formulario.value.episodiosSerie[posicionTemporada];
  const nuevoNumero = temporada.episodios.length + 1;
  temporada.episodios.push({
    numero: nuevoNumero,
    titulo: "",
    duracion: "",
  });
};

const eliminarEpisodio = (posicionTemporada, posicionEpisodio) => {
  formulario.value.episodiosSerie[posicionTemporada].episodios.splice(
    posicionEpisodio,
    1,
  );
};

// // Cuenta cuantas temporadas hay para mostrar el texto en pantalla
// const formatearTemporadas = (temporadas) => {
//   if (Array.isArray(temporadas)) {
//     return `${temporadas.length} Temporada(s)`;
//   }
//   return "0 Temporadas";
// };
</script>

<template>
  <div class="layout-admin">
    <aside class="sidebar">
      <div class="logo-admin"><h2>AdminPanel</h2></div>
      <nav class="menu-lateral">
        <button
          :class="{ activo: menuActivo === 'peliculas' }"
          @click="menuActivo = 'peliculas'"
        >
          Películas
        </button>
        <button
          :class="{ activo: menuActivo === 'series' }"
          @click="menuActivo = 'series'"
        >
          Series
        </button>
        <button
          :class="{ activo: menuActivo === 'cines' }"
          @click="menuActivo = 'cines'"
        >
          Cines
        </button>
        <button
          :class="{ activo: menuActivo === 'cartelera' }"
          @click="menuActivo = 'cartelera'"
        >
          Carteleras
        </button>
      </nav>
      <div class="sidebar-footer">
        <RouterLink to="/" class="btn-volver">⬅ Volver a la Web</RouterLink>
      </div>
    </aside>

    <main class="contenido-principal">
      <header class="cabecera-contenido">
        <div>
          <h1 class="titulo-seccion">Gestión de {{ menuActivo }}</h1>
          <p class="subtitulo">Aquí se hacen cositas de admin</p>
        </div>
        <button @click="abrirModalAgregar" class="btn-primario">
          + Agregar Nuevo
        </button>
      </header>

      <div class="contenedor-tabla">
        <table class="tabla-admin">
          <thead>
            <tr v-if="menuActivo === 'peliculas'">
              <th>ID</th>
              <th>Título</th>
              <th>T. Original</th>
              <th>Sinopsis</th>
              <th>Año</th>
              <th>Actores</th>
              <th>Género</th>
              <th>Idioma</th>
              <th>Póster</th>
              <th>Lema</th>
              <th>Tráiler</th>
              <th class="texto-centro">Acciones</th>
            </tr>
            <tr v-else-if="menuActivo === 'series'">
              <th>ID</th>
              <th>Título</th>
              <th>T. Original</th>
              <th>Sinopsis</th>
              <th>Año</th>
              <th>Temporadas</th>
              <th>Actores</th>
              <th>Género</th>
              <th>Idioma</th>
              <th class="texto-centro">Acciones</th>
            </tr>
            <tr v-else-if="menuActivo === 'cines'">
              <th>ID</th>
              <th>Nombre</th>
              <th>Dirección</th>
              <th>Ciudad</th>
              <th>Sitio Web</th>
              <th class="texto-centro">Acciones</th>
            </tr>
            <tr v-else-if="menuActivo === 'cartelera'">
              <th>ID</th>
              <th>Película</th>
              <th>Cine</th>
              <th>Sitio Web</th>
              <th>Fecha/Hora</th>
              <th>Idioma</th>
              <th class="texto-centro">Acciones</th>
            </tr>
          </thead>

          <tbody>
            <tr v-if="listaActual.length === 0">
              <td
                colspan="12"
                class="texto-centro"
                style="padding: 2rem; color: #888"
              >
                No hay datos registrados en esta sección.
              </td>
            </tr>
            <tr
              v-for="item in listaPaginada"
              :key="item.id || item.id_cine || item.id_cartelera"
            >
              <template v-if="menuActivo === 'peliculas'">
                <td>#{{ item.id }}</td>
                <td class="font-bold truncar-texto">{{ item.titulo }}</td>
                <td class="truncar-texto">
                  {{ item.titulo_original }}
                </td>
                <td class="truncar-texto" :title="item.sinopsis">
                  {{ item.sinopsis }}
                </td>
                <td>{{ item.anio }}</td>
                <td
                  class="truncar-texto"
                  :title="formatearActores(item.actores)"
                >
                  {{ formatearActores(item.actores) }}
                </td>
                <td>
                  <span class="badge">{{ item.genero }}</span>
                </td>
                <td>{{ item.idioma }}</td>
                <td class="truncar-texto">
                  <a :href="item.poster" target="_blank">Link</a>
                </td>
                <td class="truncar-texto">{{ item.lema }}</td>
                <td class="truncar-texto">
                  <a :href="item.trailer" target="_blank">Ver</a>
                </td>
              </template>

              <template v-else-if="menuActivo === 'series'">
                <td>#{{ item.id }}</td>
                <td class="font-bold truncar-texto">{{ item.titulo }}</td>
                <td class="truncar-texto">
                  {{ item.titulo_original }}
                </td>
                <td class="truncar-texto" :title="item.sinopsis">
                  {{ item.sinopsis }}
                </td>
                <td>{{ item.anio }}</td>
                <td>
                  {{ item.temporadas }}
                </td>
                <td
                  class="truncar-texto"
                  :title="formatearActores(item.actores)"
                >
                  {{ formatearActores(item.actores) }}
                </td>
                <td>
                  <span class="badge">{{ item.genero }}</span>
                </td>
                <td>{{ item.idioma }}</td>
              </template>

              <template v-else-if="menuActivo === 'cines'">
                <td>#{{ item.id_cine }}</td>
                <td class="font-bold">{{ item.nombreCine }}</td>
                <td>{{ item.direccionCine }}</td>
                <td>{{ item.ciudadCine }}</td>
                <td>
                  <a
                    v-if="item.linkWeb"
                    :href="item.linkWeb"
                    target="_blank"
                    style="color: #3b82f6; text-decoration: underline"
                  >
                    🌐 Ver Web
                  </a>
                  <span v-else style="color: gray">-</span>
                </td>
              </template>
              <template v-else-if="menuActivo === 'cartelera'">
                <td>#{{ item.id_cartelera }}</td>
                <td class="font-bold">{{ item.id_peliculaCartelera }}</td>
                <td>{{ item.id_cineCartelera }}</td>
                <td>
                  <a
                    v-if="item.linkCine"
                    :href="item.linkCine"
                    target="_blank"
                    style="color: #3b82f6; text-decoration: underline"
                  >
                    🌐 Visitar
                  </a>
                  <span v-else style="color: gray">-</span>
                </td>
                <td>{{ item.fecha_horaCartelera.replace("T", " ") }}</td>
                <td>
                  <span class="badge">{{
                    item.idioma_proyeccionCartelera
                  }}</span>
                </td>
              </template>

              <td class="celda-acciones">
                <button @click="abrirModalEditar(item)" class="btn-editar">
                  Editar
                </button>
                <button
                  @click="
                    solicitarEliminar(
                      item.id || item.id_cine || item.id_cartelera,
                    )
                  "
                  class="btn-eliminar"
                >
                  Eliminar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="paginacion-admin" v-if="totalPaginas > 1">
        <button
          @click="paginaActual--"
          :disabled="paginaActual === 1"
          class="btn-paginacion"
        >
          ⬅ Anterior
        </button>

        <span class="info-paginacion">
          Página <strong>{{ paginaActual }}</strong> de
          <strong>{{ totalPaginas }}</strong>
        </span>

        <button
          @click="paginaActual++"
          :disabled="paginaActual === totalPaginas"
          class="btn-paginacion"
        >
          Siguiente ➡
        </button>
      </div>
    </main>

    <div class="overlay-modal" v-if="modalVisible">
      <div class="caja-modal scrollable">
        <h3>{{ esEdicion ? "Editar" : "Agregar" }} {{ menuActivo }}</h3>

        <form @submit.prevent="guardarCambios" class="formulario-modal">
          <template v-if="menuActivo === 'peliculas'">
            <div class="grupo-input">
              <label>Título</label>
              <input type="text" v-model="formulario.titulo" required />
            </div>
            <div class="grupo-input">
              <label>Título Original</label>
              <input type="text" v-model="formulario.titulo_original" />
            </div>
            <div class="grupo-input">
              <label>Sinopsis</label>
              <textarea v-model="formulario.sinopsis" rows="3"></textarea>
            </div>
            <div class="fila-input">
              <div class="grupo-input flex-1">
                <label>Año</label>
                <input type="number" v-model="formulario.anio" />
              </div>
              <div class="grupo-input flex-1">
                <label>Género</label>
                <select v-model="formulario.genero">
                  <option
                    v-for="g in [
                      'Accion',
                      'Comedia',
                      'Drama',
                      'Ciencia Ficcion',
                      'Terror',
                      'Romance',
                      'Animacion',
                      'Fantasia',
                      'Documental',
                      'Otro',
                    ]"
                    :key="g"
                    :value="g"
                  >
                    {{ g }}
                  </option>
                </select>
              </div>
            </div>
            <div class="grupo-input">
              <label>Idioma</label>
              <select v-model="formulario.idioma">
                <option
                  v-for="i in [
                    'Espanol',
                    'Ingles',
                    'Japones',
                    'Coreano',
                    'Frances',
                    'Otro',
                  ]"
                  :key="i"
                  :value="i"
                >
                  {{ i }}
                </option>
              </select>
            </div>
            <div class="grupo-input">
              <label>Actores (Máximo 3)</label>

              <div
                v-for="(actor, index) in formulario.actores"
                :key="index"
                style="
                  display: flex;
                  gap: 10px;
                  margin-bottom: 10px;
                  align-items: center;
                "
              >
                <input
                  type="text"
                  v-model="actor.nombre"
                  placeholder="Nombre real"
                  required
                />
                <input
                  type="text"
                  v-model="actor.personaje"
                  placeholder="Personaje"
                  required
                />
                <input
                  type="text"
                  v-model="actor.foto"
                  placeholder="URL de la Foto"
                />

                <button
                  type="button"
                  @click="eliminarActor(index)"
                  class="btn-eliminar"
                  style="padding: 0.5rem"
                >
                  X
                </button>
              </div>

              <button
                v-if="formulario.actores.length < 3"
                type="button"
                @click="agregarActor"
                class="btn-primario"
                style="font-size: 0.8rem; padding: 0.5rem"
              >
                + Añadir Actor
              </button>
            </div>
            <div class="grupo-input">
              <label>URL Póster</label>
              <input type="text" v-model="formulario.poster" />
            </div>
            <div class="grupo-input">
              <label>Lema</label>
              <input type="text" v-model="formulario.lema" />
            </div>
            <div class="grupo-input">
              <label>URL Tráiler</label>
              <input type="text" v-model="formulario.trailer" />
            </div>
          </template>

          <template v-else-if="menuActivo === 'series'">
            <div class="grupo-input">
              <label>Título de la Serie</label>
              <input type="text" v-model="formulario.titulo" required />
            </div>
            <div class="grupo-input">
              <label>Título Original</label>
              <input type="text" v-model="formulario.titulo_original" />
            </div>
            <div class="grupo-input">
              <label>Sinopsis</label>
              <textarea v-model="formulario.sinopsis" rows="3"></textarea>
            </div>
            <div class="fila-input">
              <div class="grupo-input flex-1">
                <label>Año de Lanzamiento</label>
                <input type="number" v-model="formulario.anio" />
              </div>
              <div class="grupo-input">
                <label>Temporadas y Episodios</label>

                <div
                  v-for="(temp, tIndex) in formulario.episodiosSerie"
                  :key="tIndex"
                  style="
                    border: 1px dashed #666;
                    padding: 10px;
                    margin-bottom: 15px;
                    border-radius: 5px;
                  "
                >
                  <div
                    style="
                      display: flex;
                      justify-content: space-between;
                      align-items: center;
                      margin-bottom: 10px;
                    "
                  >
                    <strong>{{ temp.titulo }}</strong>
                    <button
                      type="button"
                      @click="eliminarTemporada(tIndex)"
                      class="btn-eliminar"
                      style="padding: 0.3rem"
                    >
                      Eliminar Temporada
                    </button>
                  </div>

                  <div
                    v-for="(ep, eIndex) in temp.episodios"
                    :key="eIndex"
                    style="
                      display: flex;
                      gap: 10px;
                      margin-bottom: 8px;
                      align-items: center;
                    "
                  >
                    <input
                      type="number"
                      v-model="ep.numero"
                      placeholder="Nº"
                      style="width: 70px"
                      required
                    />
                    <input
                      type="text"
                      v-model="ep.titulo"
                      placeholder="Título del episodio"
                      required
                    />
                    <input
                      type="text"
                      v-model="ep.duracion"
                      placeholder="Duración (ej: 45 min)"
                      style="width: 120px"
                      required
                    />

                    <button
                      type="button"
                      @click="eliminarEpisodio(tIndex, eIndex)"
                      class="btn-eliminar"
                      style="padding: 0.3rem"
                    >
                      X
                    </button>
                  </div>

                  <button
                    type="button"
                    @click="agregarEpisodio(tIndex)"
                    class="btn-primario"
                    style="font-size: 0.8rem; padding: 0.4rem"
                  >
                    + Añadir Episodio
                  </button>
                </div>

                <button
                  type="button"
                  @click="agregarTemporada"
                  class="btn-primario"
                  style="padding: 0.5rem"
                >
                  + Añadir Nueva Temporada
                </button>
              </div>
            </div>
            <div class="fila-input">
              <div class="grupo-input flex-1">
                <label>Género</label>
                <select v-model="formulario.genero">
                  <option
                    v-for="g in [
                      'Accion',
                      'Comedia',
                      'Drama',
                      'Ciencia Ficcion',
                      'Terror',
                      'Romance',
                      'Animacion',
                      'Fantasia',
                      'Documental',
                      'Otro',
                    ]"
                    :key="g"
                    :value="g"
                  >
                    {{ g }}
                  </option>
                </select>
              </div>
              <div class="grupo-input flex-1">
                <label>Idioma</label>
                <select v-model="formulario.idioma">
                  <option
                    v-for="i in [
                      'Espanol',
                      'Ingles',
                      'Japones',
                      'Coreano',
                      'Frances',
                      'Otro',
                    ]"
                    :key="i"
                    :value="i"
                  >
                    {{ i }}
                  </option>
                </select>
              </div>
            </div>
            <div class="grupo-input">
              <label>Actores (Máximo 3)</label>

              <div
                v-for="(actor, index) in formulario.actores"
                :key="index"
                style="
                  display: flex;
                  gap: 10px;
                  margin-bottom: 10px;
                  align-items: center;
                "
              >
                <input
                  type="text"
                  v-model="actor.nombre"
                  placeholder="Nombre real"
                  required
                />
                <input
                  type="text"
                  v-model="actor.personaje"
                  placeholder="Personaje"
                  required
                />
                <input
                  type="text"
                  v-model="actor.foto"
                  placeholder="URL de la Foto"
                />

                <button
                  type="button"
                  @click="eliminarActor(index)"
                  class="btn-eliminar"
                  style="padding: 0.5rem"
                >
                  X
                </button>
              </div>

              <button
                v-if="formulario.actores.length < 3"
                type="button"
                @click="agregarActor"
                class="btn-primario"
                style="font-size: 0.8rem; padding: 0.5rem"
              >
                + Añadir Actor
              </button>
            </div>
            <div class="grupo-input">
              <label>URL Póster</label>
              <input type="text" v-model="formulario.poster" />
            </div>
            <div class="grupo-input">
              <label>URL Tráiler</label>
              <input type="text" v-model="formulario.trailer" />
            </div>
          </template>

          <template v-else-if="menuActivo === 'cines'">
            <div class="grupo-input">
              <label>Nombre del Cine</label>
              <input type="text" v-model="formulario.nombreCine" required />
            </div>
            <div class="grupo-input">
              <label>Dirección</label>
              <input type="text" v-model="formulario.direccionCine" />
            </div>
            <div class="grupo-input">
              <label>Ciudad</label>
              <input type="text" v-model="formulario.ciudadCine" />
            </div>
            <div class="grupo-input">
              <label>Sitio Web (URL)</label>
              <input type="url" v-model="formulario.linkWeb" />
            </div>
          </template>

          <template v-else-if="menuActivo === 'cartelera'">
            <div class="grupo-input">
              <label>Película</label>
              <select v-model.number="formulario.id_peliculaCartelera" required>
                <option disabled value="">Seleccione una película</option>
                <option
                  v-for="peli in peliculas"
                  :key="peli.id"
                  :value="peli.id"
                >
                  {{ peli.titulo }}
                </option>
              </select>
            </div>

            <div class="grupo-input">
              <label>Cine</label>
              <select v-model.number="formulario.id_cineCartelera" required>
                <option disabled value="">Seleccione un cine</option>
                <option
                  v-for="cine in cines"
                  :key="cine.id_cine"
                  :value="cine.id_cine"
                >
                  {{ cine.nombreCine }}
                </option>
              </select>
            </div>

            <div class="grupo-input">
              <label>Fecha y Hora</label>
              <input
                type="datetime-local"
                v-model="formulario.fecha_horaCartelera"
                required
              />
            </div>

            <div class="grupo-input">
              <label>Idioma de Proyección</label>
              <select v-model="formulario.idioma_proyeccionCartelera" required>
                <option value="Doblada al Espanol">Doblada al Español</option>
                <option value="Subtitulada">Subtitulada</option>
                <option value="Idioma Original">Idioma Original</option>
              </select>
            </div>
          </template>

          <div class="acciones-modal">
            <button type="button" @click="cerrarModal" class="btn-cancelar">
              Cancelar
            </button>
            <button type="submit" class="btn-guardar">Confirmar</button>
          </div>
        </form>
      </div>
    </div>

    <div class="overlay-modal" v-if="modalEliminarVisible">
      <div class="caja-modal modal-pequeno">
        <h3 style="color: #cc0000; margin-top: 0">¡Atención!</h3>
        <p>
          ¿Estás seguro de que deseas eliminar este registro? Esta acción no se
          puede deshacer.
        </p>
        <div class="acciones-modal">
          <button @click="cancelarEliminar" class="btn-cancelar">
            No, cancelar
          </button>
          <button @click="confirmarEliminar" class="btn-eliminar-confirmar">
            Sí, eliminar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ========================================== */
/*  ESTRUCTURA PRINCIPAL DE LA PANTALLA     */
/* ========================================== */

/* Contenedor que abarca todo el espacio visible */
.layout-admin {
  display: flex;
  min-height: 100vh;
  font-family: sans-serif;
  background-color: #f4f7f6;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 10;
}

/* ========================================== */
/* Menu lateral     */
/* ========================================== */

/* La columna oscura de la izquierda */
.sidebar {
  width: 260px;
  background-color: #1a1a1a;
  color: white;
  display: flex;
  flex-direction: column;
  padding: 2rem 0;
  flex-shrink: 0;
}

.logo-admin {
  padding: 0 2rem;
  margin-bottom: 3rem;
  color: #e50914;
}

/* Opciones del menu */
.menu-lateral {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.menu-lateral button {
  background: none;
  border: none;
  color: #a0a0a0;
  padding: 1.2rem 2rem;
  text-align: left;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  border-left: 4px solid transparent;
}

/* Cuando el raton pasa por encima de un boton del menu */
.menu-lateral button:hover {
  background-color: #333;
  color: white;
}

/* El boton del menu que esta seleccionado actualmente */
.menu-lateral button.activo {
  background-color: #333;
  color: white;
  border-left: 4px solid #e50914;
  font-weight: bold;
}

/* Parte inferior del menu lateral */
.sidebar-footer {
  padding: 0 2rem;
}

/* Enlace para regresar a la pagina principal */
.btn-volver {
  color: #a0a0a0;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.btn-volver:hover {
  color: white;
}

/* ========================================== */
/* AREA CENTRAL DE TRABAJO                 */
/* ========================================== */

/* La parte derecha donde sale todo el contenido */
.contenido-principal {
  flex-grow: 1;
  padding: 3rem;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* El titulo y el boton principal de cada seccion */
.cabecera-contenido {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-shrink: 0;
}

.titulo-seccion {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  color: #333;
}

.subtitulo {
  margin: 0;
  color: #777;
}

/* ========================================== */
/* DISEÑO DE LAS TABLAS DE DATOS           */
/* ========================================== */

/* La caja blanca que envuelve a la tabla */
.contenedor-tabla {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  overflow-x: auto;
  flex-grow: 1;
}

.tabla-admin {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  white-space: nowrap;
}

/* Filas y columnas de la tabla */
.tabla-admin th,
.tabla-admin td {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  font-size: 0.9rem;
}

/* La cabecera de la tabla que se queda fija al bajar */
.tabla-admin th {
  background-color: #fafafa;
  color: #555;
  text-align: left;
  position: sticky;
  top: 0;
  z-index: 1;
}

/* Truco para cortar textos muy largos y ponerles puntos suspensivos */
.truncar-texto {
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Muestra el texto completo al poner el raton encima */
.truncar-texto:hover {
  white-space: normal;
  word-break: break-all;
  background: #fff;
  position: relative;
  z-index: 2;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  padding: 0.5rem;
}

/* Textos de ayuda y adornos en la tabla */
.font-bold {
  font-weight: bold;
  color: #222;
}

.texto-centro {
  text-align: center;
}

/* Etiquetas pequeñas grises (ej. para el idioma) */
.badge {
  background: #e2e8f0;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
  color: #475569;
}

/* ========================================== */
/* BOTONES GLOBALES Y DE LA TABLA          */
/* ========================================== */

/* Boton principal oscuro (ej. "Agregar Pelicula") */
.btn-primario {
  background-color: #4a4a4a;
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.btn-primario:hover {
  background-color: #333;
}

/* Contenedor para los botones de editar y borrar */
.celda-acciones {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.btn-editar,
.btn-eliminar {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.btn-editar {
  background-color: #e0e0e0;
  color: #333;
}

.btn-editar:hover {
  background-color: #ccc;
}

.btn-eliminar {
  background-color: #ffe6e6;
  color: #cc0000;
}

.btn-eliminar:hover {
  background-color: #ffcccc;
}

/* ========================================== */
/* VENTANAS EMERGENTES (MODALES)           */
/* ========================================== */

/* El fondo oscuro transparente que cubre todo al abrir un formulario */
.overlay-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

/* La caja blanca del formulario */
.caja-modal {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
}

/* Caja mas pequeña para preguntar si estas seguro de borrar algo */
.modal-pequeno {
  max-width: 400px;
}

/* Permite hacer scroll si el formulario es muy largo */
.scrollable {
  overflow-y: auto;
}

/* ========================================== */
/* FORMULARIOS DENTRO DE LOS MODALES       */
/* ========================================== */
.formulario-modal {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Para poner dos cajas de texto en la misma linea */
.fila-input {
  display: flex;
  gap: 1rem;
}

.flex-1 {
  flex: 1;
}

/* Agrupa el titulo y su caja de texto */
.grupo-input {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.grupo-input label {
  font-weight: bold;
  font-size: 0.85rem;
}

.grupo-input input,
.grupo-input select,
.grupo-input textarea {
  padding: 0.7rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: inherit;
  font-size: 0.9rem;
}

/* Botones al final del formulario */
.acciones-modal {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.btn-cancelar {
  background: none;
  border: 1px solid #ccc;
  padding: 0.6rem 1.2rem;
  cursor: pointer;
  border-radius: 4px;
}

.btn-guardar {
  background: #4a4a4a;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  cursor: pointer;
  border-radius: 4px;
}

/* Boton rojo fuerte para confirmar que quieres borrar algo */
.btn-eliminar-confirmar {
  background: #cc0000;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  cursor: pointer;
  border-radius: 4px;
  font-weight: bold;
}

.btn-eliminar-confirmar:hover {
  background: #990000;
}

/* ========================================== */
/* CONTROLES DE PAGINAS (PAGINACION)       */
/* ========================================== */
/* La zona de los botones de Siguiente y Anterior */
.paginacion-admin {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 1.5rem;
  padding: 1rem 0;
}

.btn-paginacion {
  padding: 0.5rem 1rem;
  background-color: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  color: #374151;
  transition: all 0.2s;
}

/* Color al pasar el raton (solo si el boton se puede usar) */
.btn-paginacion:hover:not(:disabled) {
  background-color: #e5e7eb;
}

/* Apariencia del boton cuando no hay mas paginas a donde ir */
.btn-paginacion:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Texto que dice "Pagina 1 de 3" */
.info-paginacion {
  color: #4b5563;
  font-size: 0.95rem;
}
</style>
