<script setup>
// ==========================================
// 1. IMPORTACIONES
// ==========================================
import { ref, computed, onMounted } from "vue";
import axios from "axios";

// ==========================================
// 2. ESTADO GLOBAL DE LA VISTA
// ==========================================
const cargando = ref(false);
const mensajeVisual = ref({ texto: "", tipo: "" });

const usuario = ref({
  id: null,
  nombre: "Cargando...",
  correo: "Cargando...",
  miembroDesde: "2026",
  avatarUrl: "https://api.dicebear.com/7.x/avataaars/svg?seed=Felix",
});

// ==========================================
// 3. LÓGICA DE AUTENTICACIÓN Y SESIÓN
// ==========================================
const cargarDatosUsuarioDesdeToken = () => {
  const token = localStorage.getItem("token_cine");
  if (!token) return;

  try {
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split("")
        .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
        .join(""),
    );

    const datosToken = JSON.parse(jsonPayload);

    usuario.value.id = datosToken.id;
    usuario.value.nombre = datosToken.nombre || "Cineasta";
    usuario.value.correo = datosToken.correo || "sin_correo@cine.com";
    usuario.value.avatarUrl =
      datosToken.avatarUrl ||
      "https://api.dicebear.com/7.x/avataaars/svg?seed=Felix";
    usuario.value.miembroDesde = datosToken.miembroDesde || "Reciente";
  } catch (error) {
    console.error("Error al decodificar el token de sesión:", error);
  }
};

// ==========================================
// 4. LÓGICA DE EDICIÓN DE PERFIL (SOAP)
// ==========================================
const editando = ref(false);
const formulario = ref({});

const activarEdicion = () => {
  formulario.value = { ...usuario.value };
  editando.value = true;
};

const cancelarEdicion = () => {
  editando.value = false;
};

const guardarCambios = async () => {
  cargando.value = true;
  mensajeVisual.value = { texto: "", tipo: "" };

  const xmlSOAP = `<?xml version="1.0" encoding="utf-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="spyne.api.autenticacion.Prueba">
      <soapenv:Body>
        <tns:actualizar_perfil>
          <tns:id_usuario>${usuario.value.id}</tns:id_usuario>
          <tns:nombreUsuario>${formulario.value.nombre}</tns:nombreUsuario>
          <tns:correoUsuario>${formulario.value.correo}</tns:correoUsuario>
          <tns:avatarUrl>${formulario.value.avatarUrl}</tns:avatarUrl>
        </tns:actualizar_perfil>
      </soapenv:Body>
    </soapenv:Envelope>`;

  try {
    const respuesta = await axios.post("http://127.0.0.1:8000/", xmlSOAP, {
      headers: { "Content-Type": "text/xml" },
    });

    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(respuesta.data, "text/xml");
    const resultado = xmlDoc.documentElement.textContent.trim();

    if (resultado.includes("Error")) {
      mensajeVisual.value = { texto: resultado, tipo: "error" };
    } else {
      localStorage.setItem("token_cine", resultado);
      mensajeVisual.value = {
        texto: "¡Perfil actualizado con éxito en la base de datos!",
        tipo: "exito",
      };
      cargarDatosUsuarioDesdeToken();
      editando.value = false;
    }
  } catch (error) {
    console.error(
      "Error al actualizar:",
      error.response ? error.response.data : error,
    );
    mensajeVisual.value = {
      texto: "No se pudo guardar la información. Revisa la conexión.",
      tipo: "error",
    };
  } finally {
    cargando.value = false;
  }
};

// ==========================================
// 5. LÓGICA DE ANALÍTICAS (REST + PANDAS)
// ==========================================
const cargandoAnalitica = ref(false);
const mostrarGrafica = ref(false);

const datosGrafica = ref({
  etiquetas: [],
  valores: [],
  generoDominante: "",
});

