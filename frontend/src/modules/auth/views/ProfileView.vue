<template>
  <div class="py-12">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Welcome Header -->
      <div class="flex items-center gap-5 mb-10">
        <img
          v-if="user?.profile_pic"
          :src="user.profile_pic"
          alt="Profile picture"
          class="rounded-full w-16 h-16 object-cover border-2 border-violet-200"
        />
        <div
          v-else
          class="w-16 h-16 rounded-full bg-violet-100 flex items-center justify-center text-violet-600 text-2xl font-bold"
        >
          {{ userInitial }}
        </div>
        <div>
          <h1 class="text-2xl font-bold text-headline">Hey {{ displayName }}</h1>
          <p class="text-body mt-1">Here's what's coming up for you.</p>
        </div>
      </div>

      <!-- My Upcoming Tickets -->
      <section class="mb-8">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold text-headline">My Tickets</h2>
          <router-link to="/my-tickets" class="text-sm text-violet-600 hover:text-violet-700 font-medium">
            View all →
          </router-link>
        </div>

        <div v-if="loadingTickets" class="card p-10 text-center">
          <div class="text-gray-500">Loading tickets...</div>
        </div>

        <div v-else-if="tickets.length === 0" class="card p-10">
          <div class="text-center py-6">
            <div class="w-16 h-16 bg-violet-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-violet-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" />
              </svg>
            </div>
            <h3 class="text-lg font-medium text-headline mb-2">No tickets yet</h3>
            <p class="text-muted text-sm mb-6 max-w-sm mx-auto">
              When you purchase tickets, they'll appear here.
            </p>
            <router-link to="/events" class="btn-primary">
              Browse Events
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </router-link>
          </div>
        </div>

        <div v-else class="grid gap-4">
          <div v-for="ticket in tickets.slice(0, 3)" :key="ticket.id" class="card p-4">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <h3 class="font-semibold text-headline">{{ ticket.event?.title }}</h3>
                <p class="text-sm text-muted mt-1">{{ ticket.tier?.name }} • {{ ticket.ticket_code }}</p>
              </div>
              <router-link to="/my-tickets" class="text-violet-600 hover:text-violet-700 text-sm font-medium">
                View →
              </router-link>
            </div>
          </div>
        </div>
      </section>

      <!-- My Events (Organizer) -->
      <section class="mb-8">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold text-headline">My Events</h2>
          <router-link to="/my-events" class="text-sm text-violet-600 hover:text-violet-700 font-medium">
            View all →
          </router-link>
        </div>

        <div v-if="loadingEvents" class="card p-10 text-center">
          <div class="text-gray-500">Loading events...</div>
        </div>

        <div v-else-if="myEvents.length === 0" class="card p-8">
          <div class="text-center py-4">
            <div class="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </div>
            <h3 class="text-sm font-medium text-headline mb-1">No events created</h3>
            <p class="text-muted text-xs mb-4">Start organizing your own events!</p>
            <router-link to="/create-event" class="btn-primary text-sm">
              Create Event
            </router-link>
          </div>
        </div>

        <div v-else class="grid gap-4">
          <div v-for="event in myEvents.slice(0, 3)" :key="event.id" class="card p-4">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <div class="flex items-center gap-2">
                  <h3 class="font-semibold text-headline">{{ event.title }}</h3>
                  <span
                    class="text-xs px-2 py-0.5 rounded-full"
                    :class="event.status === 'published' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'"
                  >
                    {{ event.status }}
                  </span>
                </div>
                <p class="text-sm text-muted mt-1">{{ event.category }} • {{ new Date(event.start_date).toLocaleDateString() }}</p>
              </div>
              <router-link to="/my-events" class="text-violet-600 hover:text-violet-700 text-sm font-medium">
                Manage →
              </router-link>
            </div>
          </div>
        </div>
      </section>

      <!-- Account Strip -->
      <div class="card px-6 py-4">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div class="flex items-center gap-4 text-sm">
            <span class="text-body">{{ user?.email }}</span>
          </div>
          <div class="flex items-center gap-4 text-sm">
            <button
              @click="logout"
              class="text-gray-500 hover:text-gray-700"
            >
              Log out
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import api from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.user)
const tickets = ref([])
const myEvents = ref([])
const loadingTickets = ref(false)
const loadingEvents = ref(false)

const userInitial = computed(() => {
  if (user.value?.email) {
    return user.value.email[0].toUpperCase()
  }
  return 'U'
})

const displayName = computed(() => {
  if (user.value?.fullname) return user.value.fullname
  if (user.value?.username) return user.value.username
  if (user.value?.email) return user.value.email.split('@')[0]
  return 'there'
})

async function fetchTickets() {
  loadingTickets.value = true
  try {
    const response = await api.get('/api/tickets/')
    tickets.value = response.data.data.tickets || []
  } catch (error) {
    console.error('Failed to fetch tickets:', error)
  } finally {
    loadingTickets.value = false
  }
}

async function fetchMyEvents() {
  loadingEvents.value = true
  try {
    const response = await api.get('/api/events/my-events')
    myEvents.value = response.data.data.events || []
  } catch (error) {
    console.error('Failed to fetch my events:', error)
  } finally {
    loadingEvents.value = false
  }
}

async function logout() {
  await authStore.logout()
  router.push('/login')
}

onMounted(async () => {
  if (!authStore.user) {
    await authStore.checkSession()
  }
  fetchTickets()
  fetchMyEvents()
})
</script>
