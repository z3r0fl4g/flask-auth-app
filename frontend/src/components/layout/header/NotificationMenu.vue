<template>
  <div class="relative">
    <button
      class="flex h-10 w-10 items-center justify-center rounded-full border border-gray-200 bg-white text-gray-500 hover:text-gray-700 hover:bg-gray-50 transition-colors"
      @click="isOpen = !isOpen"
    >
      <Bell :size="18" />
    </button>

    <!-- Dropdown -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      leave-active-class="transition duration-100 ease-in"
      enter-from-class="opacity-0 scale-95"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isOpen"
        class="absolute right-0 mt-2 w-72 rounded-xl border border-gray-200 bg-white shadow-lg"
      >
        <div class="border-b border-gray-100 px-4 py-3">
          <h3 class="text-sm font-semibold text-gray-900">Notifications</h3>
        </div>
        <div class="px-4 py-6 text-center text-sm text-gray-500">
          No new notifications
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Bell } from 'lucide-vue-next'

const isOpen = ref(false)

function handleClickOutside(e) {
  if (isOpen.value && !e.target.closest('.relative')) {
    isOpen.value = false
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onUnmounted(() => document.removeEventListener('click', handleClickOutside))
</script>