const solicitarAnalitica = async () => {
  cargandoAnalitica.value = true;
  mostrarGrafica.value = false;

  try {
    const token = localStorage.getItem("token_cine");
    const config = {
      headers: {
        "x-api-key": "mi_super_api_key_fija_123",
        Authorization: `Bearer ${token}`,
      },
    };

    const urlAnalitica = "http://127.0.0.1:5000/favoritos/analitica";
    const respuesta = await axios.get(urlAnalitica, config);
    const dataRecibida = respuesta.data;

    datosGrafica.value.etiquetas = Object.keys(dataRecibida.conteo_generos);
    datosGrafica.value.valores = Object.values(dataRecibida.conteo_generos);
    datosGrafica.value.generoDominante = dataRecibida.genero_dominante;

    mostrarGrafica.value = true;
  } catch (error) {
    console.error("Error al recopilar favoritos para analítica:", error);
    if (error.response && error.response.status === 404) {
      alert(error.response.data.mensaje);
    } else {
      alert("Hubo un error obteniendo tu historial de favoritos.");
    }
  } finally {
    cargandoAnalitica.value = false;
  }
};

const urlGraficaDinamica = computed(() => {
  const chartConfig = {
    type: "pie",
    data: {
      labels: datosGrafica.value.etiquetas,
      datasets: [
        {
          data: datosGrafica.value.valores,
          backgroundColor: [
            "#e50914",
            "#4a4a4a",
            "#2e7d32",
            "#0288d1",
            "#f57c00",
            "#7b1fa2",
          ],
        },
      ],
    },
    options: {
      legend: { position: "bottom" },
    },
  };
  return `https://quickchart.io/chart?c=${encodeURIComponent(JSON.stringify(chartConfig))}`;
});

// ==========================================
// 6. CICLO DE VIDA (Lanzadores iniciales)
// ==========================================
onMounted(() => {
  cargarDatosUsuarioDesdeToken();
});
</script>

<template>
  <div class="vista-perfil">
    <div class="contenedor-perfil">
      <!-- CABECERA DE USUARIO -->
      <header class="cabecera-usuario">
        <img :src="usuario.avatarUrl" alt="Avatar" class="avatar" />

        <div class="info-usuario">
          <!-- VISTA DE LECTURA -->
          <template v-if="!editando">
            <h1 class="nombre-usuario">{{ usuario.nombre }}</h1>
            <p class="correo">{{ usuario.correo }}</p>
            <p class="fecha-miembro">
              Miembro desde {{ usuario.miembroDesde }}
            </p>

            <button @click="activarEdicion" class="btn-editar-perfil">
              ✏️ Editar Perfil
            </button>
          </template>

          <!-- VISTA DE EDICION -->
          <form
            v-else
            @submit.prevent="guardarCambios"
            class="formulario-edicion"
          >
            <div class="grupo-input">
              <label>Nombre</label>
              <input type="text" v-model="formulario.nombre" required />
            </div>
            <div class="grupo-input">
              <label>Correo</label>
              <input type="email" v-model="formulario.correo" required />
            </div>
            <div class="grupo-input">
              <label>URL del Avatar (Opcional)</label>
              <input type="text" v-model="formulario.avatarUrl" />
            </div>

            <div class="acciones-edicion">
              <button
                type="button"
                @click="cancelarEdicion"
                class="btn-cancelar"
              >
                Cancelar
              </button>
              <button type="submit" :disabled="cargando" class="btn-guardar">
                {{ cargando ? "Guardando..." : "Guardar Cambios" }}
              </button>

              <div
                v-if="mensajeVisual.texto"
                :class="['alerta', mensajeVisual.tipo]"
              >
                {{ mensajeVisual.texto }}
              </div>
            </div>
          </form>
        </div>

        <!-- CAJA DE LA ANALITICA -->
        <div class="caja-analitica">
          <h3>ADN Cinéfilo</h3>
          <p>Descubre qué géneros dominan tus favoritos.</p>

          <button
            v-if="!mostrarGrafica && !cargandoAnalitica"
            @click="solicitarAnalitica"
            class="btn-analizar"
          >
            📊 Generar Analítica
          </button>

          <div v-if="cargandoAnalitica" class="cargando">
            Analizando tus favoritos... ⏳
          </div>
        </div>
      </header>

      <!-- RESULTADO GRAFICA -->
      <div v-if="mostrarGrafica" class="resultado-grafica">
        <h2>Tu Perfil de Espectador</h2>

        <img
          :src="urlGraficaDinamica"
          alt="Gráfico de géneros reales"
          class="grafica-pastel"
        />

        <p class="resumen-analitica">
          ¡Definitivamente eres un amante del género
          <strong>{{ datosGrafica.generoDominante }}</strong
          >!
        </p>

        <RouterLink to="/favoritos" class="btn-ir-favoritos">
          Ver mis películas favoritas ➡
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ==========================================
   1. ESTRUCTURA PRINCIPAL
   ========================================== */
