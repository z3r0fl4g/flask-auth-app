import axios from 'axios'
import router from '@/router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',  // Use Vite proxy (same origin) in dev
  headers: {
    'Content-Type': 'application/json'
  }
})

// Store for the getToken function (set by ClerkTokenProvider)
let getTokenFn = null

/**
 * Set the Clerk getToken function.
 * Called from App.vue after Clerk is loaded.
 */
export function setClerkTokenGetter(fn) {
  getTokenFn = fn
}

// Request interceptor - add Clerk JWT token
api.interceptors.request.use(
  async (config) => {
    if (getTokenFn) {
      try {
        const token = await getTokenFn()
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
      } catch (err) {
        console.warn('Could not get Clerk token:', err)
      }
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      const url = error.config?.url || ''
      // Only redirect to login for protected endpoints
      if (!url.includes('/api/auth/session') && !url.includes('/api/auth/me')) {
        router.push('/login')
      }
    }
    return Promise.reject(error)
  }
)

export default api
