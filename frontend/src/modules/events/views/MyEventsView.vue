<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useEventsStore } from '@/stores/events'
import { toast } from 'vue-sonner'
import api from '@/services/api'
import StatCard from '@/components/ui/StatCard.vue'
import Badge from '@/components/ui/Badge.vue'
import Modal from '@/components/ui/Modal.vue'
import { CalendarDays, TicketCheck, DollarSign, Plus, Eye, Trash2, Send } from 'lucide-vue-next'

const eventsStore = useEventsStore()

const events = ref([])
const loading = ref(true)
const error = ref(null)
const filter = ref('all') // all, draft, published
const search = ref('')

// Delete confirmation modal
const showDeleteModal = ref(false)
const eventToDelete = ref(null)
const deleting = ref(false)

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
  let result = events.value
  if (filter.value !== 'all') {
    result = result.filter(e => e.status === filter.value)
  }
  if (search.value.trim()) {
    const q = search.value.toLowerCase()
    result = result.filter(e => e.title.toLowerCase().includes(q))
  }
  return result
})

// Stats
const totalEvents = computed(() => events.value.length)
const publishedCount = computed(() => events.value.filter(e => e.status === 'published').length)
const totalTicketsSold = computed(() =>
  events.value.reduce((sum, e) => sum + getTicketsSold(e), 0)
)

async function publishEvent(event) {
  try {
    const response = await api.post(`/api/events/${event.id}/publish`)
    if (response.data.success) {
      event.status = 'published'
      toast.success(`"${event.title}" is now live!`)
    } else {
      toast.error(response.data.message)
    }
  } catch (err) {
    toast.error(err.response?.data?.message || 'Failed to publish event')
  }
}

function confirmDelete(event) {
  eventToDelete.value = event
  showDeleteModal.value = true
}