.vista-perfil {
  padding: 3rem 2rem;
  font-family: sans-serif;
  background-color: #fafafa;
  min-height: 70vh;
}
.contenedor-perfil {
  max-width: 1000px;
  margin: 0 auto;
}

/* ==========================================
   2. CABECERA Y DATOS DEL USUARIO
   ========================================== */
.cabecera-usuario {
  display: flex;
  align-items: flex-start;
  background-color: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
  gap: 2rem;
  flex-wrap: wrap;
}
.avatar {
  width: 120px;
  height: 120px;
  background-color: #f0f0f0;
  border-radius: 50%;
  border: 4px solid #fff;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  object-fit: cover;
}
.info-usuario {
  flex: 1;
  min-width: 250px;
}
.nombre-usuario {
  margin: 0 0 0.3rem 0;
  font-size: 2rem;
  color: #1a1a1a;
}
.correo {
  margin: 0;
  color: #666;
  font-size: 1.1rem;
}
.fecha-miembro {
  margin: 0.5rem 0 0 0;
  font-size: 0.9rem;
  color: #999;
}

/* ==========================================
   3. MODO EDICIÓN (FORMULARIO Y BOTONES)
   ========================================== */
.btn-editar-perfil {
  margin-top: 1rem;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  color: #333;
  transition: all 0.2s;
}
.btn-editar-perfil:hover {
  background-color: #e2e2e2;
}
.formulario-edicion {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  background: #f9f9f9;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #eaeaea;
}
.grupo-input {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}
.grupo-input label {
  font-size: 0.85rem;
  font-weight: bold;
  color: #555;
}
.grupo-input input {
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-family: inherit;
  font-size: 1rem;
}
.acciones-edicion {
  display: flex;
  gap: 0.8rem;
  margin-top: 0.5rem;
}
.btn-cancelar {
  background: none;
  border: 1px solid #ccc;
  padding: 0.5rem 1rem;
  cursor: pointer;
  border-radius: 4px;
  color: #555;
}
.btn-cancelar:hover {
  background: #eee;
}
.btn-guardar {
  background: #4a4a4a;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
  border-radius: 4px;
  font-weight: bold;
}
.btn-guardar:hover {
  background: #333;
}

/* ==========================================
   4. CAJA DE LLAMADO A LA ANALÍTICA
   ========================================== */
.caja-analitica {
  background-color: #1a1a1a;
  color: white;
  padding: 1.5rem 2rem;
  border-radius: 8px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 250px;
}
.caja-analitica h3 {
  margin: 0 0 0.5rem 0;
  color: #e50914;
  font-size: 1.2rem;
}
.caja-analitica p {
  margin: 0 0 1rem 0;
  font-size: 0.9rem;
  color: #ccc;
}
.btn-analizar {
  background-color: #e50914;
  color: white;
  border: none;
  padding: 0.6rem 1rem;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s;
}
.btn-analizar:hover {
  transform: scale(1.05);
  background-color: #b8070f;
}
.cargando {
  font-style: italic;
  color: #aaa;
  font-size: 0.9rem;
}

/* ==========================================
   5. RESULTADOS Y GRÁFICA
   ========================================== */
.resultado-grafica {
  background-color: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  margin-bottom: 3rem;
  text-align: center;
  border-top: 4px solid #e50914;
  animation: aparecer 0.5s ease-out;
}
.resultado-grafica h2 {
  margin-top: 0;
  color: #333;
}
.grafica-pastel {
  max-width: 400px;
  width: 100%;
  height: auto;
  margin: 1rem auto;
  display: block;
}
.resumen-analitica {
  font-size: 1.2rem;
  color: #555;
  margin-bottom: 1.5rem;
}
.resumen-analitica strong {
  color: #e50914;
}
.btn-ir-favoritos {
  display: inline-block;
  padding: 0.6rem 1.2rem;
  background-color: #4a4a4a;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: bold;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}
.btn-ir-favoritos:hover {
  background-color: #333;
}

/* ==========================================
   6. ANIMACIONES
   ========================================== */
@keyframes aparecer {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
