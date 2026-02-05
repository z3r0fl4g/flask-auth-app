// Auth module routes
import { useAuth } from '@clerk/vue'

// Auth views
import LoginView from '../views/LoginView.vue'
import SignupView from '../views/SignupView.vue'
import ForgotPasswordView from '../views/ForgotPasswordView.vue'
import ResetPasswordView from '../views/ResetPasswordView.vue'
import TwoFAVerifyView from '../views/TwoFAVerifyView.vue'
import TwoFASettingsView from '../views/TwoFASettingsView.vue'
import ProfileView from '../views/ProfileView.vue'
import HomeView from '../views/HomeView.vue'
import SSOCallbackView from '../views/SSOCallbackView.vue'

// Navigation guards using Clerk
const requiresAuth = async (to, from, next) => {
  const { isSignedIn, isLoaded } = useAuth()

  // Wait for Clerk to load
  if (!isLoaded.value) {
    // Wait a bit and try again
    await new Promise(resolve => setTimeout(resolve, 100))
  }

  if (!isSignedIn.value) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
}

const requiresGuest = async (to, from, next) => {
  const { isSignedIn, isLoaded } = useAuth()

  // Wait for Clerk to load
  if (!isLoaded.value) {
    await new Promise(resolve => setTimeout(resolve, 100))
  }

  if (isSignedIn.value) {
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

  // SSO callback for OAuth redirects
  {
    path: '/sso-callback',
    name: 'sso-callback',
    component: SSOCallbackView,
    meta: { title: 'Signing in...' }
  },

  // 2FA/Verification routes
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
