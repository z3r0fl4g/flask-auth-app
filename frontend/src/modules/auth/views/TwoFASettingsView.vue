<template>
  <section class="relative">
    <div class="min-h-screen py-12 px-4 sm:px-6">
      <!-- Background gradient -->
      <div class="absolute inset-x-0 -top-32 h-56 max-w-4xl mx-auto bg-gradient-to-r from-[#d7e6ff]/50 via-white to-[#ffe59d]/50 blur-3xl"></div>

      <div class="max-w-4xl mx-auto">
        <div class="rounded-3xl border border-gray-200 bg-white/90 p-8 shadow-xl shadow-gray-200/60">
          <!-- Header -->
          <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between mb-8">
            <div class="flex items-center gap-4">
              <div class="h-12 w-12 rounded-full bg-[#8338ec]/15 flex items-center justify-center text-[#8338ec]">
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <div>
                <h1 class="text-2xl font-semibold text-gray-900">Security & 2FA</h1>
                <p class="text-sm text-gray-500">Add extra verification so only you can access your tickets and payouts.</p>
              </div>
            </div>
            <span class="inline-flex items-center gap-2 rounded-full border border-gray-200 bg-gray-50 px-4 py-1.5 text-xs font-semibold text-gray-600">
              <svg class="h-4 w-4 text-[#8338ec]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              Status: {{ authStore.user?.twofa_enabled ? 'Enabled' : 'Disabled' }}
            </span>
          </div>

          <!-- Flash Messages -->
          <div v-if="message" class="mb-6 rounded-2xl border px-4 py-3 text-sm" :class="messageClass">
            {{ message }}
          </div>

          <!-- Form -->
          <form @submit.prevent="handleSubmit" class="space-y-6">
            <div class="rounded-3xl border border-gray-200 bg-gray-50 px-6 py-6">
              <label class="flex items-start gap-3">
                <input
                  type="checkbox"
                  v-model="enable2FA"
                  class="mt-1 h-5 w-5 rounded border-gray-300 text-[#8338ec] focus:ring-[#8338ec]"
                />
                <div>
                  <span class="text-lg font-semibold text-gray-900">Turn on two-factor authentication</span>
                  <p class="text-sm text-gray-600 mt-1">
                    Require a secure code after your password to block unwanted access.
                  </p>
                </div>
              </label>

              <div class="mt-6 space-y-4 pl-8" :class="{ 'opacity-50': !enable2FA }">
                <!-- Email verification -->
                <div class="flex items-center gap-3">
                  <div class="h-9 w-9 rounded-full bg-[#d7e6ff]/70 flex items-center justify-center text-[#3a86ff]">
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-sm font-semibold text-gray-800">Email verification</p>
                    <p class="text-xs text-gray-500">Codes arrive instantly at {{ authStore.user?.email }}</p>
                  </div>
                  <span class="ml-auto text-xs rounded-full bg-[#d7e6ff]/70 px-3 py-1 font-semibold text-[#00307c]">Active</span>
                </div>

                <!-- SMS verification (disabled) -->
                <div class="flex items-center gap-3 text-gray-400">
                  <div class="h-9 w-9 rounded-full bg-gray-100 flex items-center justify-center">
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-sm font-semibold">SMS verification</p>
                    <p class="text-xs">Secure text codes launching soon</p>
                  </div>
                </div>

                <!-- Authenticator app (disabled) -->
                <div class="flex items-center gap-3 text-gray-400">
                  <div class="h-9 w-9 rounded-full bg-gray-100 flex items-center justify-center">
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-sm font-semibold">Authenticator app</p>
                    <p class="text-xs">App-based tokens coming soon</p>
                  </div>
                </div>
              </div>
            </div>

            <button
              type="submit"
              :disabled="loading"
              class="btn-primary"
            >
              {{ loading ? 'Saving...' : 'Save security settings' }}
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </button>
          </form>

          <!-- Recovery options (only show if 2FA enabled) -->
          <div v-if="authStore.user?.twofa_enabled" class="mt-12 space-y-4 border-t border-gray-200 pt-8">
            <h3 class="text-lg font-semibold text-gray-900">Recovery options</h3>
            <div class="rounded-3xl border border-gray-200 bg-white px-6 py-5 shadow-sm">
              <div class="flex items-center gap-4">
                <div class="h-10 w-10 rounded-full bg-[#ffe59d]/60 flex items-center justify-center text-[#9f7500]">
                  <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                </div>
                <div class="flex-1">
                  <p class="text-sm font-semibold text-gray-800">Resend verification code</p>
                  <p class="text-xs text-gray-500">Code expired or missing? Trigger another email instantly.</p>
                </div>
                <button
                  @click="resendCode"
                  :disabled="resending"
                  class="rounded-full border border-gray-200 bg-white px-4 py-2 text-xs font-semibold text-[#8338ec] hover:border-[#8338ec]/40 hover:text-[#6414d5] transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {{ resending ? 'Sending...' : 'Resend code' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import api from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

const enable2FA = ref(false)
const loading = ref(false)
const resending = ref(false)
const message = ref(null)
const messageType = ref('info')

const messageClass = computed(() => {
  if (messageType.value === 'success') {
    return 'border-emerald-200 bg-emerald-50 text-emerald-700'
  } else if (messageType.value === 'error') {
    return 'border-rose-200 bg-rose-50 text-rose-600'
  }
  return 'border-blue-200 bg-blue-50 text-blue-700'
})

onMounted(async () => {
  // Ensure user session is loaded
  if (!authStore.user) {
    await authStore.checkSession()
  }
  enable2FA.value = authStore.user?.twofa_enabled || false
})

async function handleSubmit() {
  loading.value = true
  message.value = null

  try {
    const { data } = await api.post('/api/2fa/settings', {
      enabled: enable2FA.value
    })

    if (data.success) {
      messageType.value = 'success'
      message.value = data.message

      // If enabling 2FA, redirect to verification
      if (data.data?.requires_verification) {
        setTimeout(() => {
          router.push('/2fa/verify')
        }, 1500)
      } else {
        // Update user in store
        await authStore.checkSession()
      }
    }
  } catch (err) {
    messageType.value = 'error'
    message.value = err.response?.data?.message || 'Failed to update settings'
  } finally {
    loading.value = false
  }
}

async function resendCode() {
  resending.value = true
  message.value = null

  try {
    const { data } = await api.post('/api/2fa/resend')
    messageType.value = 'success'
    message.value = data.message || 'New code sent to your email'
  } catch (err) {
    messageType.value = 'error'
    message.value = err.response?.data?.message || 'Failed to resend code'
  } finally {
    resending.value = false
  }
}
</script>
