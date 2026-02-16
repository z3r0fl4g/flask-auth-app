<template>
  <div class="min-h-screen" :class="{ 'bg-background': currentLayout === 'public' }">
    <!-- Ambient glows only on public layout -->
    <div v-if="currentLayout === 'public'" class="ambient-bg">
      <div class="glow glow-rose" style="width:42rem;height:42rem;top:-14rem;right:-18rem;"></div>
      <div class="glow glow-amber" style="width:38rem;height:38rem;bottom:-16rem;left:-12rem;"></div>
      <div class="glow glow-orange" style="width:30rem;height:30rem;top:40%;left:48%;transform:translateX(-48%);"></div>
    </div>

    <!-- Dynamic layout resolution -->
    <component :is="layoutComponent">
      <router-view />
    </component>

    <!-- Toast notifications -->
    <Toaster position="top-center" :toastOptions="{ class: 'font-sans' }" />
  </div>
</template>

<script setup>
import { computed, watchEffect } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth } from '@clerk/vue'
import { Toaster } from 'vue-sonner'
import { useSidebarProvider } from '@/composables/useSidebar'
import AppLayout from '@/components/layout/AppLayout.vue'
import OrganizerLayout from '@/components/layout/OrganizerLayout.vue'
import { setClerkTokenGetter } from '@/services/api'

const route = useRoute()
const { getToken, isLoaded } = useAuth()

// Initialize sidebar state for entire app
useSidebarProvider()

// Set up Clerk token getter for API requests
watchEffect(() => {
  if (isLoaded.value) {
    setClerkTokenGetter(() => getToken.value())
  }
})

// Determine layout based on route meta
const currentLayout = computed(() => route.meta.layout || 'public')

const layoutComponent = computed(() => {
  return currentLayout.value === 'organizer' ? OrganizerLayout : AppLayout
})
</script>
