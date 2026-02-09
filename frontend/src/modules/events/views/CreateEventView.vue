<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useEventsStore } from '@/stores/events'
import api from '@/services/api'

const router = useRouter()
const eventsStore = useEventsStore()

const loading = ref(false)
const error = ref(null)

// Form data
const form = ref({
  title: '',
  description: '',
  category: '',
  start_date: '',
  start_time: '',
  end_date: '',
  end_time: '',
  venue_name: '',
  venue_address: '',
  city: 'Port-au-Prince',
  is_online: false,
  online_url: '',
  cover_image: ''
})

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

// Validation
const isValid = computed(() => {
  if (!form.value.title.trim()) return false
  if (!form.value.start_date) return false
  if (!form.value.category) return false

  // Validate ticket tiers
  for (const tier of ticketTiers.value) {
    if (!tier.name.trim()) return false
    if (tier.quantity_total < 1) return false
  }

  return true
})

async function handleSubmit() {
  if (!isValid.value) return

  loading.value = true
  error.value = null

  try {
    const payload = {
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
        price: Math.round(tier.price * 100), // Convert dollars to cents
        quantity_total: tier.quantity_total,
        max_per_order: tier.max_per_order
      }))
    }

    const response = await api.post('/api/events/', payload)

    if (response.data.success) {
      router.push({ name: 'my-events' })
    } else {
      error.value = response.data.message
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to create event'
    console.error('Create event error:', err)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b">
      <div class="max-w-3xl mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold text-gray-900">Create Event</h1>
        <p class="text-gray-600 mt-2">Fill in the details to create your event</p>
      </div>
    </div>

    <!-- Form -->
    <div class="max-w-3xl mx-auto px-4 py-8">
      <form @submit.prevent="handleSubmit" class="space-y-8">
        <!-- Error Message -->
        <div v-if="error" class="p-4 bg-red-50 border border-red-200 rounded-xl text-red-700">
          {{ error }}
        </div>

        <!-- Basic Info -->
        <div class="bg-white rounded-2xl shadow-sm p-6 space-y-6">
          <h2 class="text-lg font-bold text-gray-900">Basic Information</h2>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Event Title *</label>
            <input
              v-model="form.title"
              type="text"
              placeholder="Enter event title"
              class="input w-full"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
            <textarea
              v-model="form.description"
              rows="4"
              placeholder="Describe your event..."
              class="input w-full"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Category *</label>
            <select v-model="form.category" class="input w-full" required>
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
            <label class="block text-sm font-medium text-gray-700 mb-2">Cover Image URL</label>
            <input
              v-model="form.cover_image"
              type="url"
              placeholder="https://example.com/image.jpg"
              class="input w-full"
            />
            <p class="mt-1 text-sm text-gray-500">Optional. Leave empty for a placeholder image.</p>
          </div>
        </div>

        <!-- Date & Time -->
        <div class="bg-white rounded-2xl shadow-sm p-6 space-y-6">
          <h2 class="text-lg font-bold text-gray-900">Date & Time</h2>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Start Date *</label>
              <input
                v-model="form.start_date"
                type="date"
                class="input w-full"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Start Time</label>
              <input
                v-model="form.start_time"
                type="time"
                class="input w-full"
              />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">End Date</label>
              <input
                v-model="form.end_date"
                type="date"
                class="input w-full"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">End Time</label>
              <input
                v-model="form.end_time"
                type="time"
                class="input w-full"
              />
            </div>
          </div>
        </div>

        <!-- Location -->
        <div class="bg-white rounded-2xl shadow-sm p-6 space-y-6">
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
                placeholder="Port-au-Prince"
                class="input w-full"
              />
            </div>
          </template>
        </div>

        <!-- Ticket Tiers -->
        <div class="bg-white rounded-2xl shadow-sm p-6 space-y-6">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-bold text-gray-900">Ticket Tiers</h2>
            <button
              type="button"
              @click="addTicketTier"
              class="text-sm font-medium text-violet-600 hover:text-violet-700"
            >
              + Add Tier
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
                class="text-sm text-red-600 hover:text-red-700"
              >
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
                  required
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
                  required
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

        <!-- Submit -->
        <div class="flex items-center justify-end gap-4">
          <router-link
            to="/my-events"
            class="px-6 py-3 text-gray-700 font-medium hover:text-gray-900 transition"
          >
            Cancel
          </router-link>
          <button
            type="submit"
            :disabled="!isValid || loading"
            :class="[
              'btn-primary',
              (!isValid || loading) && 'opacity-50 cursor-not-allowed'
            ]"
          >
            <span v-if="loading">Creating...</span>
            <span v-else>Create Event</span>
          </button>
        </div>

        <p class="text-sm text-gray-500 text-center">
          Your event will be saved as a draft. You can publish it from your events dashboard.
        </p>
      </form>
    </div>
  </div>
</template>
