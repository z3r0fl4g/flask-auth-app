<template>
  <header class="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-gray-200 bg-white px-4 sm:px-6">
    <!-- Left: hamburger + breadcrumb -->
    <div class="flex items-center gap-3">
      <!-- Mobile menu toggle -->
      <button
        class="lg:hidden flex h-10 w-10 items-center justify-center rounded-full text-gray-500 hover:text-gray-700 hover:bg-gray-100 transition-colors"
        @click="toggleMobileSidebar"
      >
        <Menu :size="20" />
      </button>

      <!-- Desktop sidebar toggle -->
      <button
        class="hidden lg:flex h-10 w-10 items-center justify-center rounded-full text-gray-500 hover:text-gray-700 hover:bg-gray-100 transition-colors"
        @click="toggleSidebar"
      >
        <PanelLeftClose v-if="isExpanded" :size="20" />
        <PanelLeftOpen v-else :size="20" />
      </button>

      <!-- Breadcrumb -->
      <div class="hidden sm:block text-sm text-gray-500">
        <span class="text-gray-400">Dashboard</span>
        <span class="mx-1.5 text-gray-300">/</span>
        <span class="font-medium text-gray-900">{{ pageTitle }}</span>
      </div>
    </div>

    <!-- Right: search, notifications, profile -->
    <div class="flex items-center gap-2">
      <SearchBar />
      <NotificationMenu />
      <UserMenu />
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useSidebar } from '@/composables/useSidebar'
import { Menu, PanelLeftClose, PanelLeftOpen } from 'lucide-vue-next'
import SearchBar from './header/SearchBar.vue'
import NotificationMenu from './header/NotificationMenu.vue'
import UserMenu from './header/UserMenu.vue'

const route = useRoute()
const { isExpanded, toggleSidebar, toggleMobileSidebar } = useSidebar()

const pageTitle = computed(() => route.meta.title || route.name || 'Dashboard')
</script>
