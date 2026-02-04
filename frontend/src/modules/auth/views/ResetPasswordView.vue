<template>
  <section class="relative">
    <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6">
      <div class="max-w-3xl w-full">
        <div class="card p-8">
          <div class="text-center mb-8">
            <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-[#8338ec]/15 text-[#8338ec]">
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
              </svg>
            </div>
            <h1 class="mt-4 text-2xl font-semibold text-gray-900">Set a new password</h1>
            <p class="text-sm text-gray-500">Choose a fresh, secure password to protect your Tikepam account.</p>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="mb-6 rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-600">
            {{ error }}
          </div>

          <form @submit.prevent="handleSubmit" class="space-y-5">
            <!-- New Password -->
            <div class="space-y-2">
              <label for="password" class="text-sm font-medium text-gray-700">New password</label>
              <PasswordInput
                id="password"
                v-model="password"
                placeholder="Create a new password"
                autocomplete="new-password"
                :error="passwordError"
                required
              />
              <p class="text-xs text-gray-500">Use 8+ characters with letters, numbers, and symbols.</p>
            </div>

            <!-- Confirm Password -->
            <div class="space-y-2">
              <label for="confirm-password" class="text-sm font-medium text-gray-700">Confirm password</label>
              <div class="relative">
                <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400 z-10">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </span>
                <input
                  id="confirm-password"
                  v-model="confirmPassword"
                  type="password"
                  placeholder="Re-enter your new password"
                  required
                  autocomplete="new-password"
                  class="w-full rounded-2xl border border-gray-200 bg-white pl-10 pr-4 py-3 text-sm text-gray-700 shadow-sm focus:border-[#8338ec]/60 focus:outline-none focus:ring-2 focus:ring-[#8338ec]/20"
                  :class="{ 'border-rose-500': confirmError }"
                />
              </div>
              <p
                v-if="confirmError"
                class="text-xs text-rose-500"
              >
                Passwords do not match
              </p>
            </div>

            <button
              type="submit"
              :disabled="loading"
              class="btn-primary w-full justify-center"
            >
              {{ loading ? 'Saving...' : 'Save new password' }}
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </button>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/services/api'
import { useFormValidation } from '../composables/useFormValidation'
import PasswordInput from '../components/PasswordInput.vue'

const router = useRouter()
const route = useRoute()
const { validatePassword, validatePasswordConfirmation } = useFormValidation()

const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref(null)

const passwordError = computed(() => {
  const result = validatePassword(password.value, true, true)
  return result.showError
})

const confirmError = computed(() => {
  if (!confirmPassword.value) return false
  return password.value !== confirmPassword.value
})

async function handleSubmit() {
  // Validate
  if (passwordError.value || confirmError.value) {
    error.value = 'Please fix the errors before submitting'
    return
  }

  loading.value = true
  error.value = null

  try {
    const token = route.params.token
    const { data } = await api.post('/api/auth/reset-password', {
      token,
      password: password.value
    })

    if (data.success) {
      // Redirect to login with success message
      router.push({ name: 'login', query: { reset: 'success' } })
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to reset password. The link may have expired.'
  } finally {
    loading.value = false
  }
}
</script>
