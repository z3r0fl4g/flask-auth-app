<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import api from '@/services/api'
import TicketCard from '../components/TicketCard.vue'

const tickets = ref([])
const loading = ref(true)
const error = ref(null)
const filter = ref('upcoming') // upcoming, past, all

onMounted(async () => {
  await fetchTickets()
})

async function fetchTickets() {
  loading.value = true
  error.value = null
  try {
    const response = await api.get('/api/tickets/')
    tickets.value = response.data.data.tickets
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to load tickets'
    console.error('Failed to fetch tickets:', err)
  } finally {
    loading.value = false
  }
}

const filteredTickets = computed(() => {
  const now = new Date()

  return tickets.value.filter(ticket => {
    if (filter.value === 'all') return true

    const eventDate = new Date(ticket.event?.start_date)

    if (filter.value === 'upcoming') {
      return eventDate >= now && ticket.status === 'valid'
    }

    if (filter.value === 'past') {
      return eventDate < now || ticket.status !== 'valid'
    }

    return true
  })
})

const upcomingCount = computed(() => {
  const now = new Date()
  return tickets.value.filter(t =>
    new Date(t.event?.start_date) >= now && t.status === 'valid'
  ).length
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b">
      <div class="max-w-7xl mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">My Tickets</h1>
        <p class="text-gray-600">
          {{ upcomingCount }} upcoming event{{ upcomingCount !== 1 ? 's' : '' }}
        </p>
      </div>
    </div>

    <!-- Filter Tabs -->
    <div class="bg-white border-b sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex gap-1">
          <button
            @click="filter = 'upcoming'"
            :class="[
              'px-4 py-3 text-sm font-medium border-b-2 transition-colors',
              filter === 'upcoming'
                ? 'border-violet-600 text-violet-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            ]"
          >
            Upcoming
          </button>
          <button
            @click="filter = 'past'"
            :class="[
              'px-4 py-3 text-sm font-medium border-b-2 transition-colors',
              filter === 'past'
                ? 'border-violet-600 text-violet-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            ]"
          >
            Past
          </button>
          <button
            @click="filter = 'all'"
            :class="[
              'px-4 py-3 text-sm font-medium border-b-2 transition-colors',
              filter === 'all'
                ? 'border-violet-600 text-violet-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            ]"
          >
            All
          </button>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="max-w-7xl mx-auto px-4 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="i in 3"
          :key="i"
          class="bg-white rounded-2xl overflow-hidden shadow-sm animate-pulse"
        >
          <div class="h-32 bg-gray-200"></div>
          <div class="p-5 space-y-4">
            <div class="h-4 bg-gray-200 rounded w-1/2"></div>
            <div class="h-40 bg-gray-200 rounded"></div>
            <div class="h-4 bg-gray-200 rounded w-2/3"></div>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-16">
        <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">Something went wrong</h2>
        <p class="text-gray-600 mb-6">{{ error }}</p>
        <button @click="fetchTickets" class="btn-primary">
          Try Again
        </button>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredTickets.length === 0" class="text-center py-16">
        <div class="w-20 h-20 bg-violet-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-10 h-10 text-violet-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" />
          </svg>
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">
          {{ filter === 'upcoming' ? 'No upcoming tickets' : 'No tickets found' }}
        </h2>
        <p class="text-gray-600 mb-6">
          {{ filter === 'upcoming'
            ? "You don't have any upcoming events. Browse events to find your next experience!"
            : "You haven't purchased any tickets yet."
          }}
        </p>
        <RouterLink to="/events" class="btn-primary">
          Browse Events
        </RouterLink>
      </div>

      <!-- Tickets Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <TicketCard
          v-for="ticket in filteredTickets"
          :key="ticket.id"
          :ticket="ticket"
        />
      </div>
    </div>
  </div>
</template>
