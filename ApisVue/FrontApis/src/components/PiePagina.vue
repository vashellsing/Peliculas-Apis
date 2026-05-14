<script setup>
// Por ahora no necesitamos lógica aquí, solo estructura visual
const anioActual = new Date().getFullYear();
</script>

<template>
  <footer class="pie-pagina">
    <div class="contenedor-footer">
      
      <div class="enlaces-footer">
        <a href="#">Sobre nosotros</a>
        <a href="#">Términos de servicio</a>
        <a href="#">Política de privacidad</a>
        <a href="#">Contacto</a>
      </div>

      <div class="redes-sociales">
        <a href="#" class="icono-red">FB</a>
        <a href="#" class="icono-red">IG</a>
        <a href="#" class="icono-red">X</a>
      </div>

    </div>

    <div class="derechos-autor">
      <p>&copy; {{ anioActual }} CarteleraVue. Todos los derechos reservados.</p>
    </div>
  </footer>
</template>

<style scoped>
/* Estilos del pie de página */
.pie-pagina {
  background-color: #1a1a1a; /* Gris muy oscuro, casi negro */
  color: #cccccc; /* Texto en gris claro para contraste */
  padding: 3rem 2rem 1rem 2rem;
  font-family: sans-serif;
  margin-top: 4rem; /* Lo separa un poco del contenido principal */
}

.contenedor-footer {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

/* Enlaces */
.enlaces-footer {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap; /* Si la pantalla es pequeña, se acomodan abajo */
  justify-content: center;
}

.enlaces-footer a {
  color: #cccccc;
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.2s;
}

.enlaces-footer a:hover {
  color: #ffffff; /* Brilla un poco al pasar el cursor */
}

/* Redes sociales */
.redes-sociales {
  display: flex;
  gap: 1.5rem;
}

.icono-red {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background-color: #333333;
  color: #ffffff;
  text-decoration: none;
  border-radius: 50%; /* Círculos perfectos */
  font-weight: bold;
  transition: background-color 0.2s, transform 0.2s;
}

.icono-red:hover {
  background-color: #555555;
  transform: scale(1.1); /* Efecto de acercamiento */
}

/* Derechos de autor */
.derechos-autor {
  text-align: center;
  margin-top: 3rem;
  padding-top: 1rem;
  border-top: 1px solid #333333;
  font-size: 0.85rem;
  color: #888888;
}
</style>