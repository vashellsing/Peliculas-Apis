import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useAuthStore = defineStore("auth", () => {
  // Al iniciar la app, revisamos si ya había un token guardado
  // (por ejemplo, si el usuario recargó la página)
  const token = ref(localStorage.getItem("token_cine") || null);

  const setToken = (nuevoToken) => {
    token.value = nuevoToken;
    localStorage.setItem("token_cine", nuevoToken);
  };

  const limpiarToken = () => {
    token.value = null;
    localStorage.removeItem("token_cine");
  };

  // Decodificamos el JWT para leer el payload (la parte del medio)
  // Un JWT tiene forma: xxxxx.PAYLOAD.zzzzz
  // El payload está en Base64, por eso usamos atob() para descifrarlo
  const datosUsuario = computed(() => {
    if (!token.value) return null;
    try {
      return JSON.parse(atob(token.value.split(".")[1]));
    } catch {
      // Si el token está corrupto, lo tratamos como si no existiera
      return null;
    }
  });

  const estaAutenticado = computed(() => token.value !== null);
  
  // Ajusta "rol" al nombre exacto que tu backend de Python pone en el JWT
  const esAdmin = computed(() => datosUsuario.value?.rol === "admin");

  return { token, setToken, limpiarToken, estaAutenticado, esAdmin };
});