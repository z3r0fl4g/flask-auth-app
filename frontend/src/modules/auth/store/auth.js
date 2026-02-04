import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!user.value)
  const requires2FA = computed(() => !user.value || !user.value.twofa_verified)

  async function checkSession() {
    loading.value = true
    try {
      const { data } = await api.get('/api/auth/session')
      if (data.data?.authenticated) {
        user.value = data.data.user
      } else {
        user.value = null
      }
    } catch (err) {
      user.value = null
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  async function login(email, password) {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.post('/api/auth/login', { email, password })
      if (data.success) {
        if (data.data.requires_2fa) {
          return { success: true, requires2FA: true }
        }
        user.value = data.data.user
        return { success: true, requires2FA: false }
      }
    } catch (err) {
      error.value = err.response?.data?.message || 'Login failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function signup(email, password, fullname) {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.post('/api/auth/signup', { email, password, fullname })
      if (data.success) {
        return { success: true, requires2FA: data.data.requires_2fa }
      }
    } catch (err) {
      error.value = err.response?.data?.message || 'Signup failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function verify2FA(code) {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.post('/api/2fa/verify', { code })
      if (data.success) {
        user.value = data.data.user
        return { success: true }
      }
    } catch (err) {
      error.value = err.response?.data?.message || 'Verification failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    await api.post('/api/auth/logout')
    user.value = null
  }

  function clearError() {
    error.value = null
  }

  return {
    user,
    loading,
    error,
    isAuthenticated,
    requires2FA,
    checkSession,
    login,
    signup,
    verify2FA,
    logout,
    clearError
  }
})
