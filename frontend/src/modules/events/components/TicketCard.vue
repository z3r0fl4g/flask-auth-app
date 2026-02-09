<script setup>
import { ref, computed, onMounted } from 'vue'
import QRCode from 'qrcode'

const props = defineProps({
  ticket: {
    type: Object,
    required: true
  }
})

const qrDataUrl = ref('')

onMounted(async () => {
  try {
    qrDataUrl.value = await QRCode.toDataURL(props.ticket.ticket_code, {
      width: 200,
      margin: 2,
      color: {
        dark: '#1f2937',
        light: '#ffffff'
      }
    })
  } catch (err) {
    console.error('Failed to generate QR code:', err)
  }
})

const formattedDate = computed(() => {
  if (!props.ticket.event?.start_date) return ''
  const date = new Date(props.ticket.event.start_date)
  return date.toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric'
  })
})

const formattedTime = computed(() => {
  if (!props.ticket.event?.start_date) return ''
  const date = new Date(props.ticket.event.start_date)
  return date.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit'
  })
})

const statusColor = computed(() => {
  switch (props.ticket.status) {
    case 'valid':
      return 'bg-green-100 text-green-700'
    case 'used':
      return 'bg-gray-100 text-gray-700'
    case 'cancelled':
      return 'bg-red-100 text-red-700'
    default:
      return 'bg-gray-100 text-gray-700'
  }
})

const eventImage = computed(() => {
  if (props.ticket.event?.cover_image) return props.ticket.event.cover_image
  const seed = props.ticket.event?.id || 'default'
  return `https://picsum.photos/seed/${seed}/400/200`
})
</script>

<template>
  <div class="bg-white rounded-2xl shadow-lg overflow-hidden">
    <!-- Event Image Header -->
    <div class="relative h-32">
      <img
        :src="eventImage"
        :alt="ticket.event?.title"
        class="w-full h-full object-cover"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
      <div class="absolute bottom-3 left-4 right-4">
        <h3 class="font-bold text-white text-lg line-clamp-1">
          {{ ticket.event?.title }}
        </h3>
      </div>
      <!-- Status Badge -->
      <div class="absolute top-3 right-3">
        <span
          :class="[
            'px-3 py-1 rounded-full text-xs font-bold uppercase',
            statusColor
          ]"
        >
          {{ ticket.status }}
        </span>
      </div>
    </div>

    <!-- Ticket Content -->
    <div class="p-5">
      <!-- Date & Location -->
      <div class="flex items-center gap-4 text-sm text-gray-600 mb-4">
        <div class="flex items-center gap-1.5">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span>{{ formattedDate }}</span>
        </div>
        <div class="flex items-center gap-1.5">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>{{ formattedTime }}</span>
        </div>
      </div>

      <!-- Ticket Tier -->
      <div class="mb-4 p-3 bg-violet-50 rounded-xl">
        <p class="text-sm text-violet-600 font-medium">{{ ticket.tier?.name }}</p>
      </div>

      <!-- QR Code -->
      <div class="flex flex-col items-center py-4 border-t border-dashed border-gray-200">
        <img
          v-if="qrDataUrl"
          :src="qrDataUrl"
          alt="Ticket QR Code"
          class="w-40 h-40 mb-3"
        />
        <div v-else class="w-40 h-40 bg-gray-100 animate-pulse rounded-lg mb-3"></div>
        <p class="font-mono text-sm text-gray-600 bg-gray-100 px-3 py-1 rounded-lg">
          {{ ticket.ticket_code }}
        </p>
      </div>

      <!-- Location -->
      <div class="mt-4 pt-4 border-t border-gray-100">
        <div class="flex items-center gap-2 text-sm text-gray-600">
          <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span class="line-clamp-1">
            {{ ticket.event?.is_online ? 'Online Event' : (ticket.event?.venue_name || ticket.event?.city) }}
          </span>
        </div>
      </div>

      <!-- Checked In Time -->
      <div v-if="ticket.checked_in_at" class="mt-3 text-sm text-gray-500">
        Checked in: {{ new Date(ticket.checked_in_at).toLocaleString() }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
