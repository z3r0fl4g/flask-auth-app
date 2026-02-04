import { createRouter, createWebHistory } from 'vue-router'

// Import module routes
import { authRoutes } from '@/modules/auth/routes'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    // Auth module routes (login, signup, profile, 2fa, home)
    ...authRoutes
  ]
})

// Update document title on navigation
router.afterEach((to) => {
  if (to.meta.title) {
    document.title = to.meta.title
  }
})

export default router
