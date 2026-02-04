import axios from 'axios'
import router from '@/router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',  // Use Vite proxy (same origin) in dev
  withCredentials: true,  // Send cookies
  headers: {
    'Content-Type': 'application/json'
  }
})

// Response interceptor
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      const url = error.config?.url || ''
      if (!url.includes('/api/auth/login') && !url.includes('/api/auth/signup')) {
        router.push('/login')
      }
    } else if (error.response?.status === 403) {
      if (error.response.data?.error === 'VERIFICATION_REQUIRED') {
        router.push('/2fa/verify')
      }
    }
    return Promise.reject(error)
  }
)

export default api
