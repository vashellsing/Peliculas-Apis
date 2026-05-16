<script setup>
import { ref, computed } from "vue";

const menuActivo = ref("peliculas");

// --- SIMULACIÓN DE BASE DE DATOS (Alineado al 100% con tu SQL) ---

const datosPeliculas = ref([
  {
    id_pelicula: 1,
    titulo: "Spider-Man: No Way Home",
    titulo_originalPelicula: "Spider-Man: No Way Home",
    sinopsis:
      "Spider-Man es desenmascarado y ya no puede separar su vida normal de la de superhéroe.",
    anio: 2021,
    actoresPelicula: "Tom Holland, Zendaya, Benedict Cumberbatch",
    generoPelicula: "Accion",
    idiomaPelicula: "Ingles",
    poster: "https://ejemplo.com/poster.jpg",
    lema: "El multiverso se desata",
    trailer: "https://youtube.com/trailer",
  },
]);

const datosSeries = ref([
  {
    id_serie: 1,
    tituloSerie: "Breaking Bad",
    titulo_originalSerie: "Breaking Bad",
    sinopsisSerie:
      "Un profesor de química con cáncer terminal se asocia con un exalumno para fabricar y vender metanfetamina.",
    anio_lanzamientoSerie: 2008,
    temporadasSerie: 5,
    actoresSerie: "Bryan Cranston, Aaron Paul",
    generoSerie: "Drama",
    idiomaSerie: "Ingles",
  },
]);

const datosCines = ref([
  {
    id_cine: 1,
    nombreCine: "Cine Colombia",
    direccionCine: "C.C. Campanario",
    ciudadCine: "Popayán",
  },
]);

const datosCarteleras = ref([
  {
    id_cartelera: 1,
    id_peliculaCartelera: 1,
    id_cineCartelera: 1,
    fecha_horaCartelera: "2024-05-20T18:30",
    idioma_proyeccionCartelera: "Doblada al Espanol",
  },
]);

const listaActual = computed(() => {
  if (menuActivo.value === "peliculas") return datosPeliculas.value;
  if (menuActivo.value === "series") return datosSeries.value;
  if (menuActivo.value === "cines") return datosCines.value;
  if (menuActivo.value === "cartelera") return datosCarteleras.value;
  return [];
});

// --- LÓGICA DEL MODAL ---
const modalVisible = ref(false);
const esEdicion = ref(false);
const formulario = ref({});