async function handleDelete() {
  if (!eventToDelete.value) return
  deleting.value = true
  const deletedTitle = eventToDelete.value.title
  try {
    const response = await api.delete(`/api/events/${eventToDelete.value.id}`)
    if (response.data.success) {
      events.value = events.value.filter(e => e.id !== eventToDelete.value.id)
      toast.success(`"${deletedTitle}" has been deleted.`)
      showDeleteModal.value = false
      eventToDelete.value = null
    } else {
      toast.error(response.data.message)
    }
  } catch (err) {
    toast.error(err.response?.data?.message || 'Failed to delete event')
  } finally {
    deleting.value = false
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

function getBadgeVariant(status) {
  const map = { published: 'published', draft: 'draft', cancelled: 'error' }
  return map[status] || 'default'
}
</script>

<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">My Events</h1>
        <p class="text-sm text-gray-500 mt-1">Manage your events and track sales</p>
      </div>
      <RouterLink to="/create-event" class="btn-primary">
        <Plus :size="18" class="mr-1.5" />
        Create Event
      </RouterLink>
    </div>

    <!-- Stat Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <StatCard
        label="Total Events"
        :value="totalEvents"
        :icon="CalendarDays"
        variant="violet"
      />
      <StatCard
        label="Published"
        :value="publishedCount"
        :icon="Send"
        variant="green"
      />
      <StatCard
        label="Tickets Sold"
        :value="totalTicketsSold"
        :icon="TicketCheck"
        variant="blue"
      />
    </div>

    <!-- Filter & Search Bar -->
    <div class="bg-white rounded-xl border border-gray-200 p-4">
      <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4">
        <!-- Filter Tabs -->
        <div class="flex gap-1 bg-gray-100 rounded-lg p-1">
          <button
            v-for="tab in [
              { key: 'all', label: 'All' },
              { key: 'draft', label: 'Drafts' },
              { key: 'published', label: 'Published' }
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

        <!-- Search -->
        <div class="relative flex-1 w-full sm:w-auto">
          <input
            v-model="search"
            type="text"
            placeholder="Search events..."
            class="w-full pl-9 pr-4 py-2 text-sm border border-gray-200 rounded-lg focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 outline-hidden transition"
          />
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="space-y-4">
      <div
        v-for="i in 3"
        :key="i"
        class="bg-white rounded-xl border border-gray-200 p-5 animate-pulse"
      >
        <div class="flex gap-5">
          <div class="w-40 h-28 bg-gray-200 rounded-lg shrink-0"></div>
          <div class="flex-1 space-y-3">
            <div class="h-5 bg-gray-200 rounded w-1/3"></div>
            <div class="h-4 bg-gray-200 rounded w-1/2"></div>
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
    <div v-else-if="filteredEvents.length === 0" class="bg-white rounded-xl border border-gray-200 text-center py-16">
      <div class="w-20 h-20 bg-violet-100 rounded-full flex items-center justify-center mx-auto mb-6">
        <CalendarDays :size="40" class="text-violet-600" />
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
        <Plus :size="18" class="mr-1.5" />
        Create Event
      </RouterLink>
    </div>

    <!-- Events List -->
    <div v-else class="space-y-3">
      <div
        v-for="event in filteredEvents"
        :key="event.id"
        class="bg-white rounded-xl border border-gray-200 overflow-hidden hover:border-gray-300 transition-colors"
      >
        <div class="flex flex-col sm:flex-row">
          <!-- Event Image -->
          <div class="sm:w-44 h-32 sm:h-auto shrink-0">
            <img
              :src="getEventImage(event)"
              :alt="event.title"
              class="w-full h-full object-cover"
            />
          </div>

          <!-- Event Info -->
          <div class="flex-1 p-5">
            <div class="flex items-start justify-between gap-4">
              <div class="flex-1 min-w-0">
                <!-- Status Badge + Category -->
                <div class="flex items-center gap-2 mb-2">
                  <Badge :variant="getBadgeVariant(event.status)">
                    {{ event.status }}
                  </Badge>
                  <span class="text-xs text-gray-500">
                    {{ eventsStore.getCategoryLabel(event.category) }}
                  </span>
                </div>

                <!-- Title -->
                <h3 class="text-base font-bold text-gray-900 mb-1.5 truncate">{{ event.title }}</h3>

                <!-- Date & Location -->
                <div class="flex flex-wrap items-center gap-3 text-sm text-gray-500">
                  <div class="flex items-center gap-1">
                    <CalendarDays :size="14" />
                    {{ formatDate(event.start_date) }}
                  </div>
                  <div class="flex items-center gap-1">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    </svg>
                    {{ event.is_online ? 'Online' : (event.venue_name || event.city) }}
                  </div>
                </div>

                <!-- Ticket Progress -->
                <div v-if="event.status === 'published' && getTotalCapacity(event) > 0" class="mt-3">
                  <div class="flex items-center gap-2">
                    <div class="flex-1 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                      <div
                        class="h-full bg-violet-500 rounded-full transition-all"
                        :style="{ width: `${Math.min((getTicketsSold(event) / getTotalCapacity(event)) * 100, 100)}%` }"
                      ></div>
                    </div>
                    <span class="text-xs font-medium text-gray-500 whitespace-nowrap">
                      {{ getTicketsSold(event) }}/{{ getTotalCapacity(event) }} sold
                    </span>
                  </div>
                </div>
              </div>

              <!-- Actions -->
              <div class="flex items-center gap-1">
                <RouterLink
                  :to="{ name: 'event-detail', params: { slug: event.slug } }"
                  class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition"
                  title="View"
                >
                  <Eye :size="18" />
                </RouterLink>

                <button
                  v-if="event.status === 'draft'"
                  @click="publishEvent(event)"
                  class="px-3 py-1.5 bg-green-600 text-white text-xs font-medium rounded-lg hover:bg-green-700 transition"
                >
                  Publish
                </button>

                <button
                  @click="confirmDelete(event)"
                  class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition"
                  title="Delete"
                >
                  <Trash2 :size="18" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <Modal :show="showDeleteModal" @close="showDeleteModal = false" size="sm">
      <template #header>Delete Event</template>
      <template #body>
        <p class="text-gray-600">
          Are you sure you want to delete <strong>"{{ eventToDelete?.title }}"</strong>?
          This action cannot be undone.
        </p>
      </template>
      <template #footer>
        <button
          @click="showDeleteModal = false"
          class="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 transition"
        >
          Cancel
        </button>
        <button
          @click="handleDelete"
          :disabled="deleting"
          class="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 transition disabled:opacity-50"
        >
          {{ deleting ? 'Deleting...' : 'Delete' }}
        </button>
      </template>
    </Modal>
  </div>
</template>
