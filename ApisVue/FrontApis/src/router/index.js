import { createRouter, createWebHistory } from 'vue-router'
import VistaInicio from '../views/VistaInicio.vue'
import VistaDetalle from '../views/VistaDetalle.vue'
import VistaAutenticacion from '../views/VistaAutenticacion.vue'
import VistaSeries from '@/views/VistaSeries.vue'
import VistaAdmin from '@/views/VistaAdmin.vue'
import vistaFavoritos from '@/views/VistaFavoritos.vue'
import VistaPerfil from '@/views/VistaPerfil.vue'
import VistaGeneros from '@/views/VistaGeneros.vue'
import SerieDetalle from '@/views/Seriedetalle.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'inicio',
      component: VistaInicio,
    },
    {
      
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
      path: '/serieDetalle',
      name: 'SerieDetalle',
      component: SerieDetalle,
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
    {
      path:'/perfil',
      name:'perfil',
      component: VistaPerfil
    },
    {
      path:'/generos',
      name:'generos',
      component: VistaGeneros
    }
  
  ],
})

export default router
