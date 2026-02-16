<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useEventsStore } from '@/stores/events'
import { toast } from 'vue-sonner'
import api from '@/services/api'
import Badge from '@/components/ui/Badge.vue'
import { ChevronLeft, ChevronRight, Plus, Trash2, Check, CalendarDays, MapPin, Globe, TicketCheck, Eye } from 'lucide-vue-next'

const router = useRouter()
const eventsStore = useEventsStore()

const loading = ref(false)
const error = ref(null)
const currentStep = ref(1)
const totalSteps = 4

const steps = [
  { number: 1, label: 'Details' },
  { number: 2, label: 'Date & Location' },
  { number: 3, label: 'Tickets' },
  { number: 4, label: 'Review & Publish' }
]

// Form data
const form = ref({
  title: '',
  description: '',
  category: '',
  cover_image: '',
  start_date: '',
  start_time: '',
  end_date: '',
  end_time: '',
  venue_name: '',
  venue_address: '',
  city: 'Port-au-Prince',
  is_online: false,
  online_url: ''
})

// Haitian cities for datalist
const haitianCities = [
  'Port-au-Prince', 'Cap-Haïtien', 'Gonaïves', 'Les Cayes',
  'Pétion-Ville', 'Delmas', 'Jacmel', 'Jérémie',
  'Saint-Marc', 'Hinche', 'Fort-Liberté', 'Port-de-Paix',
  'Kenscoff', 'Tabarre', 'Carrefour', 'Croix-des-Bouquets'
]

// Ticket tiers
const ticketTiers = ref([
  { name: 'General Admission', description: '', price: 0, quantity_total: 100, max_per_order: 10 }
])

function addTicketTier() {
  ticketTiers.value.push({
    name: '',
    description: '',
    price: 0,
    quantity_total: 50,
    max_per_order: 10
  })
}

function removeTicketTier(index) {
  if (ticketTiers.value.length > 1) {
    ticketTiers.value.splice(index, 1)
  }
}

// Convert local datetime to ISO string
function toISODateTime(date, time) {
  if (!date) return null
  const dateTime = time ? `${date}T${time}` : `${date}T00:00`
  return new Date(dateTime).toISOString()
}

// Per-step validation
const step1Valid = computed(() => {
  return form.value.title.trim().length > 0 && form.value.category.length > 0
})

const step2Valid = computed(() => {
  return form.value.start_date.length > 0
})

const step3Valid = computed(() => {
  return ticketTiers.value.every(tier =>
    tier.name.trim().length > 0 && tier.quantity_total >= 1
  )
})

const isCurrentStepValid = computed(() => {
  const validators = { 1: step1Valid, 2: step2Valid, 3: step3Valid, 4: computed(() => true) }
  return validators[currentStep.value]?.value ?? true
})

const isAllValid = computed(() => step1Valid.value && step2Valid.value && step3Valid.value)

function nextStep() {
  if (isCurrentStepValid.value && currentStep.value < totalSteps) {
    currentStep.value++
  }
}

