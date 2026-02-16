<template>
  <span
    :class="[
      'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium',
      variantClasses
    ]"
  >
    <slot />
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'default',
    validator: (v) => ['default', 'success', 'warning', 'error', 'info', 'draft', 'published'].includes(v)
  }
})

const variantClasses = computed(() => {
  const map = {
    default: 'bg-gray-100 text-gray-700',
    success: 'bg-green-50 text-green-700 border border-green-200',
    warning: 'bg-amber-50 text-amber-700 border border-amber-200',
    error: 'bg-red-50 text-red-700 border border-red-200',
    info: 'bg-blue-50 text-blue-700 border border-blue-200',
    draft: 'bg-gray-100 text-gray-600',
    published: 'bg-green-50 text-green-700 border border-green-200'
  }
  return map[props.variant] || map.default
})
</script>
