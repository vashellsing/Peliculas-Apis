import { createRouter, createWebHistory } from 'vue-router'
import VistaInicio from '../views/VistaInicio.vue'
import VistaDetalle from '../views/VistaDetalle.vue'
import VistaAutenticacion from '../views/VistaAutenticacion.vue'
import VistaSeries from '@/views/VistaSeries.vue'
import VistaAdmin from '@/views/VistaAdmin.vue'
import vistaFavoritos from '@/views/VistaFavoritos.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'inicio',
      component: VistaInicio,
    },
    {
      // Usamos :id para que en un futuro la URL sea dinámica (ej. /pelicula/1)
      path: '/pelicula/:id',
      name: 'detalle',
      component: VistaDetalle,
    },

    {
      path: '/acceso',
      name: 'acceso',
      component: VistaAutenticacion,
    },

    {
      path: '/series',
      name: 'series',
      component: VistaSeries,
    },
    {
      path:'/admin',
      name: 'admin',
      component: VistaAdmin
    },
    {
      path: '/favoritos',
      name: 'favoritos',
      component: vistaFavoritos,
    },
  ],
})

export default router
