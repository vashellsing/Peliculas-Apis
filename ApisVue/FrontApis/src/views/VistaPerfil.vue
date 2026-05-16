<script setup>
import { ref } from "vue";

const usuario = ref({
  nombre: "Cinéfilo Experto",
  correo: "usuario@correo.com",
  miembroDesde: "2023",
  avatarUrl: "https://api.dicebear.com/7.x/avataaars/svg?seed=Felix",
});

// Estados para la carga de analítica
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
      <header class="cabecera-usuario">
        <img :src="usuario.avatarUrl" alt="Avatar" class="avatar" />
        <div class="info-usuario">
          <h1 class="nombre-usuario">{{ usuario.nombre }}</h1>
          <p class="correo">{{ usuario.correo }}</p>
          <p class="fecha-miembro">Miembro desde {{ usuario.miembroDesde }}</p>
        </div>

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

        <RouterLink to="/favoritos" class="btn-ir-favoritos"
          >Ver mis películas favoritas ➡</RouterLink
        >
      </div>
    </div>
  </div>
</template>

<style scoped>
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
  align-items: center;
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
}
.info-usuario {
  flex: 1;
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
