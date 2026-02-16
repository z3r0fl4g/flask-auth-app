<template>
  <div class="rounded-xl border border-gray-200 bg-white p-5">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-sm font-medium text-gray-500">{{ label }}</p>
        <p class="mt-1 text-2xl font-bold text-gray-900">{{ value }}</p>
        <p v-if="change" :class="['mt-1 text-xs font-medium', changePositive ? 'text-green-600' : 'text-red-600']">
          {{ changePositive ? '+' : '' }}{{ change }}
          <span class="text-gray-400 font-normal">vs last month</span>
        </p>
      </div>
      <div
        :class="[
          'flex h-12 w-12 items-center justify-center rounded-xl',
          iconBgClass
        ]"
      >
        <component :is="icon" :size="22" :class="iconTextClass" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: { type: String, required: true },
  value: { type: [String, Number], required: true },
  change: { type: String, default: '' },
  icon: { type: Object, required: true },
  variant: { type: String, default: 'violet' }
})

const changePositive = computed(() => {
  if (!props.change) return false
  return !props.change.startsWith('-')
})

const iconBgClass = computed(() => {
  const map = {
    violet: 'bg-violet-50',
    green: 'bg-green-50',
    blue: 'bg-blue-50',
    amber: 'bg-amber-50',
    red: 'bg-red-50'
  }
  return map[props.variant] || map.violet
})

const iconTextClass = computed(() => {
  const map = {
    violet: 'text-violet-500',
    green: 'text-green-500',
    blue: 'text-blue-500',
    amber: 'text-amber-500',
    red: 'text-red-500'
  }
  return map[props.variant] || map.violet
})
</script>
