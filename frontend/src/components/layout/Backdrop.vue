<template>
  <transition
    enter-active-class="transition-opacity duration-200 ease-out"
    leave-active-class="transition-opacity duration-200 ease-in"
    enter-from-class="opacity-0"
    leave-to-class="opacity-0"
  >
    <div
      v-if="isMobileOpen"
      class="fixed inset-0 z-40 bg-gray-900/50 lg:hidden"
      @click="toggleMobileSidebar"
    />
  </transition>
</template>

<script setup>
import { useSidebar } from '@/composables/useSidebar'

const { isMobileOpen, toggleMobileSidebar } = useSidebar()
</script>
