<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Nav from './components/Nav.vue'
import PiePagina from './components/PiePagina.vue';
import BarraBusqueda from './components/BarraBusqueda.vue';


</script>

<template>
 <Nav 
 
 />
<BarraBusqueda />

 <main>
  <RouterView />
 </main>

 <PiePagina />
</template>

<style scoped>



</style>
