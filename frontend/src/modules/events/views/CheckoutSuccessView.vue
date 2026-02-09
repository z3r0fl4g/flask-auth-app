<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useAuth } from '@clerk/vue'
import { useAuthStore } from '@/stores/auth'
import QRCode from 'qrcode'
import api from '@/services/api'

const route = useRoute()
const { isLoaded } = useAuth()
const authStore = useAuthStore()

const loading = ref(true)
const error = ref(null)
const orderData = ref(null)
const qrCodes = ref({})

const attendeeName = computed(() => {
  return authStore.user?.fullname || authStore.user?.email?.split('@')[0] || 'Attendee'
})

const event = computed(() => orderData.value?.order?.event)

const eventImage = computed(() => {
  if (event.value?.cover_image) return event.value.cover_image
  return `https://picsum.photos/seed/${event.value?.id || 'default'}/600/200`
})

async function generateQRCodes(tickets) {
  for (const ticket of tickets) {
    try {
      qrCodes.value[ticket.ticket_code] = await QRCode.toDataURL(ticket.ticket_code, {
        width: 200,
        margin: 2,
        color: { dark: '#1f2937', light: '#ffffff' }
      })
    } catch (err) {
      console.error('Failed to generate QR code:', err)
    }
  }
}

async function fetchOrder() {
  const sessionId = route.query.session_id

  if (!sessionId) {
    error.value = 'Invalid checkout session'
    loading.value = false
    return
  }

  try {
    const response = await api.get(`/api/checkout/session/${sessionId}`)

    if (response.data.success) {
      orderData.value = response.data.data
      if (orderData.value.order?.tickets) {
        await generateQRCodes(orderData.value.order.tickets)
      }
    } else {
      error.value = response.data.message
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to load order details'
    console.error('Failed to fetch order:', err)
  } finally {
    loading.value = false
  }
}

function formatDate(isoString) {
  if (!isoString) return ''
  const date = new Date(isoString)
  return date.toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

function formatTime(isoString) {
  if (!isoString) return ''
  const date = new Date(isoString)
  return date.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit'
  })
}

function statusColor(status) {
  switch (status) {
    case 'valid': return 'bg-green-500'
    case 'used': return 'bg-gray-400'
    case 'cancelled': return 'bg-red-500'
    default: return 'bg-gray-400'
  }
}

// Wait for Clerk to load before fetching order data
watch(isLoaded, (loaded) => {
  if (loaded) {
    fetchOrder()
  }
}, { immediate: true })
</script>

