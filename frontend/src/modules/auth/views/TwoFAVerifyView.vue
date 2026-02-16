<template>
  <div class="fixed inset-0 flex items-center justify-center py-12 px-4">
    <div class="max-w-md w-full">
      <div class="card p-8 shadow-lg shadow-gray-200/60">
        <!-- Header -->
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold text-headline">
            {{ isSignupMode ? 'Verify your email' : 'Two-factor authentication' }}
          </h1>
          <p class="mt-3 text-body">
            {{ isSignupMode
              ? 'We just sent a 6-digit verification code to your email. Enter it below to continue.'
              : 'Enter the verification code to complete sign-in.'
            }}
          </p>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="mb-6 px-4 py-3 rounded-xl bg-red-50 border border-red-300 text-red-800 text-sm">
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
          This code expires in 10 minutes. Didn't get it?
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
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useSignIn, useSignUp } from '@clerk/vue'
import { toast } from 'vue-sonner'
import OTPInput from '../components/OTPInput.vue'

const router = useRouter()
const route = useRoute()
const { signIn, setActive: setActiveSignIn, isLoaded: signInLoaded } = useSignIn()
const { signUp, setActive: setActiveSignUp, isLoaded: signUpLoaded } = useSignUp()

const code = ref('')
const loading = ref(false)
const resending = ref(false)
const error = ref(null)
const otpInputRef = ref(null)

// Determine if this is signup email verification or login 2FA
const isSignupMode = computed(() => route.query.mode === 'signup')

function handleComplete(value) {
  code.value = value
  verify()
}

async function verify() {
  if (!code.value || code.value.length !== 6) return

  loading.value = true
  error.value = null

  try {
    if (isSignupMode.value) {
      // Email verification for signup
      if (!signUpLoaded.value) {
        error.value = 'Authentication is loading. Please try again.'
        return
      }

      const result = await signUp.value.attemptEmailAddressVerification({
        code: code.value
      })

      if (result.status === 'complete') {
        await setActiveSignUp.value({ session: result.createdSessionId })
        router.push('/profile')
      } else {
        console.log('Verification result:', result)
        error.value = 'Please complete the verification process.'
      }
    } else {
      // 2FA for login
      if (!signInLoaded.value) {
        error.value = 'Authentication is loading. Please try again.'
        return
      }

      const result = await signIn.value.attemptSecondFactor({
        strategy: 'totp',
        code: code.value
      })

      if (result.status === 'complete') {
        await setActiveSignIn.value({ session: result.createdSessionId })
        router.push('/profile')
      } else {
        console.log('2FA result:', result)
        error.value = 'Please complete the verification process.'
      }
    }
  } catch (err) {
    console.error('Verification error:', err)
    error.value = err.errors?.[0]?.longMessage || err.errors?.[0]?.message || 'Invalid or expired code'
    code.value = ''
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
    if (isSignupMode.value) {
      // Resend signup verification email
      if (!signUpLoaded.value) return
      await signUp.value.prepareEmailAddressVerification({
        strategy: 'email_code'
      })
    } else {
      // For 2FA, this typically isn't resendable in the same way
      // TOTP codes are generated on device, not sent
      error.value = 'Please use your authenticator app to get a new code.'
      resending.value = false
      return
    }
    toast.success('New code sent!')
    error.value = null
  } catch (err) {
    console.error('Resend error:', err)
    error.value = err.errors?.[0]?.message || 'Failed to resend code'
  } finally {
    resending.value = false
  }
}
</script>
