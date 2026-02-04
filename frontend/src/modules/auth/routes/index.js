// Auth module routes - mirrors backend auth/ module structure
import { useAuthStore } from '../store/auth'

// Auth views
import LoginView from '../views/LoginView.vue'
import SignupView from '../views/SignupView.vue'
import ForgotPasswordView from '../views/ForgotPasswordView.vue'
import ResetPasswordView from '../views/ResetPasswordView.vue'
import TwoFAVerifyView from '../views/TwoFAVerifyView.vue'
import TwoFASettingsView from '../views/TwoFASettingsView.vue'
import ProfileView from '../views/ProfileView.vue'
import HomeView from '../views/HomeView.vue'

// Navigation guards
const requiresAuth = async (to, from, next) => {
  const authStore = useAuthStore()

  // Check session if not already loaded
  if (!authStore.user && !authStore.loading) {
    await authStore.checkSession()
  }

  if (!authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
}

const requiresGuest = async (to, from, next) => {
  const authStore = useAuthStore()

  // Check session if not already loaded
  if (!authStore.user && !authStore.loading) {
    await authStore.checkSession()
  }

  if (authStore.isAuthenticated) {
    next({ name: 'profile' })
  } else {
    next()
  }
}

// Auth module routes
export const authRoutes = [
  // Public routes (guest only)
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    beforeEnter: requiresGuest,
    meta: { title: 'Log In - Tikepam' }
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupView,
    beforeEnter: requiresGuest,
    meta: { title: 'Sign Up - Tikepam' }
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: ForgotPasswordView,
    meta: { title: 'Reset Password - Tikepam' }
  },
  {
    path: '/reset-password/:token',
    name: 'reset-password',
    component: ResetPasswordView,
    meta: { title: 'Set New Password - Tikepam' }
  },

  // 2FA routes
  {
    path: '/2fa/verify',
    name: 'twofa-verify',
    component: TwoFAVerifyView,
    meta: { title: 'Verify Code - Tikepam' }
  },
  {
    path: '/2fa/settings',
    name: 'twofa-settings',
    component: TwoFASettingsView,
    beforeEnter: requiresAuth,
    meta: { title: 'Security Settings - Tikepam' }
  },

  // Protected routes
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    beforeEnter: requiresAuth,
    meta: { title: 'Your Profile - Tikepam' }
  },

  // Home/Landing page
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { title: 'Tikepam - Real Haitian Events' }
  }
]

export default authRoutes
