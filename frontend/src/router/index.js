import { createRouter, createWebHistory } from 'vue-router'

// Import module routes
import { authRoutes } from '@/modules/auth/routes'
import { eventsRoutes } from '@/modules/events/routes'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    // Auth module routes (login, signup, profile, 2fa, home)
    ...authRoutes,
    // Events module routes
    ...eventsRoutes
  ]
})

// Update document title on navigation
router.afterEach((to) => {
  if (to.meta.title) {
    document.title = to.meta.title
  }
})

export default router
