<template>
  <section class="py-16 lg:py-20">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section Header -->
      <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-10">
        <div>
          <p class="text-xs uppercase tracking-[0.4em] text-gray-400 mb-2">This Weekend</p>
          <h2 class="text-3xl font-semibold text-gray-900">Events Selling Fast</h2>
        </div>
        <a
          href="#"
          class="inline-flex items-center gap-2 text-sm font-semibold text-violet-500 hover:text-violet-600 transition-colors"
        >
          View all events
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
          </svg>
        </a>
      </div>

      <!-- Events Carousel/Grid -->
      <div class="relative">
        <!-- Desktop Grid -->
        <div class="hidden lg:grid lg:grid-cols-4 gap-6">
          <EventCard
            v-for="event in events"
            :key="event.id"
            v-bind="event"
          />
        </div>

        <!-- Mobile/Tablet Horizontal Scroll -->
        <div class="lg:hidden overflow-x-auto pb-4 -mx-4 px-4 scrollbar-hide">
          <div class="flex gap-4" style="width: max-content;">
            <div v-for="event in events" :key="event.id" class="w-72 flex-shrink-0">
              <EventCard v-bind="event" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import EventCard from './EventCard.vue'

// Placeholder events data per the plan
const events = [
  {
    id: 1,
    title: 'Kompa Classics & New Heat',
    date: 'Sat, Feb 15 • 9PM',
    location: 'Brooklyn, NY',
    price: 'From $25',
    category: 'Kompa Night',
    image: '',
    href: '#'
  },
  {
    id: 2,
    title: 'Ayiti Brunch & Bottomless Beats',
    date: 'Sun, Feb 16 • 11:30AM',
    location: 'Miami, FL',
    price: 'From $45',
    category: 'Brunch',
    image: '',
    href: '#'
  },
  {
    id: 3,
    title: 'Rara Street Energy Takeover',
    date: 'Sat, Feb 22 • 2PM',
    location: 'Boston, MA',
    price: 'Free Entry',
    category: 'Festival',
    image: '',
    href: '#'
  },
  {
    id: 4,
    title: 'Diaspora Impact Gala 2025',
    date: 'Sat, Mar 1 • 6:30PM',
    location: 'Providence, RI',
    price: 'From $75',
    category: 'Fundraiser',
    image: '',
    href: '#'
  },
  {
    id: 5,
    title: 'Haitian Flag Day Festival',
    date: 'Sun, May 18 • 12PM',
    location: 'New York, NY',
    price: 'From $15',
    category: 'Festival',
    image: '',
    href: '#'
  },
  {
    id: 6,
    title: 'Kanaval Block Party',
    date: 'Fri, Feb 28 • 8PM',
    location: 'Montreal, CA',
    price: 'From $30',
    category: 'Concert',
    image: '',
    href: '#'
  }
]
</script>

<style scoped>
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>
