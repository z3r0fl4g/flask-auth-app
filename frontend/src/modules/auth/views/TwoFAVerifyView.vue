<template>
  <div class="fixed inset-0 flex items-center justify-center py-12 px-4">
    <div class="max-w-md w-full">
      <div class="card p-8 shadow-lg shadow-gray-200/60">
        <!-- Header -->
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold text-headline">
            Check your inbox
          </h1>
          <p class="mt-3 text-body">
            We just sent a 6-digit verification code to your email. Enter it below to continue.
          </p>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="mb-6 px-4 py-3 rounded-2xl bg-red-50 border border-red-200 text-red-800 text-sm">
          {{ error }}
        </div>

        <!-- OTP Input -->
        <div class="mb-6">
          <OTPInput
            ref="otpInputRef"
            :error="!!error"
            @complete="handleComplete"
          />
        </div>

        <!-- Continue Button -->
        <button
          @click="verify"
          :disabled="loading || !code || code.length !== 6"
          class="btn-primary w-full justify-center"
        >
          {{ loading ? 'Verifying...' : 'Continue' }}
        </button>

        <p class="mt-5 text-center text-xs text-muted">
          This code expires in 15 minutes. Didn't get it?
          <button
            @click="resend"
            :disabled="resending"
            class="text-violet-500 hover:underline font-medium disabled:opacity-50"
          >
            {{ resending ? 'Sending...' : 'Resend code' }}
          </button>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import OTPInput from '../components/OTPInput.vue'

const router = useRouter()
const authStore = useAuthStore()

const code = ref('')
const loading = ref(false)
const resending = ref(false)
const error = ref(null)
const otpInputRef = ref(null)

function handleComplete(value) {
  code.value = value
  verify()
}

async function verify() {
  if (!code.value || code.value.length !== 6) return

  loading.value = true
  error.value = null
  try {
    const { data } = await api.post('/api/2fa/verify', { code: code.value })
    if (data.success) {
      authStore.user = data.data.user
      router.push('/profile')
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'Invalid or expired code'
    code.value = ''
    // Reset OTP input on error
    if (otpInputRef.value) {
      otpInputRef.value.reset()
    }
  } finally {
    loading.value = false
  }
}

async function resend() {
  resending.value = true
  error.value = null
  try {
    const { data } = await api.post('/api/2fa/resend')
    // Show success message
    alert(data.message || 'New code sent!')
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to resend code'
  } finally {
    resending.value = false
  }
}
</script>
