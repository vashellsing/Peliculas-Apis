<script setup>
// ==========================================
// HERRAMIENTAS NECESARIAS
// ==========================================
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

// Esto nos sirve para mandar al usuario a otra pagina de la web
const router = useRouter();

// ==========================================
// CAJAS PARA EL ESTADO DE LA PANTALLA
// ==========================================
// Nos dice si mostramos la pantalla de registrarse o la de entrar
const esRegistro = ref(false);

// Nos avisa si el servidor esta procesando la informacion
const cargando = ref(false);

// Para guardar el mensaje de exito o de error que vera el usuario
const mensajeVisual = ref({ texto: "", tipo: "" });

// ==========================================
// CAJAS PARA GUARDAR LO QUE ESCRIBE EL USUARIO
// ==========================================
const formulario = ref({
  nombreUsuario: "",
  correo: "",
  contrasena: "",
});

// ==========================================
// FUNCION PARA CAMBIAR ENTRE ENTRAR Y REGISTRARSE
// ==========================================
const alternarModo = () => {
  esRegistro.value = !esRegistro.value;

  // Limpiamos los textos escritos y los mensajes viejos
  formulario.value = { nombreUsuario: "", correo: "", contrasena: "" };
  mensajeVisual.value = { texto: "", tipo: "" };
};

// ==========================================
// FUNCION PRINCIPAL PARA ENVIAR EL FORMULARIO
// ==========================================
const enviarFormulario = async () => {
  // Empezamos a pensar y borramos cualquier aviso anterior
  cargando.value = true;
  mensajeVisual.value = { texto: "", tipo: "" };

  // Aqui guardaremos el mensaje especial con etiquetas que entiende el servidor
  let xmlSOAP = "";

  // Preparamos el mensaje dependiendo de lo que quiera hacer el usuario
  if (esRegistro.value) {
    xmlSOAP = `<?xml version="1.0" encoding="utf-8"?>
      <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="spyne.api.autenticacion.Prueba">
        <soapenv:Body>
          <tns:registrar_usuario>
            <tns:nombreUsuario>${formulario.value.nombreUsuario}</tns:nombreUsuario>
            <tns:correoUsuario>${formulario.value.correo}</tns:correoUsuario>
            <tns:contrasenaUsuario>${formulario.value.contrasena}</tns:contrasenaUsuario>
          </tns:registrar_usuario>
        </soapenv:Body>
      </soapenv:Envelope>`;
  } else {
    xmlSOAP = `<?xml version="1.0" encoding="utf-8"?>
      <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="spyne.api.autenticacion.Prueba">
        <soapenv:Body>
          <tns:iniciar_sesion>
            <tns:correoUsuario>${formulario.value.correo}</tns:correoUsuario>
            <tns:contrasenaUsuario>${formulario.value.contrasena}</tns:contrasenaUsuario>
          </tns:iniciar_sesion>
        </soapenv:Body>
      </soapenv:Envelope>`;
  }

  try {
    // Enviamos el paquete de datos al servidor especial de contrasenas
    const respuesta = await axios.post("http://127.0.0.1:8000/", xmlSOAP, {
      headers: { "Content-Type": "text/xml" },
    });

    // Herramienta para desarmar el paquete con etiquetas que nos devolvio el servidor
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(respuesta.data, "text/xml");

    // Limpiamos las etiquetas y nos quedamos solo con el texto util (el pase o el error)
    const resultado = xmlDoc.documentElement.textContent.trim();

    // Revisamos que nos respondio el servidor para tomar una decision
    if (resultado.includes("Error")) {
      // Si la respuesta dice que hay un problema, lo mostramos en pantalla
      mensajeVisual.value = { texto: resultado, tipo: "error" };
    } else {
      if (esRegistro.value) {
        // Si se estaba registrando y todo salio bien, lo pasamos a la pantalla de entrar
        mensajeVisual.value = {
          texto: "¡Registro exitoso! Por favor, inicia sesion.",
          tipo: "exito",
        };
        esRegistro.value = false;
        formulario.value.contrasena = "";
      } else {
        // Si estaba entrando, guardamos su pase secreto en la memoria del navegador
        localStorage.setItem("token_cine", resultado);

        // Lo mandamos directo a la pagina de inicio de la web
        router.push("/");
      }
    }
  } catch (error) {
    console.error("Error SOAP:", error.response ? error.response.data : error);
    mensajeVisual.value = {
      texto: "No se pudo conectar con el servidor de autenticacion.",
      tipo: "error",
    };
  } finally {
    // Avisamos que ya terminamos todo el proceso
    cargando.value = false;
  }
};
</script>

