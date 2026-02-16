<template>
  <aside
    :class="[
      'fixed left-0 top-0 z-50 flex h-screen flex-col border-r border-gray-200 bg-white transition-all duration-300 ease-in-out',
      'lg:translate-x-0',
      isMobileOpen ? 'translate-x-0' : '-translate-x-full',
      isExpanded || isHovered ? 'w-64' : 'lg:w-20',
      'lg:static'
    ]"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <!-- Logo -->
    <div class="flex h-16 items-center border-b border-gray-200 px-4">
      <RouterLink to="/" class="flex items-center gap-3">
        <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-violet-500 to-violet-400 text-white font-bold text-lg">
          T
        </div>
        <span
          v-if="isExpanded || isHovered"
          class="text-lg font-bold text-headline whitespace-nowrap"
        >
          Tikepam
        </span>
      </RouterLink>

      <!-- Close button (mobile) -->
      <button
        class="ml-auto lg:hidden text-gray-500 hover:text-gray-700"
        @click="toggleMobileSidebar"
      >
        <X :size="20" />
      </button>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 overflow-y-auto px-3 py-4">
      <ul class="space-y-1">
        <li v-for="item in menuItems" :key="item.name">
          <RouterLink
            :to="item.path"
            :class="[
              'flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors duration-150',
              isActive(item.path)
                ? 'bg-violet-50 text-violet-700'
                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
            ]"
            @click="isMobileOpen && toggleMobileSidebar()"
          >
            <component
              :is="item.icon"
              :size="20"
              :class="[
                'shrink-0',
                isActive(item.path) ? 'text-violet-500' : 'text-gray-400'
              ]"
            />
            <span v-if="isExpanded || isHovered" class="whitespace-nowrap">
              {{ item.label }}
            </span>
          </RouterLink>
        </li>
      </ul>

      <!-- Divider -->
      <div class="my-4 border-t border-gray-100" />

      <!-- Back to site -->
      <RouterLink
        to="/"
        class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-50 hover:text-gray-900 transition-colors duration-150"
      >
        <ArrowLeft :size="20" class="shrink-0 text-gray-400" />
        <span v-if="isExpanded || isHovered" class="whitespace-nowrap">Back to Site</span>
      </RouterLink>
    </nav>
  </aside>
</template>

<script setup>
import { RouterLink, useRoute } from 'vue-router'
import { useSidebar } from '@/composables/useSidebar'
import {
  LayoutDashboard,
  PlusCircle,
  Ticket,
  ShoppingCart,
  BarChart3,
  ScanLine,
  ArrowLeft,
  X
} from 'lucide-vue-next'

const route = useRoute()
const { isExpanded, isMobileOpen, isHovered, toggleMobileSidebar } = useSidebar()

const menuItems = [
  { name: 'my-events', label: 'My Events', path: '/my-events', icon: LayoutDashboard },
  { name: 'create-event', label: 'Create Event', path: '/create-event', icon: PlusCircle },
  { name: 'my-tickets', label: 'My Tickets', path: '/my-tickets', icon: Ticket },
  { name: 'orders', label: 'Orders', path: '/orders', icon: ShoppingCart },
  { name: 'analytics', label: 'Analytics', path: '/analytics', icon: BarChart3 },
  { name: 'check-in', label: 'Check-In', path: '/check-in', icon: ScanLine }
]

function isActive(path) {
  return route.path === path
}
</script>