const abrirModalAgregar = () => {
  esEdicion.value = false;
  if (menuActivo.value === "peliculas") {
    formulario.value = {
      id_pelicula: null,
      titulo: "",
      titulo_originalPelicula: "",
      sinopsis: "",
      anio: new Date().getFullYear(),
      actoresPelicula: "",
      generoPelicula: "Otro",
      idiomaPelicula: "Otro",
      poster: "",
      lema: "",
      trailer: "",
    };
  } else if (menuActivo.value === "series") {
    formulario.value = {
      id_serie: null,
      tituloSerie: "",
      titulo_originalSerie: "",
      sinopsisSerie: "",
      anio_lanzamientoSerie: new Date().getFullYear(),
      temporadasSerie: 1,
      actoresSerie: "",
      generoSerie: "Otro",
      idiomaSerie: "Otro",
    };
  } else if (menuActivo.value === "cines") {
    formulario.value = {
      id_cine: null,
      nombreCine: "",
      direccionCine: "",
      ciudadCine: "",
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

const abrirModalEditar = (item) => {
  esEdicion.value = true;
  formulario.value = { ...item };
  modalVisible.value = true;
};

const cerrarModal = () => (modalVisible.value = false);

const guardarCambios = () => {
  console.log("Datos para SQL:", formulario.value);
  cerrarModal();
};

const eliminarItem = (id) => {
  if (confirm("¿Confirmas que deseas eliminar este registro?")) {
    console.log(`DELETE FROM ${menuActivo.value} WHERE id = ${id}`);
  }
};
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
          <p class="subtitulo">Aqui se hacen cositas de admin</p>
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
              <th class="texto-centro">Acciones</th>
            </tr>

            <tr v-else-if="menuActivo === 'cartelera'">
              <th>ID</th>
              <th>Peli ID</th>
              <th>Cine ID</th>
              <th>Fecha/Hora</th>
              <th>Idioma</th>
              <th class="texto-centro">Acciones</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="item in listaActual"
              :key="
                item.id_pelicula ||
                item.id_serie ||
                item.id_cine ||
                item.id_cartelera
              "
            >
              <template v-if="menuActivo === 'peliculas'">
                <td>#{{ item.id_pelicula }}</td>
                <td class="font-bold truncar-texto">{{ item.titulo }}</td>
                <td class="truncar-texto">
                  {{ item.titulo_originalPelicula }}
                </td>
                <td class="truncar-texto" :title="item.sinopsis">
                  {{ item.sinopsis }}
                </td>
                <td>{{ item.anio }}</td>
                <td class="truncar-texto" :title="item.actoresPelicula">
                  {{ item.actoresPelicula }}
                </td>
                <td>
                  <span class="badge">{{ item.generoPelicula }}</span>
                </td>
                <td>{{ item.idiomaPelicula }}</td>
                <td class="truncar-texto">
                  <a :href="item.poster" target="_blank">Link</a>
                </td>
                <td class="truncar-texto">{{ item.lema }}</td>
                <td class="truncar-texto">
                  <a :href="item.trailer" target="_blank">Ver</a>
                </td>
              </template>

              <template v-else-if="menuActivo === 'series'">
                <td>#{{ item.id_serie }}</td>
                <td class="font-bold truncar-texto">{{ item.tituloSerie }}</td>
                <td class="truncar-texto">{{ item.titulo_originalSerie }}</td>
                <td class="truncar-texto" :title="item.sinopsisSerie">
                  {{ item.sinopsisSerie }}
                </td>
                <td>{{ item.anio_lanzamientoSerie }}</td>
                <td>{{ item.temporadasSerie }}</td>
                <td class="truncar-texto" :title="item.actoresSerie">
                  {{ item.actoresSerie }}
                </td>
                <td>
                  <span class="badge">{{ item.generoSerie }}</span>
                </td>
                <td>{{ item.idiomaSerie }}</td>
              </template>

              <template v-else-if="menuActivo === 'cines'">
                <td>#{{ item.id_cine }}</td>
                <td class="font-bold">{{ item.nombreCine }}</td>
                <td>{{ item.direccionCine }}</td>
                <td>{{ item.ciudadCine }}</td>
              </template>

              <template v-else-if="menuActivo === 'cartelera'">
                <td>#{{ item.id_cartelera }}</td>
                <td>{{ item.id_peliculaCartelera }}</td>
                <td>{{ item.id_cineCartelera }}</td>
                <td>{{ item.fecha_horaCartelera }}</td>
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
                    eliminarItem(
                      item.id_pelicula ||
                        item.id_serie ||
                        item.id_cine ||
                        item.id_cartelera,
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
              <input type="text" v-model="formulario.titulo_originalPelicula" />
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
                <select v-model="formulario.generoPelicula">
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
              <select v-model="formulario.idiomaPelicula">
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
              <label>Actores (Separados por coma)</label>
              <textarea
                v-model="formulario.actoresPelicula"
                rows="2"
              ></textarea>
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
              <input type="text" v-model="formulario.tituloSerie" required />
            </div>
            <div class="grupo-input">
              <label>Título Original</label>
              <input type="text" v-model="formulario.titulo_originalSerie" />
            </div>
            <div class="grupo-input">
              <label>Sinopsis</label>
              <textarea v-model="formulario.sinopsisSerie" rows="3"></textarea>
            </div>
            <div class="fila-input">
              <div class="grupo-input flex-1">
                <label>Año de Lanzamiento</label>
                <input
                  type="number"
                  v-model="formulario.anio_lanzamientoSerie"
                />
              </div>
              <div class="grupo-input flex-1">
                <label>Temporadas</label>
                <input
                  type="number"
                  v-model="formulario.temporadasSerie"
                  min="1"
                  required
                />
              </div>
            </div>
            <div class="fila-input">
              <div class="grupo-input flex-1">
                <label>Género</label>
                <select v-model="formulario.generoSerie">
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
                <select v-model="formulario.idiomaSerie">
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
              <label>Actores</label>
              <textarea v-model="formulario.actoresSerie" rows="2"></textarea>
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
          </template>

          <template v-else-if="menuActivo === 'cartelera'">
            <div class="grupo-input">
              <label>ID Película</label>
              <input
                type="number"
                v-model="formulario.id_peliculaCartelera"
                required
              />
            </div>
            <div class="grupo-input">
              <label>ID Cine</label>
              <input
                type="number"
                v-model="formulario.id_cineCartelera"
                required
              />
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
  </div>
</template>

<style scoped>
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
.menu-lateral button:hover {
  background-color: #333;
  color: white;
}
.menu-lateral button.activo {
  background-color: #333;
  color: white;
  border-left: 4px solid #e50914;
  font-weight: bold;
}
.sidebar-footer {
  padding: 0 2rem;
}
.btn-volver {
  color: #a0a0a0;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s;
}
.btn-volver:hover {
  color: white;
}
.contenido-principal {
  flex-grow: 1;
  padding: 3rem;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
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

/* NUEVO: Contenedor de tabla con scroll horizontal */
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
.tabla-admin th,
.tabla-admin td {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  font-size: 0.9rem;
}
.tabla-admin th {
  background-color: #fafafa;
  color: #555;
  text-align: left;
  position: sticky;
  top: 0;
  z-index: 1;
}

/* NUEVO: Truncar textos largos en la tabla */
.truncar-texto {
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
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

.font-bold {
  font-weight: bold;
  color: #222;
}
.texto-centro {
  text-align: center;
}
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
.badge {
  background: #e2e8f0;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
  color: #475569;
}

/* MODAL */
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
.caja-modal {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
}
.scrollable {
  overflow-y: auto;
}
.formulario-modal {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.fila-input {
  display: flex;
  gap: 1rem;
}
.flex-1 {
  flex: 1;
}
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
</style>
