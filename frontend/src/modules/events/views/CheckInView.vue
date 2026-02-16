<script setup>
import { ref } from 'vue'
import { toast } from 'vue-sonner'
import api from '@/services/api'
import Badge from '@/components/ui/Badge.vue'
import { ScanLine, CheckCircle, XCircle, RotateCcw } from 'lucide-vue-next'

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
      history.value.unshift({
        ...response.data.ticket,
        timestamp: new Date()
      })

      result.value = {
        valid: true,
        checked_in: true,
        message: 'Check-in successful!',
        ticket: response.data.ticket
      }

      toast.success('Check-in successful!')
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
    toast.error(err.response?.data?.message || 'Check-in failed')
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
  <div class="space-y-6">
    <!-- Page Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900">Check-In</h1>
      <p class="text-sm text-gray-500 mt-1">Scan or enter ticket codes to check in attendees</p>
    </div>

    <!-- Input Section -->
    <div class="bg-white rounded-xl border border-gray-200 p-6">
      <div class="flex gap-3">
        <div class="relative flex-1">
          <ScanLine :size="18" class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            v-model="ticketCode"
            type="text"
            placeholder="Enter ticket code (e.g., TIK-XXXXXXXXXX)"
            class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl text-sm font-mono focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 outline-hidden transition"
            @keyup.enter="validateTicket"
            :disabled="loading"
          />
        </div>
        <button
          @click="validateTicket"
          :disabled="loading || !ticketCode.trim()"
          class="btn-primary"
        >
          {{ loading ? 'Checking...' : 'Validate' }}
        </button>
      </div>
    </div>

    <!-- Result Section -->
    <div v-if="result">
      <!-- Valid Ticket (Ready to Check In) -->
      <div
        v-if="result.valid && !result.checked_in"
        class="bg-green-50 border border-green-200 rounded-xl p-6"
      >
        <div class="flex items-start gap-4">
          <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center shrink-0">
            <CheckCircle :size="24" class="text-green-600" />
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-bold text-green-800 mb-2">Valid Ticket</h3>
            <div class="space-y-1 text-sm text-green-700">
              <p><span class="font-medium">Attendee:</span> {{ result.ticket.attendee }}</p>
              <p><span class="font-medium">Event:</span> {{ result.ticket.event }}</p>
              <p><span class="font-medium">Tier:</span> {{ result.ticket.tier }}</p>
              <p class="font-mono text-xs text-green-600">{{ result.ticket.ticket_code }}</p>
            </div>
          </div>
        </div>

        <div class="mt-5 flex gap-3">
          <button
            @click="checkIn"
            :disabled="loading"
            class="flex-1 py-3 bg-green-600 text-white font-bold rounded-xl hover:bg-green-700 transition disabled:opacity-50"
          >
            {{ loading ? 'Checking in...' : 'Confirm Check-In' }}
          </button>
          <button
            @click="reset"
            class="px-5 py-3 border border-gray-300 text-gray-700 font-medium rounded-xl hover:bg-gray-50 transition"
          >
            Cancel
          </button>
        </div>
      </div>

      <!-- Successfully Checked In -->
      <div
        v-else-if="result.checked_in"
        class="bg-green-50 border border-green-200 rounded-xl p-6 text-center"
      >
        <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <CheckCircle :size="32" class="text-green-600" />
        </div>
        <h3 class="text-xl font-bold text-green-800 mb-1">Checked In!</h3>
        <p class="text-green-700">{{ result.ticket.attendee }}</p>
        <p class="text-green-600 text-sm">{{ result.ticket.tier }}</p>

        <button
          @click="reset"
          class="mt-5 px-6 py-2.5 border border-gray-300 text-gray-700 font-medium rounded-xl hover:bg-gray-50 transition"
        >
          <RotateCcw :size="16" class="inline mr-1.5" />
          Next Ticket
        </button>
      </div>

      <!-- Invalid Ticket -->
      <div
        v-else
        class="bg-red-50 border border-red-200 rounded-xl p-6"
      >
        <div class="flex items-start gap-4">
          <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center shrink-0">
            <XCircle :size="24" class="text-red-600" />
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-bold text-red-800 mb-1">Invalid</h3>
            <p class="text-red-700 text-sm">{{ result.message }}</p>
            <p v-if="result.checked_in_at" class="text-red-500 text-xs mt-1">
              Checked in at: {{ new Date(result.checked_in_at).toLocaleString() }}
            </p>
          </div>
        </div>

        <button
          @click="reset"
          class="mt-4 w-full py-2.5 border border-gray-300 text-gray-700 font-medium rounded-xl hover:bg-gray-50 transition"
        >
          Try Another
        </button>
      </div>
    </div>

    <!-- Recent Check-ins -->
    <div v-if="history.length > 0" class="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <div class="px-5 py-4 border-b border-gray-100">
        <h2 class="font-bold text-gray-900">Recent Check-ins</h2>
      </div>
      <div class="divide-y divide-gray-100">
        <div
          v-for="(item, index) in history.slice(0, 10)"
          :key="index"
          class="px-5 py-3.5 flex items-center justify-between"
        >
          <div>
            <p class="font-medium text-gray-900 text-sm">{{ item.attendee }}</p>
            <p class="text-gray-500 text-xs">{{ item.tier }}</p>
          </div>
          <div class="text-right">
            <Badge variant="success">Checked in</Badge>
            <p class="text-gray-400 text-xs mt-0.5">{{ formatTime(item.timestamp) }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!result && history.length === 0" class="bg-white rounded-xl border border-gray-200 text-center py-16">
      <div class="w-20 h-20 bg-violet-100 rounded-full flex items-center justify-center mx-auto mb-6">
        <ScanLine :size="40" class="text-violet-600" />
      </div>
      <h3 class="text-xl font-bold text-gray-900 mb-2">Ready to Check In</h3>
      <p class="text-gray-500 max-w-sm mx-auto text-sm">
        Enter the ticket code shown on the attendee's phone or scan their QR code to get started.
      </p>
    </div>
  </div>
</template>
