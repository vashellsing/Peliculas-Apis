<script setup>

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
  <!-- Facebook -->
  <a href="https://www.facebook.com/login" target="_blank" rel="noopener" class="icono-red icono-facebook">
    <svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
      <path d="M24 12.073C24 5.405 18.627 0 12 0S0 5.405 0 12.073C0 18.1 4.388 23.094 10.125 24v-8.437H7.078v-3.49h3.047V9.41c0-3.025 1.792-4.697 4.533-4.697 1.312 0 2.686.236 2.686.236v2.97h-1.513c-1.491 0-1.956.93-1.956 1.886v2.268h3.328l-.532 3.49h-2.796V24C19.612 23.094 24 18.1 24 12.073z"/>
    </svg>
  </a>

  <!-- Instagram -->
  <a href="https://www.instagram.com/accounts/login" target="_blank" rel="noopener" class="icono-red icono-instagram">
    <svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
      <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/>
    </svg>
  </a>

  <!-- X (Twitter) -->
  <a href="https://x.com/i/flow/login" target="_blank" rel="noopener" class="icono-red icono-x">
    <svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
      <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.746l7.73-8.835L1.254 2.25H8.08l4.253 5.622 5.911-5.622zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
    </svg>
  </a>
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
  background-color: #1a1a1a;
  color: #cccccc;
  padding: 3rem 2rem 1rem 2rem;
  font-family: sans-serif;
  margin-top: 4rem; 
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
  flex-wrap: wrap; 
  justify-content: center;
}

.enlaces-footer a {
  color: #cccccc;
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.2s;
}

.enlaces-footer a:hover {
  color: #ffffff; 
}

/* Redes sociales */
.redes-sociales {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.icono-red {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  transition: transform 0.2s, background-color 0.2s;
  color: white;
}

.icono-red:hover {
  transform: scale(1.1);
}

/* Color oficial de cada red */
.icono-facebook { background-color: #1877F2; }
.icono-facebook:hover { background-color: #0d6edc; }

.icono-instagram { background: radial-gradient(circle at 30% 107%, #fdf497 0%, #fd5949 45%, #d6249f 60%, #285AEB 90%); }
.icono-instagram:hover { opacity: 0.85; }

.icono-x { background-color: #000000; }
.icono-x:hover { background-color: #333; }

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