<template>
  <div class="min-h-screen bg-gray-50 px-4 py-12 sm:py-16">
    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center min-h-[60vh]">
      <div class="text-center">
        <svg class="animate-spin w-12 h-12 text-violet-600 mx-auto mb-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
        <p class="text-gray-600">Loading your tickets...</p>
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="flex items-center justify-center min-h-[60vh]">
      <div class="text-center max-w-md">
        <div class="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-10 h-10 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-gray-900 mb-2">Something went wrong</h1>
        <p class="text-gray-600 mb-6">{{ error }}</p>
        <RouterLink to="/events" class="btn-primary">
          Browse Events
        </RouterLink>
      </div>
    </div>

    <!-- Success -->
    <div v-else-if="orderData" class="max-w-2xl mx-auto">
      <!-- Success Banner -->
      <div class="text-center mb-10">
        <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">You're going!</h1>
        <p class="text-gray-500">
          {{ orderData.order?.tickets?.length === 1
            ? '1 ticket confirmed'
            : `${orderData.order?.tickets?.length} tickets confirmed`
          }}
        </p>
      </div>

      <!-- Ticket Cards -->
      <div class="space-y-6 mb-8">
        <div
          v-for="ticket in orderData.order?.tickets"
          :key="ticket.id"
          class="bg-white rounded-2xl shadow-lg overflow-hidden"
        >
          <div class="flex flex-col sm:flex-row">
            <!-- Left: Cover Image + Event Details -->
            <div class="flex-1 min-w-0">
              <!-- Cover Image Banner -->
              <div class="h-28 sm:h-32 overflow-hidden">
                <img
                  :src="eventImage"
                  :alt="event?.title"
                  class="w-full h-full object-cover"
                />
              </div>

              <!-- Event Details -->
              <div class="p-5 sm:p-6">
                <!-- Event Name -->
                <h2 class="text-lg sm:text-xl font-bold text-gray-900 mb-0.5 truncate">
                  {{ event?.title }}
                </h2>
                <!-- Organizer -->
                <p class="text-sm text-gray-500 mb-1">
                  Organized by {{ event?.organizer?.fullname || 'Event Organizer' }}
                </p>
                <!-- Attendee -->
                <p class="text-sm text-gray-900 font-medium mb-4">
                  Attendee: {{ attendeeName }}
                </p>

                <!-- Detail Rows -->
                <div class="space-y-2.5">
                  <!-- Date & Time -->
                  <div class="flex items-center gap-2.5 text-sm">
                    <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <span class="text-gray-700">{{ formatDate(event?.start_date) }} &middot; {{ formatTime(event?.start_date) }}</span>
                  </div>

                  <!-- Entry / Access Type -->
                  <div class="flex items-center gap-2.5 text-sm">
                    <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                    </svg>
                    <span class="text-gray-700">{{ ticket.tier?.description || 'General Entry' }}</span>
                  </div>

                  <!-- Location -->
                  <div class="flex items-center gap-2.5 text-sm">
                    <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <span class="text-gray-700">
                      {{ event?.is_online
                        ? 'Online Event'
                        : [event?.venue_name, event?.city].filter(Boolean).join(', ') || 'Venue TBA'
                      }}
                    </span>
                  </div>

                  <!-- Ticket Type -->
                  <div class="flex items-center gap-2.5 text-sm">
                    <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" />
                    </svg>
                    <span class="text-gray-700">{{ ticket.tier?.name }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Perforated Divider -->
            <!-- Mobile: Horizontal -->
            <div class="relative sm:hidden">
              <div class="mx-4 border-t-2 border-dashed border-gray-200"></div>
              <div class="punch-hole-left"></div>
              <div class="punch-hole-right"></div>
            </div>
            <!-- Desktop: Vertical -->
            <div class="relative hidden sm:block">
              <div class="absolute inset-y-0 w-0 border-l-2 border-dashed border-gray-200"></div>
              <div class="punch-hole-top"></div>
              <div class="punch-hole-bottom"></div>
            </div>

            <!-- Right: QR Code Stub -->
            <div class="sm:w-48 p-6 sm:py-8 sm:px-6 flex flex-col items-center justify-center text-center">
              <img
                v-if="qrCodes[ticket.ticket_code]"
                :src="qrCodes[ticket.ticket_code]"
                alt="Ticket QR Code"
                class="w-32 h-32 sm:w-36 sm:h-36 mb-3"
              />
              <div v-else class="w-32 h-32 sm:w-36 sm:h-36 bg-gray-100 animate-pulse rounded-lg mb-3"></div>

              <p class="font-mono text-[11px] text-gray-900 font-semibold tracking-wide bg-gray-100 px-2.5 py-1 rounded-md mb-2">
                {{ ticket.ticket_code }}
              </p>
              <div class="flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full" :class="statusColor(ticket.status)"></span>
                <span class="text-xs text-gray-500 capitalize">{{ ticket.status }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Order Summary Footer -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 mb-6">
        <div class="flex items-center justify-between text-sm">
          <div class="flex items-center gap-3">
            <span class="text-gray-500">Order</span>
            <span class="font-mono font-semibold text-gray-900">{{ orderData.order?.order_number }}</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-gray-500">Total</span>
            <span class="font-bold text-gray-900">{{ orderData.order?.total_display }}</span>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row gap-3 mb-6">
        <RouterLink
          to="/my-tickets"
          class="flex-1 btn-primary text-center justify-center"
        >
          View My Tickets
        </RouterLink>
        <RouterLink
          to="/events"
          class="flex-1 btn-secondary text-center justify-center"
        >
          Browse More Events
        </RouterLink>
      </div>

      <!-- Confirmation Note -->
      <p class="text-center text-gray-400 text-sm">
        A confirmation email will be sent to your email address.
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Mobile: horizontal divider with left/right punch holes */
.punch-hole-left,
.punch-hole-right {
  position: absolute;
  top: 50%;
  width: 24px;
  height: 24px;
  border-radius: 9999px;
  background-color: rgb(249 250 251);
  transform: translateY(-50%);
}

.punch-hole-left {
  left: -12px;
}

.punch-hole-right {
  right: -12px;
}

/* Desktop: vertical divider with top/bottom punch holes */
.punch-hole-top,
.punch-hole-bottom {
  position: absolute;
  left: -12px;
  width: 24px;
  height: 24px;
  border-radius: 9999px;
  background-color: rgb(249 250 251);
  z-index: 1;
}

.punch-hole-top {
  top: -12px;
}

.punch-hole-bottom {
  bottom: -12px;
}
</style>
