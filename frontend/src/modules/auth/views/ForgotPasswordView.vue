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
            <h1 class="mt-4 text-2xl font-semibold text-gray-900">Reset your password</h1>
            <p class="text-sm text-gray-500">Enter your email and we'll send a secure link to get you back into Tikepam.</p>
          </div>

          <!-- Success Message -->
          <div v-if="success" class="mb-6 rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700">
            {{ success }}
          </div>

          <!-- Error Message -->
          <div v-if="error" class="mb-6 rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-600">
            {{ error }}
          </div>

          <form @submit.prevent="handleSubmit" class="space-y-5">
            <div class="space-y-2">
              <label for="email" class="text-sm font-medium text-gray-700">Email address</label>
              <div class="relative">
                <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </span>
                <input
                  id="email"
                  v-model="email"
                  type="email"
                  placeholder="name@email.com"
                  required
                  class="w-full rounded-2xl border border-gray-200 bg-white pl-10 pr-4 py-3 text-sm text-gray-700 shadow-sm focus:border-[#8338ec]/60 focus:outline-none focus:ring-2 focus:ring-[#8338ec]/20"
                />
              </div>
            </div>

            <button
              type="submit"
              :disabled="loading"
              class="btn-primary w-full justify-center"
            >
              {{ loading ? 'Sending...' : 'Send secure link' }}
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </button>
          </form>

          <div class="mt-8 flex flex-col gap-3 text-sm text-gray-600">
            <div class="rounded-2xl border border-dashed border-gray-300 bg-gray-50 px-5 py-4">
              <p class="font-semibold text-gray-700">Didn't see the email?</p>
              <p class="text-xs text-gray-500 mt-1">Peek at spam or request another reset in a few minutes.</p>
            </div>
            <div class="text-center">
              <span class="mr-1">Remember your password?</span>
              <router-link to="/login" class="font-semibold text-[#8338ec] hover:text-[#6414d5] transition">
                Sign in
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/services/api'

const email = ref('')
const loading = ref(false)
const error = ref(null)
const success = ref(null)

async function handleSubmit() {
  loading.value = true
  error.value = null
  success.value = null

  try {
    const { data } = await api.post('/api/auth/forgot-password', { email: email.value })
    if (data.success) {
      success.value = data.message || 'If an account exists, a password reset link has been sent to your email.'
      email.value = ''
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to send reset link. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
