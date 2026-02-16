import { ref, provide, inject } from 'vue'

const SIDEBAR_KEY = Symbol('sidebar')

export function useSidebarProvider() {
  const isExpanded = ref(true)
  const isMobileOpen = ref(false)
  const isHovered = ref(false)
  const activeItem = ref(null)

  function toggleSidebar() {
    isExpanded.value = !isExpanded.value
  }

  function toggleMobileSidebar() {
    isMobileOpen.value = !isMobileOpen.value
  }

  function setActiveItem(item) {
    activeItem.value = item
  }

  const state = {
    isExpanded,
    isMobileOpen,
    isHovered,
    activeItem,
    toggleSidebar,
    toggleMobileSidebar,
    setActiveItem
  }

  provide(SIDEBAR_KEY, state)
  return state
}

export function useSidebar() {
  const state = inject(SIDEBAR_KEY)
  if (!state) {
    throw new Error('useSidebar() must be used within a component that calls useSidebarProvider()')
  }
  return state
}