function prevStep() {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

function goToStep(step) {
  // Allow going back to any step, forward only if current is valid
  if (step < currentStep.value || isCurrentStepValid.value) {
    currentStep.value = step
  }
}

function buildPayload() {
  return {
    title: form.value.title,
    description: form.value.description,
    category: form.value.category,
    start_date: toISODateTime(form.value.start_date, form.value.start_time),
    end_date: form.value.end_date ? toISODateTime(form.value.end_date, form.value.end_time) : null,
    venue_name: form.value.venue_name,
    venue_address: form.value.venue_address,
    city: form.value.city,
    is_online: form.value.is_online,
    online_url: form.value.online_url,
    cover_image: form.value.cover_image,
    ticket_tiers: ticketTiers.value.map(tier => ({
      name: tier.name,
      description: tier.description,
      price: Math.round(tier.price * 100),
      quantity_total: tier.quantity_total,
      max_per_order: tier.max_per_order
    }))
  }
}

async function saveDraft() {
  if (!isAllValid.value) return
  loading.value = true
  error.value = null

  try {
    const response = await api.post('/api/events/', buildPayload())
    if (response.data.success) {
      toast.success(`"${form.value.title}" saved as draft.`)
      router.push({ name: 'my-events' })
    } else {
      error.value = response.data.message
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to create event'
    toast.error(err.response?.data?.message || 'Failed to create event')
  } finally {
    loading.value = false
  }
}

async function createAndPublish() {
  if (!isAllValid.value) return
  loading.value = true
  error.value = null

  try {
    // Create event first
    const response = await api.post('/api/events/', buildPayload())
    if (response.data.success) {
      const eventId = response.data.data.event.id
      // Then publish it
      try {
        await api.post(`/api/events/${eventId}/publish`)
        toast.success(`"${form.value.title}" is now live!`)
      } catch {
        toast.warning('Event saved as draft. Publishing failed.')
      }
      router.push({ name: 'my-events' })
    } else {
      error.value = response.data.message
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to create event'
    toast.error(err.response?.data?.message || 'Failed to create event')
  } finally {
    loading.value = false
  }
}

// Formatting helpers for review step
function formatDate(dateStr) {
  if (!dateStr) return 'Not set'
  return new Date(dateStr + 'T00:00').toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
    year: 'numeric'
  })
}

function formatTime(timeStr) {
  if (!timeStr) return ''
  const [h, m] = timeStr.split(':')
  const hour = parseInt(h)
  const ampm = hour >= 12 ? 'PM' : 'AM'
  const displayHour = hour % 12 || 12
  return `${displayHour}:${m} ${ampm}`
}

function formatPrice(price) {
  return price === 0 ? 'Free' : `$${price.toFixed(2)}`
}
</script>

<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900">Create Event</h1>
      <p class="text-sm text-gray-500 mt-1">Fill in the details to create your event</p>
    </div>

    <!-- Progress Steps -->
    <div class="bg-white rounded-xl border border-gray-200 p-4">
      <div class="flex items-center justify-between">
        <button
          v-for="step in steps"
          :key="step.number"
          @click="goToStep(step.number)"
          class="flex items-center gap-2 group"
        >
          <div
            :class="[
              'w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-colors',
              currentStep === step.number
                ? 'bg-violet-600 text-white'
                : step.number < currentStep
                ? 'bg-green-100 text-green-700'
                : 'bg-gray-100 text-gray-400'
            ]"
          >
            <Check v-if="step.number < currentStep" :size="16" />
            <span v-else>{{ step.number }}</span>
          </div>
          <span
            :class="[
              'text-sm font-medium hidden sm:inline transition-colors',
              currentStep === step.number
                ? 'text-gray-900'
                : step.number < currentStep
                ? 'text-green-700'
                : 'text-gray-400'
            ]"
          >
            {{ step.label }}
          </span>
          <!-- Connector line -->
          <div
            v-if="step.number < totalSteps"
            :class="[
              'hidden sm:block w-12 lg:w-24 h-0.5 ml-2',
              step.number < currentStep ? 'bg-green-200' : 'bg-gray-200'
            ]"
          ></div>
        </button>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="p-4 bg-red-50 border border-red-300 rounded-xl text-red-800">
      {{ error }}
    </div>

    <!-- Step 1: Details -->
    <div v-show="currentStep === 1" class="bg-white rounded-xl border border-gray-200 p-6 space-y-6">
      <h2 class="text-lg font-bold text-gray-900">Event Details</h2>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Event Title *</label>
        <input
          v-model="form.title"
          type="text"
          placeholder="What's your event called?"
          class="input w-full"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Category *</label>
        <select v-model="form.category" class="input w-full">
          <option value="">Select a category</option>
          <option
            v-for="cat in eventsStore.categories"
            :key="cat.value"
            :value="cat.value"
          >
            {{ cat.label }}
          </option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
        <textarea
          v-model="form.description"
          rows="4"
          placeholder="Tell people what to expect at your event..."
          class="input w-full"
        ></textarea>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Cover Image URL</label>
        <input
          v-model="form.cover_image"
          type="url"
          placeholder="https://example.com/image.jpg"
          class="input w-full"
        />
        <p class="mt-1 text-xs text-gray-500">Optional. Leave empty for a placeholder image.</p>
        <!-- Image Preview -->
        <div v-if="form.cover_image" class="mt-3">
          <img
            :src="form.cover_image"
            alt="Cover preview"
            class="w-full max-w-sm h-40 object-cover rounded-lg border border-gray-200"
            @error="$event.target.style.display = 'none'"
          />
        </div>
      </div>
    </div>

    <!-- Step 2: Date & Location -->
    <div v-show="currentStep === 2" class="space-y-6">
      <div class="bg-white rounded-xl border border-gray-200 p-6 space-y-6">
        <h2 class="text-lg font-bold text-gray-900">Date & Time</h2>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Start Date *</label>
            <input v-model="form.start_date" type="date" class="input w-full" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Start Time</label>
            <input v-model="form.start_time" type="time" class="input w-full" />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">End Date</label>
            <input v-model="form.end_date" type="date" class="input w-full" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">End Time</label>
            <input v-model="form.end_time" type="time" class="input w-full" />
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl border border-gray-200 p-6 space-y-6">
        <h2 class="text-lg font-bold text-gray-900">Location</h2>

        <div class="flex items-center gap-3">
          <input
            v-model="form.is_online"
            type="checkbox"
            id="is_online"
            class="w-5 h-5 rounded border-gray-300 text-violet-600 focus:ring-violet-500"
          />
          <label for="is_online" class="text-sm font-medium text-gray-700">
            This is an online event
          </label>
        </div>

        <template v-if="form.is_online">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Online URL</label>
            <input
              v-model="form.online_url"
              type="url"
              placeholder="https://zoom.us/..."
              class="input w-full"
            />
          </div>
        </template>

        <template v-else>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Venue Name</label>
            <input
              v-model="form.venue_name"
              type="text"
              placeholder="e.g., Karibe Hotel"
              class="input w-full"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Address</label>
            <input
              v-model="form.venue_address"
              type="text"
              placeholder="Full address"
              class="input w-full"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">City</label>
            <input
              v-model="form.city"
              type="text"
              list="haitian-cities"
              placeholder="Port-au-Prince"
              class="input w-full"
            />
            <datalist id="haitian-cities">
              <option v-for="city in haitianCities" :key="city" :value="city" />
            </datalist>
          </div>
        </template>
      </div>
    </div>

    <!-- Step 3: Tickets -->
    <div v-show="currentStep === 3" class="bg-white rounded-xl border border-gray-200 p-6 space-y-6">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-bold text-gray-900">Ticket Tiers</h2>
        <button
          type="button"
          @click="addTicketTier"
          class="flex items-center gap-1 text-sm font-medium text-violet-600 hover:text-violet-700"
        >
          <Plus :size="16" />
          Add Tier
        </button>
      </div>

      <div
        v-for="(tier, index) in ticketTiers"
        :key="index"
        class="p-4 border border-gray-200 rounded-xl space-y-4"
      >
        <div class="flex items-center justify-between">
          <span class="font-medium text-gray-900">Tier {{ index + 1 }}</span>
          <button
            v-if="ticketTiers.length > 1"
            type="button"
            @click="removeTicketTier(index)"
            class="flex items-center gap-1 text-sm text-red-600 hover:text-red-700"
          >
            <Trash2 :size="14" />
            Remove
          </button>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div class="col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-2">Name *</label>
            <input
              v-model="tier.name"
              type="text"
              placeholder="e.g., General Admission, VIP"
              class="input w-full"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Price ($)</label>
            <input
              v-model.number="tier.price"
              type="number"
              min="0"
              step="0.01"
              placeholder="0.00"
              class="input w-full"
            />
            <p class="mt-1 text-xs text-gray-500">Enter 0 for free tickets</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Quantity *</label>
            <input
              v-model.number="tier.quantity_total"
              type="number"
              min="1"
              placeholder="100"
              class="input w-full"
            />
          </div>

          <div class="col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
            <input
              v-model="tier.description"
              type="text"
              placeholder="What's included?"
              class="input w-full"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Max per order</label>
            <input
              v-model.number="tier.max_per_order"
              type="number"
              min="1"
              max="50"
              class="input w-full"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Step 4: Review -->
    <div v-show="currentStep === 4" class="space-y-6">
      <!-- Event Summary -->
      <div class="bg-white rounded-xl border border-gray-200 p-6 space-y-5">
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-bold text-gray-900">Review Your Event</h2>
          <Badge variant="draft">Draft</Badge>
        </div>

        <!-- Cover Preview -->
        <div v-if="form.cover_image" class="rounded-lg overflow-hidden">
          <img
            :src="form.cover_image"
            alt="Cover"
            class="w-full h-48 object-cover"
            @error="$event.target.style.display = 'none'"
          />
        </div>

        <!-- Details -->
        <div class="space-y-3">
          <div>
            <h3 class="text-xl font-bold text-gray-900">{{ form.title || 'Untitled Event' }}</h3>
            <p class="text-sm text-gray-500 mt-0.5">{{ eventsStore.getCategoryLabel(form.category) || 'No category' }}</p>
          </div>

          <p v-if="form.description" class="text-sm text-gray-600">{{ form.description }}</p>

          <!-- Date & Location Info -->
          <div class="flex flex-wrap gap-4 text-sm text-gray-600">
            <div class="flex items-center gap-1.5">
              <CalendarDays :size="16" class="text-gray-400" />
              <span>{{ formatDate(form.start_date) }}</span>
              <span v-if="form.start_time" class="text-gray-400">at {{ formatTime(form.start_time) }}</span>
            </div>
            <div class="flex items-center gap-1.5">
              <component :is="form.is_online ? Globe : MapPin" :size="16" class="text-gray-400" />
              <span v-if="form.is_online">Online Event</span>
              <span v-else>{{ form.venue_name || form.city || 'No venue' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Ticket Summary -->
      <div class="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
        <h3 class="text-base font-bold text-gray-900 flex items-center gap-2">
          <TicketCheck :size="18" class="text-violet-500" />
          Tickets
        </h3>

        <div class="space-y-2">
          <div
            v-for="(tier, index) in ticketTiers"
            :key="index"
            class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
          >
            <div>
              <span class="font-medium text-gray-900">{{ tier.name }}</span>
              <span v-if="tier.description" class="text-xs text-gray-500 ml-2">{{ tier.description }}</span>
            </div>
            <div class="text-right">
              <span class="font-bold text-gray-900">{{ formatPrice(tier.price) }}</span>
              <span class="text-xs text-gray-500 ml-2">{{ tier.quantity_total }} available</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <div class="flex items-center justify-between bg-white rounded-xl border border-gray-200 p-4">
      <button
        v-if="currentStep > 1"
        @click="prevStep"
        class="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 transition"
      >
        <ChevronLeft :size="18" />
        Back
      </button>
      <router-link
        v-else
        to="/my-events"
        class="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 transition"
      >
        Cancel
      </router-link>

      <div class="flex items-center gap-3">
        <!-- Next button (steps 1-3) -->
        <button
          v-if="currentStep < totalSteps"
          @click="nextStep"
          :disabled="!isCurrentStepValid"
          :class="[
            'btn-primary',
            !isCurrentStepValid && 'opacity-50 cursor-not-allowed'
          ]"
        >
          Next
          <ChevronRight :size="18" class="ml-1" />
        </button>

        <!-- Final step actions -->
        <template v-if="currentStep === totalSteps">
          <button
            @click="saveDraft"
            :disabled="!isAllValid || loading"
            class="px-5 py-2.5 text-sm font-medium text-gray-700 border border-gray-300 rounded-full hover:bg-gray-50 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ loading ? 'Saving...' : 'Save as Draft' }}
          </button>
          <button
            @click="createAndPublish"
            :disabled="!isAllValid || loading"
            :class="[
              'btn-primary',
              (!isAllValid || loading) && 'opacity-50 cursor-not-allowed'
            ]"
          >
            {{ loading ? 'Publishing...' : 'Create & Publish' }}
          </button>
        </template>
      </div>
    </div>
  </div>
</template>
