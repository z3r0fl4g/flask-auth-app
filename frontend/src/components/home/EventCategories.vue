<template>
  <section class="py-16 lg:py-20">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section Header -->
      <div class="text-center mb-12">
        <p class="text-xs uppercase tracking-[0.4em] text-gray-400 mb-3">Browse by Vibe</p>
        <h2 class="text-3xl font-semibold text-gray-900">Find Your Kind of Event</h2>
      </div>

      <!-- Category Grid -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
        <a
          v-for="category in categories"
          :key="category.name"
          :href="category.href"
          class="group relative overflow-hidden rounded-3xl aspect-[4/5] transition-transform duration-300 hover:scale-105"
        >
          <!-- Gradient Background -->
          <div
            class="absolute inset-0 transition-opacity duration-300"
            :style="{ background: `linear-gradient(135deg, ${category.gradient[0]}, ${category.gradient[1]})` }"
          ></div>

          <!-- Overlay -->
          <div class="absolute inset-0 bg-black/20 group-hover:bg-black/30 transition-colors"></div>

          <!-- Content -->
          <div class="absolute inset-0 flex flex-col items-center justify-center text-white p-4">
            <span class="text-4xl mb-3">{{ category.emoji }}</span>
            <h3 class="text-lg font-semibold text-center">{{ category.name }}</h3>
            <p class="text-xs text-white/80 mt-1">{{ category.count }} events</p>
          </div>

          <!-- Hover Arrow -->
          <div class="absolute bottom-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
            <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </div>
        </a>
      </div>
    </div>
  </section>
</template>

<script setup>
const categories = [
  {
    name: 'Kompa Nights',
    emoji: '🎵',
    count: '2,400+',
    gradient: ['#8338ec', '#ff006e'],
    href: '#'
  },
  {
    name: 'Rara & Festivals',
    emoji: '🎭',
    count: '850+',
    gradient: ['#fb5607', '#ffbe0b'],
    href: '#'
  },
  {
    name: 'Brunch & Day',
    emoji: '☀️',
    count: '1,200+',
    gradient: ['#ffbe0b', '#ff006e'],
    href: '#'
  },
  {
    name: 'Fundraisers',
    emoji: '❤️',
    count: '620+',
    gradient: ['#3a86ff', '#8338ec'],
    href: '#'
  },
  {
    name: 'Concerts',
    emoji: '🎤',
    count: '980+',
    gradient: ['#ff006e', '#8338ec'],
    href: '#'
  }
]
</script>
