import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { useAuth, useUser, useClerk } from '@clerk/vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  // Clerk composables
  const { isSignedIn, isLoaded: authLoaded } = useAuth()
  const { user: clerkUser, isLoaded: userLoaded } = useUser()
  const clerk = useClerk()

  // Local state
  const localUser = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Computed
  const isAuthenticated = computed(() => isSignedIn.value)
  const isLoaded = computed(() => authLoaded.value && userLoaded.value)

  // Watch for sign-in changes to fetch local user
  watch(isSignedIn, async (signedIn) => {
    if (signedIn) {
      await fetchLocalUser()
    } else {
      localUser.value = null
    }
  }, { immediate: true })

  /**
   * Fetch the local user from our backend.
   * This syncs Clerk auth with our Supabase user data.
   */
  async function fetchLocalUser() {
    if (!isSignedIn.value) return

    loading.value = true
    try {
      const { data } = await api.get('/api/auth/me')
      if (data.success) {
        localUser.value = data.data.user
      }
    } catch (err) {
      // User might not be synced yet (webhook delay)
      console.warn('Could not fetch local user:', err)
      localUser.value = null
    } finally {
      loading.value = false
    }
  }

  /**
   * Check session - for compatibility with existing code.
   * With Clerk, this just triggers a local user fetch if signed in.
   */
  async function checkSession() {
    if (isSignedIn.value) {
      await fetchLocalUser()
    }
  }

  /**
   * Sign out using Clerk.
   */
  async function logout() {
    loading.value = true
    try {
      await clerk.value.signOut()
      localUser.value = null
    } catch (err) {
      error.value = 'Logout failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Clear any error messages.
   */
  function clearError() {
    error.value = null
  }

  /**
   * Set an error message.
   */
  function setError(message) {
    error.value = message
  }

  return {
    // State
    user: localUser,
    clerkUser,
    loading,
    error,
    isLoaded,

    // Computed
    isAuthenticated,

    // Actions
    checkSession,
    fetchLocalUser,
    logout,
    clearError,
    setError
  }
})
