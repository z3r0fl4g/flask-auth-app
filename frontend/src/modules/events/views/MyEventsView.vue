<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useEventsStore } from '@/stores/events'
import api from '@/services/api'

const eventsStore = useEventsStore()

const events = ref([])
const loading = ref(true)
const error = ref(null)
const filter = ref('all') // all, draft, published

onMounted(async () => {
  await fetchEvents()
})

async function fetchEvents() {
  loading.value = true
  error.value = null
  try {
    const response = await api.get('/api/events/my-events')
    events.value = response.data.data.events
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to load events'
    console.error('Failed to fetch events:', err)
  } finally {
    loading.value = false
  }
}

const filteredEvents = computed(() => {
  if (filter.value === 'all') return events.value
  return events.value.filter(e => e.status === filter.value)
})

async function publishEvent(event) {
  try {
    const response = await api.post(`/api/events/${event.id}/publish`)
    if (response.data.success) {
      event.status = 'published'
    } else {
      alert(response.data.message)
    }
  } catch (err) {
    alert(err.response?.data?.message || 'Failed to publish event')
  }
}

async function deleteEvent(event) {
  if (!confirm(`Are you sure you want to delete "${event.title}"?`)) return

  try {
    const response = await api.delete(`/api/events/${event.id}`)
    if (response.data.success) {
      events.value = events.value.filter(e => e.id !== event.id)
    } else {
      alert(response.data.message)
    }
  } catch (err) {
    alert(err.response?.data?.message || 'Failed to delete event')
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

function getEventImage(event) {
  if (event.cover_image) return event.cover_image
  return `https://picsum.photos/seed/${event.id}/400/200`
}

function getTicketsSold(event) {
  if (!event.ticket_tiers) return 0
  return event.ticket_tiers.reduce((sum, tier) => sum + (tier.quantity_sold || 0), 0)
}

function getTotalCapacity(event) {
  if (!event.ticket_tiers) return 0
  return event.ticket_tiers.reduce((sum, tier) => sum + tier.quantity_total, 0)
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b">
      <div class="max-w-7xl mx-auto px-4 py-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">My Events</h1>
            <p class="text-gray-600 mt-1">Manage your events and track sales</p>
          </div>
          <RouterLink to="/create-event" class="btn-primary">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Create Event
          </RouterLink>
        </div>
      </div>
    </div>

    <!-- Filter Tabs -->
    <div class="bg-white border-b sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex gap-1">
          <button
            @click="filter = 'all'"
            :class="[
              'px-4 py-3 text-sm font-medium border-b-2 transition-colors',
              filter === 'all'
                ? 'border-violet-600 text-violet-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            ]"
          >
            All ({{ events.length }})
          </button>
          <button
            @click="filter = 'draft'"
            :class="[
              'px-4 py-3 text-sm font-medium border-b-2 transition-colors',
              filter === 'draft'
                ? 'border-violet-600 text-violet-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            ]"
          >
            Drafts ({{ events.filter(e => e.status === 'draft').length }})
          </button>
          <button
            @click="filter = 'published'"
            :class="[
              'px-4 py-3 text-sm font-medium border-b-2 transition-colors',
              filter === 'published'
                ? 'border-violet-600 text-violet-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            ]"
          >
            Published ({{ events.filter(e => e.status === 'published').length }})
          </button>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="max-w-7xl mx-auto px-4 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="space-y-4">
        <div
          v-for="i in 3"
          :key="i"
          class="bg-white rounded-2xl p-6 shadow-sm animate-pulse"
        >
          <div class="flex gap-6">
            <div class="w-48 h-32 bg-gray-200 rounded-xl"></div>
            <div class="flex-1 space-y-3">
              <div class="h-6 bg-gray-200 rounded w-1/2"></div>
              <div class="h-4 bg-gray-200 rounded w-1/3"></div>
              <div class="h-4 bg-gray-200 rounded w-1/4"></div>
            </div>
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
        <button @click="fetchEvents" class="btn-primary">Try Again</button>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredEvents.length === 0" class="text-center py-16">
        <div class="w-20 h-20 bg-violet-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-10 h-10 text-violet-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">
          {{ filter === 'all' ? 'No events yet' : `No ${filter} events` }}
        </h2>
        <p class="text-gray-600 mb-6">
          {{ filter === 'all'
            ? 'Create your first event to start selling tickets!'
            : `You don't have any ${filter} events.`
          }}
        </p>
        <RouterLink v-if="filter === 'all'" to="/create-event" class="btn-primary">
          Create Event
        </RouterLink>
      </div>

      <!-- Events List -->
      <div v-else class="space-y-4">
        <div
          v-for="event in filteredEvents"
          :key="event.id"
          class="bg-white rounded-2xl shadow-sm overflow-hidden hover:shadow-md transition-shadow"
        >
          <div class="flex flex-col sm:flex-row">
            <!-- Event Image -->
            <div class="sm:w-48 sm:h-auto h-32 flex-shrink-0">
              <img
                :src="getEventImage(event)"
                :alt="event.title"
                class="w-full h-full object-cover"
              />
            </div>

            <!-- Event Info -->
            <div class="flex-1 p-6">
              <div class="flex items-start justify-between gap-4">
                <div class="flex-1">
                  <!-- Status Badge -->
                  <div class="flex items-center gap-2 mb-2">
                    <span
                      :class="[
                        'px-2 py-0.5 text-xs font-bold rounded-full uppercase',
                        event.status === 'published'
                          ? 'bg-green-100 text-green-700'
                          : event.status === 'draft'
                          ? 'bg-amber-100 text-amber-700'
                          : 'bg-gray-100 text-gray-700'
                      ]"
                    >
                      {{ event.status }}
                    </span>
                    <span class="text-sm text-gray-500">
                      {{ eventsStore.getCategoryLabel(event.category) }}
                    </span>
                  </div>

                  <!-- Title -->
                  <h3 class="text-lg font-bold text-gray-900 mb-1">{{ event.title }}</h3>

                  <!-- Date & Location -->
                  <div class="flex flex-wrap items-center gap-4 text-sm text-gray-600">
                    <div class="flex items-center gap-1.5">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      {{ formatDate(event.start_date) }}
                    </div>
                    <div class="flex items-center gap-1.5">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      </svg>
                      {{ event.is_online ? 'Online' : (event.venue_name || event.city) }}
                    </div>
                  </div>

                  <!-- Ticket Stats -->
                  <div v-if="event.status === 'published'" class="mt-3">
                    <div class="flex items-center gap-2">
                      <div class="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                        <div
                          class="h-full bg-violet-600 rounded-full"
                          :style="{ width: `${(getTicketsSold(event) / getTotalCapacity(event)) * 100}%` }"
                        ></div>
                      </div>
                      <span class="text-sm font-medium text-gray-600">
                        {{ getTicketsSold(event) }}/{{ getTotalCapacity(event) }} sold
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Actions -->
                <div class="flex items-center gap-2">
                  <RouterLink
                    :to="{ name: 'event-detail', params: { slug: event.slug } }"
                    class="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition"
                    title="View"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </RouterLink>

                  <button
                    v-if="event.status === 'draft'"
                    @click="publishEvent(event)"
                    class="px-3 py-1.5 bg-green-600 text-white text-sm font-medium rounded-lg hover:bg-green-700 transition"
                  >
                    Publish
                  </button>

                  <button
                    @click="deleteEvent(event)"
                    class="p-2 text-red-500 hover:text-red-700 hover:bg-red-50 rounded-lg transition"
                    title="Delete"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
