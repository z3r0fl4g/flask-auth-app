<script setup>
import { ref } from 'vue'
import api from '@/services/api'

const ticketCode = ref('')
const loading = ref(false)
const result = ref(null)
const history = ref([])

async function validateTicket() {
  if (!ticketCode.value.trim()) return

  loading.value = true
  result.value = null

  try {
    const response = await api.get(`/api/checkin/validate/${ticketCode.value.trim()}`)
    result.value = {
      ...response.data,
      code: ticketCode.value.trim()
    }
  } catch (err) {
    result.value = {
      valid: false,
      message: err.response?.data?.message || 'Failed to validate ticket',
      code: ticketCode.value.trim()
    }
  } finally {
    loading.value = false
  }
}

async function checkIn() {
  if (!result.value?.valid) return

  loading.value = true

  try {
    const response = await api.post('/api/checkin/', {
      ticket_code: result.value.code
    })

    if (response.data.valid) {
      // Add to history
      history.value.unshift({
        ...response.data.ticket,
        timestamp: new Date()
      })

      // Show success
      result.value = {
        valid: true,
        checked_in: true,
        message: 'Check-in successful!',
        ticket: response.data.ticket
      }

      // Clear input after success
      ticketCode.value = ''
    } else {
      result.value = {
        valid: false,
        message: response.data.message
      }
    }
  } catch (err) {
    result.value = {
      valid: false,
      message: err.response?.data?.message || 'Check-in failed'
    }
  } finally {
    loading.value = false
  }
}

function reset() {
  ticketCode.value = ''
  result.value = null
}

function formatTime(date) {
  return new Date(date).toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit'
  })
}
</script>

<template>
  <div class="min-h-screen bg-gray-900">
    <!-- Header -->
    <div class="bg-gray-800 border-b border-gray-700">
      <div class="max-w-2xl mx-auto px-4 py-6">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-white">Check-In</h1>
            <p class="text-gray-400 text-sm">Scan or enter ticket code</p>
          </div>
          <router-link
            to="/my-events"
            class="text-gray-400 hover:text-white transition"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-2xl mx-auto px-4 py-8">
      <!-- Input Section -->
      <div class="bg-gray-800 rounded-2xl p-6 mb-6">
        <div class="flex gap-3">
          <input
            v-model="ticketCode"
            type="text"
            placeholder="Enter ticket code (e.g., TIK-XXXXXXXXXX)"
            class="flex-1 bg-gray-700 border-0 rounded-xl px-4 py-3 text-white placeholder-gray-400 focus:ring-2 focus:ring-violet-500 font-mono"
            @keyup.enter="validateTicket"
            :disabled="loading"
          />
          <button
            @click="validateTicket"
            :disabled="loading || !ticketCode.trim()"
            class="px-6 py-3 bg-violet-600 text-white font-medium rounded-xl hover:bg-violet-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">...</span>
            <span v-else>Check</span>
          </button>
        </div>
      </div>

      <!-- Result Section -->
      <div v-if="result" class="mb-6">
        <!-- Valid Ticket (Ready to Check In) -->
        <div
          v-if="result.valid && !result.checked_in"
          class="bg-green-900/50 border border-green-500 rounded-2xl p-6"
        >
          <div class="flex items-start gap-4">
            <div class="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center flex-shrink-0">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div class="flex-1">
              <h3 class="text-xl font-bold text-green-400 mb-2">Valid Ticket</h3>
              <div class="space-y-1 text-green-200">
                <p><span class="text-green-400">Attendee:</span> {{ result.ticket.attendee }}</p>
                <p><span class="text-green-400">Event:</span> {{ result.ticket.event }}</p>
                <p><span class="text-green-400">Tier:</span> {{ result.ticket.tier }}</p>
                <p class="font-mono text-sm opacity-75">{{ result.ticket.ticket_code }}</p>
              </div>
            </div>
          </div>

          <div class="mt-6 flex gap-3">
            <button
              @click="checkIn"
              :disabled="loading"
              class="flex-1 py-4 bg-green-500 text-white text-lg font-bold rounded-xl hover:bg-green-600 transition disabled:opacity-50"
            >
              <span v-if="loading">Checking in...</span>
              <span v-else>Confirm Check-In</span>
            </button>
            <button
              @click="reset"
              class="px-6 py-4 bg-gray-700 text-white font-medium rounded-xl hover:bg-gray-600 transition"
            >
              Cancel
            </button>
          </div>
        </div>

        <!-- Successfully Checked In -->
        <div
          v-else-if="result.checked_in"
          class="bg-green-900/50 border border-green-500 rounded-2xl p-6 text-center"
        >
          <div class="w-20 h-20 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-green-400 mb-2">Checked In!</h3>
          <p class="text-green-200 mb-1">{{ result.ticket.attendee }}</p>
          <p class="text-green-300/70 text-sm">{{ result.ticket.tier }}</p>

          <button
            @click="reset"
            class="mt-6 px-8 py-3 bg-gray-700 text-white font-medium rounded-xl hover:bg-gray-600 transition"
          >
            Next Ticket
          </button>
        </div>

        <!-- Invalid Ticket -->
        <div
          v-else
          class="bg-red-900/50 border border-red-500 rounded-2xl p-6"
        >
          <div class="flex items-start gap-4">
            <div class="w-12 h-12 bg-red-500 rounded-full flex items-center justify-center flex-shrink-0">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <div class="flex-1">
              <h3 class="text-xl font-bold text-red-400 mb-1">Invalid</h3>
              <p class="text-red-200">{{ result.message }}</p>
              <p v-if="result.checked_in_at" class="text-red-300/70 text-sm mt-2">
                Checked in at: {{ new Date(result.checked_in_at).toLocaleString() }}
              </p>
            </div>
          </div>

          <button
            @click="reset"
            class="mt-4 w-full py-3 bg-gray-700 text-white font-medium rounded-xl hover:bg-gray-600 transition"
          >
            Try Another
          </button>
        </div>
      </div>

      <!-- Recent Check-ins -->
      <div v-if="history.length > 0" class="bg-gray-800 rounded-2xl overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-700">
          <h2 class="font-bold text-white">Recent Check-ins</h2>
        </div>
        <div class="divide-y divide-gray-700">
          <div
            v-for="(item, index) in history.slice(0, 10)"
            :key="index"
            class="px-6 py-4 flex items-center justify-between"
          >
            <div>
              <p class="text-white font-medium">{{ item.attendee }}</p>
              <p class="text-gray-400 text-sm">{{ item.tier }}</p>
            </div>
            <div class="text-right">
              <p class="text-green-400 text-sm font-medium">Checked in</p>
              <p class="text-gray-500 text-xs">{{ formatTime(item.timestamp) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Instructions -->
      <div v-if="!result && history.length === 0" class="text-center py-12">
        <div class="w-20 h-20 bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-10 h-10 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" />
          </svg>
        </div>
        <h3 class="text-xl font-bold text-white mb-2">Ready to Check In</h3>
        <p class="text-gray-400 max-w-sm mx-auto">
          Enter the ticket code shown on the attendee's phone or scan their QR code.
        </p>
      </div>
    </div>
  </div>
</template>
