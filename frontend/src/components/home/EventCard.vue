<template>
  <article
    class="group relative overflow-hidden rounded-3xl border border-gray-200 bg-white shadow-lg shadow-gray-200/50 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl"
  >
    <!-- Event Image -->
    <div class="relative h-48 overflow-hidden">
      <div
        class="absolute inset-0 bg-gradient-to-br from-violet-500/20 via-rose-500/10 to-amber-500/20"
        :style="image ? {} : { background: `linear-gradient(135deg, ${gradientColors[0]}, ${gradientColors[1]})` }"
      >
        <img
          v-if="image"
          :src="image"
          :alt="title"
          class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
        />
      </div>
      <!-- Category Badge -->
      <span
        class="absolute left-4 top-4 inline-flex items-center gap-1.5 rounded-full bg-white/90 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-gray-700 backdrop-blur-sm"
      >
        <span class="h-2 w-2 rounded-full" :class="categoryColor"></span>
        {{ category }}
      </span>
    </div>

    <!-- Event Details -->
    <div class="p-5">
      <!-- Location -->
      <div class="mb-2 flex items-center gap-1.5 text-sm text-gray-500">
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        {{ location }}
      </div>

      <!-- Title -->
      <h3 class="mb-2 text-lg font-semibold text-gray-900 line-clamp-2">
        {{ title }}
      </h3>

      <!-- Date -->
      <p class="mb-4 text-sm text-gray-600">
        {{ date }}
      </p>

      <!-- Price & CTA -->
      <div class="flex items-center justify-between">
        <span class="text-sm font-semibold text-gray-900">{{ price }}</span>
        <a
          :href="href"
          class="inline-flex items-center gap-1.5 rounded-full bg-gradient-to-r from-violet-500 to-violet-400 px-4 py-2 text-xs font-semibold text-white shadow-md transition-all hover:-translate-y-0.5 hover:shadow-lg"
        >
          Get Tickets
          <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
          </svg>
        </a>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  image: {
    type: String,
    default: ''
  },
  title: {
    type: String,
    required: true
  },
  date: {
    type: String,
    required: true
  },
  location: {
    type: String,
    required: true
  },
  price: {
    type: String,
    required: true
  },
  category: {
    type: String,
    required: true
  },
  href: {
    type: String,
    default: '#'
  }
})

// Generate gradient colors based on category for placeholder
const gradientColors = computed(() => {
  const gradients = {
    'Kompa Night': ['#8338ec', '#ff006e'],
    'Brunch': ['#ffbe0b', '#fb5607'],
    'Festival': ['#fb5607', '#ff006e'],
    'Fundraiser': ['#3a86ff', '#8338ec'],
    'Concert': ['#ff006e', '#8338ec'],
    'default': ['#8338ec', '#3a86ff']
  }
  return gradients[props.category] || gradients.default
})

// Category badge color
const categoryColor = computed(() => {
  const colors = {
    'Kompa Night': 'bg-violet-500',
    'Brunch': 'bg-amber-500',
    'Festival': 'bg-orange-500',
    'Fundraiser': 'bg-azure-500',
    'Concert': 'bg-rose-500'
  }
  return colors[props.category] || 'bg-violet-500'
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
