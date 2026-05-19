<script setup>
import { ref } from "vue";

// --- DATOS DEL USUARIO ---
const usuario = ref({
  nombre: "Cinéfilo Experto",
  correo: "usuario@correo.com",
  miembroDesde: "2023",
  avatarUrl: "https://api.dicebear.com/7.x/avataaars/svg?seed=Felix",
});

// --- LÓGICA DE EDICIÓN DE PERFIL ---
const editando = ref(false);
const formulario = ref({});

const activarEdicion = () => {
  // Clonamos los datos actuales al formulario para no afectar la vista antes de guardar
  formulario.value = { ...usuario.value };
  editando.value = true;
};

const cancelarEdicion = () => {
  editando.value = false;
};

const guardarCambios = () => {
  // Pasamos los datos del formulario de vuelta al usuario y cerramos el modo edición
  usuario.value = { ...formulario.value };
  editando.value = false;
  console.log("Datos actualizados (Simulación):", usuario.value);
};

// --- LÓGICA DE ANALÍTICA ---
const cargandoAnalitica = ref(false);
const mostrarGrafica = ref(false);

const solicitarAnalitica = () => {
  cargandoAnalitica.value = true;
  mostrarGrafica.value = false;

  setTimeout(() => {
    cargandoAnalitica.value = false;
    mostrarGrafica.value = true;
  }, 1500);
};
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

          <!-- VISTA DE EDICIÓN -->
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
              <button type="submit" class="btn-guardar">Guardar Cambios</button>
            </div>
          </form>
        </div>

        <!-- CAJA DE ANALÍTICA (Se mantiene igual) -->
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

      <!-- RESULTADO GRÁFICA -->
      <div v-if="mostrarGrafica" class="resultado-grafica">
        <h2>Tu Perfil de Espectador</h2>
        <img
          src="https://quickchart.io/chart?c={type:'pie',data:{labels:['Ciencia Ficción','Acción','Drama'],datasets:[{data:[60,25,15]}]}}"
          alt="Gráfico de géneros"
          class="grafica-pastel"
        />
        <p class="resumen-analitica">
          ¡Definitivamente eres un amante de la
          <strong>Ciencia Ficción</strong>!
        </p>

        <RouterLink to="/favoritos" class="btn-ir-favoritos">
          Ver mis películas favoritas ➡
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ESTILOS ORIGINALES */
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

/* NUEVOS ESTILOS PARA EDICIÓN */
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

/* RESTO DE ESTILOS ORIGINALES */
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
