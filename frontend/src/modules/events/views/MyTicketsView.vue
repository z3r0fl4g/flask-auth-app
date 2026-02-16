<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import api from '@/services/api'
import Badge from '@/components/ui/Badge.vue'
import TicketCard from '../components/TicketCard.vue'
import { TicketCheck } from 'lucide-vue-next'

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
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">My Tickets</h1>
        <p class="text-sm text-gray-500 mt-1">
          {{ upcomingCount }} upcoming event{{ upcomingCount !== 1 ? 's' : '' }}
        </p>
      </div>
      <RouterLink to="/events" class="btn-primary">
        Browse Events
      </RouterLink>
    </div>

    <!-- Filter Tabs -->
    <div class="bg-white rounded-xl border border-gray-200 p-4">
      <div class="flex gap-1 bg-gray-100 rounded-lg p-1 w-fit">
        <button
          v-for="tab in [
            { key: 'upcoming', label: 'Upcoming' },
            { key: 'past', label: 'Past' },
            { key: 'all', label: 'All' }
          ]"
          :key="tab.key"
          @click="filter = tab.key"
          :class="[
            'px-3 py-1.5 text-sm font-medium rounded-md transition-colors',
            filter === tab.key
              ? 'bg-white text-gray-900 shadow-sm'
              : 'text-gray-500 hover:text-gray-700'
          ]"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="i in 3"
        :key="i"
        class="bg-white rounded-xl border border-gray-200 overflow-hidden animate-pulse"
      >
        <div class="h-28 bg-gray-200"></div>
        <div class="p-4 space-y-3">
          <div class="h-4 bg-gray-200 rounded w-1/2"></div>
          <div class="h-32 bg-gray-200 rounded"></div>
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
      <button @click="fetchTickets" class="btn-primary">Try Again</button>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredTickets.length === 0" class="bg-white rounded-xl border border-gray-200 text-center py-16">
      <div class="w-20 h-20 bg-violet-100 rounded-full flex items-center justify-center mx-auto mb-6">
        <TicketCheck :size="40" class="text-violet-600" />
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
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <TicketCard
        v-for="ticket in filteredTickets"
        :key="ticket.id"
        :ticket="ticket"
      />
    </div>
  </div>
</template>
