<template>
  <div class="relative hidden sm:block">
    <Search :size="18" class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
    <input
      type="text"
      placeholder="Search events..."
      class="h-10 w-64 rounded-full border border-gray-200 bg-gray-50 pl-10 pr-4 text-sm text-gray-700 placeholder-gray-400 focus:outline-hidden focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 transition-all"
    />
  </div>
</template>

<script setup>
import { Search } from 'lucide-vue-next'
</script>