<template>
  <div class="vista-autenticacion">
    <div class="contenedor-formulario">
      <h2 class="titulo">
        {{ esRegistro ? "Crear una cuenta" : "Bienvenido de nuevo" }}
      </h2>

      <!-- Alerta visual para errores o casos exitosos -->
      <div v-if="mensajeVisual.texto" :class="['alerta', mensajeVisual.tipo]">
        {{ mensajeVisual.texto }}
      </div>

      <form @submit.prevent="enviarFormulario" class="formulario">
        <div class="grupo-input" v-if="esRegistro">
          <input
            type="text"
            v-model="formulario.nombreUsuario"
            placeholder="Nombre de usuario"
            required
          />
        </div>

        <div class="grupo-input">
          <input
            type="email"
            v-model="formulario.correo"
            placeholder="Correo electrónico"
            required
          />
        </div>

        <div class="grupo-input">
          <input
            type="password"
            v-model="formulario.contrasena"
            placeholder="Contraseña"
            required
          />
        </div>

        <button type="submit" class="btn-submit" :disabled="cargando">
          {{
            cargando
              ? "Procesando..."
              : esRegistro
                ? "Registrarse"
                : "Iniciar Sesión"
          }}
        </button>
      </form>

      <div class="pie-formulario">
        <p>
          {{ esRegistro ? "¿Ya tienes una cuenta?" : "¿No tienes cuenta?" }}
          <button type="button" @click="alternarModo" class="btn-texto">
            {{ esRegistro ? "Inicia sesión aquí" : "Regístrate" }}
          </button>
        </p>
        <p class="terminos" v-if="esRegistro">
          Al registrarte, aceptas nuestros Términos de Servicio y Política de
          Privacidad.
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.vista-autenticacion {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  font-family: sans-serif;
  padding: 2rem;
}
.contenedor-formulario {
  width: 100%;
  max-width: 400px;
  background-color: #fff;
  padding: 2.5rem;
  border-radius: 8px;
  border: 1px solid #eaeaea;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  text-align: center;
}
.titulo {
  margin-bottom: 2rem;
  color: #333;
  font-size: 1.8rem;
}
.formulario {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}
.grupo-input input {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}
.grupo-input input:focus {
  outline: none;
  border-color: #4a4a4a;
}
.btn-submit {
  width: 100%;
  padding: 0.9rem;
  background-color: #4a4a4a;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: background-color 0.2s;
}
.btn-submit:hover {
  background-color: #333;
}
.btn-submit:disabled {
  background-color: #999;
  cursor: not-allowed;
}
.pie-formulario {
  margin-top: 2rem;
  font-size: 0.9rem;
  color: #666;
}
.btn-texto {
  background: none;
  border: none;
  color: #e50914;
  font-weight: bold;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 0;
  margin-left: 0.3rem;
}
.btn-texto:hover {
  text-decoration: underline;
}
.terminos {
  margin-top: 1.5rem;
  font-size: 0.75rem;
  color: #999;
}

/*Clases para las alertas */
.alerta {
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
  font-weight: bold;
  font-size: 0.9rem;
}
.alerta.error {
  background-color: #ffebee;
  color: #c62828;
  border: 1px solid #ef9a9a;
}
.alerta.exito {
  background-color: #e8f5e9;
  color: #2e7d32;
  border: 1px solid #a5d6a7;
}
</style>
