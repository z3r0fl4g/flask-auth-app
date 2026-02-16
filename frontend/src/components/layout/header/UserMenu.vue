<template>
  <div class="relative">
    <button
      class="flex items-center gap-2 rounded-full border border-gray-200 bg-white py-1.5 pl-1.5 pr-3 hover:bg-gray-50 transition-colors"
      @click="isOpen = !isOpen"
    >
      <div class="flex h-8 w-8 items-center justify-center rounded-full bg-violet-100 text-sm font-semibold text-violet-600">
        {{ userInitial }}
      </div>
      <span class="hidden text-sm font-medium text-gray-700 sm:block">{{ userName }}</span>
      <ChevronDown :size="14" class="text-gray-400" />
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
        class="absolute right-0 mt-2 w-56 rounded-xl border border-gray-200 bg-white shadow-lg"
      >
        <div class="border-b border-gray-100 px-4 py-3">
          <p class="text-sm font-semibold text-gray-900">{{ userName }}</p>
          <p class="text-xs text-gray-500">{{ userEmail }}</p>
        </div>
        <div class="py-1">
          <RouterLink
            to="/profile"
            class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
            @click="isOpen = false"
          >
            <UserIcon :size="16" class="text-gray-400" />
            Profile
          </RouterLink>
          <RouterLink
            to="/"
            class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
            @click="isOpen = false"
          >
            <Home :size="16" class="text-gray-400" />
            Back to Site
          </RouterLink>
        </div>
        <div class="border-t border-gray-100 py-1">
          <button
            class="flex w-full items-center gap-2 px-4 py-2 text-sm text-red-600 hover:bg-red-50"
            @click="handleSignOut"
          >
            <LogOut :size="16" class="text-red-400" />
            Sign Out
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useUser, useClerk } from '@clerk/vue'
import { ChevronDown, User as UserIcon, Home, LogOut } from 'lucide-vue-next'

const { user } = useUser()
const clerk = useClerk()
const isOpen = ref(false)

const userName = computed(() => user.value?.fullName || user.value?.firstName || 'User')
const userEmail = computed(() => user.value?.primaryEmailAddress?.emailAddress || '')
const userInitial = computed(() => userName.value.charAt(0).toUpperCase())

async function handleSignOut() {
  isOpen.value = false
  await clerk.value.signOut()
}

function handleClickOutside(e) {
  if (isOpen.value && !e.target.closest('.relative')) {
    isOpen.value = false
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onUnmounted(() => document.removeEventListener('click', handleClickOutside))
</script>
