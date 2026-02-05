<template>
  <div class="fixed inset-0 flex items-center justify-center bg-background">
    <div class="text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-violet-600 mx-auto mb-4"></div>
      <p class="text-gray-600">Completing sign in...</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useClerk } from '@clerk/vue'

const router = useRouter()
const clerk = useClerk()

onMounted(async () => {
  try {
    // Handle the OAuth callback
    await clerk.value.handleRedirectCallback()
    // Redirect to profile after successful auth
    router.push('/profile')
  } catch (err) {
    console.error('SSO callback error:', err)
    router.push('/login')
  }
})
</script>
