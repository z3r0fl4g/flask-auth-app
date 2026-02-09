<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  tiers: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['update:selection', 'checkout'])

// Track quantities for each tier
const quantities = ref({})

// Initialize quantities
props.tiers.forEach(tier => {
  quantities.value[tier.id] = 0
})

// Computed totals
const selectedItems = computed(() => {
  return props.tiers
    .filter(tier => quantities.value[tier.id] > 0)
    .map(tier => ({
      tier_id: tier.id,
      name: tier.name,
      price: tier.price,
      quantity: quantities.value[tier.id],
      subtotal: tier.price * quantities.value[tier.id]
    }))
})

const totalAmount = computed(() => {
  return selectedItems.value.reduce((sum, item) => sum + item.subtotal, 0)
})

const totalTickets = computed(() => {
  return selectedItems.value.reduce((sum, item) => sum + item.quantity, 0)
})

function increment(tier) {
  if (tier.is_sold_out) return
  const current = quantities.value[tier.id] || 0
  const max = Math.min(tier.max_per_order, tier.quantity_available)
  if (current < max) {
    quantities.value[tier.id] = current + 1
    emitSelection()
  }
}

function decrement(tier) {
  const current = quantities.value[tier.id] || 0
  if (current > 0) {
    quantities.value[tier.id] = current - 1
    emitSelection()
  }
}

function emitSelection() {
  emit('update:selection', selectedItems.value)
}

function handleCheckout() {
  if (totalTickets.value > 0) {
    emit('checkout', selectedItems.value)
  }
}
</script>

<template>
  <div class="bg-white rounded-2xl shadow-lg overflow-hidden">
    <div class="p-6 border-b bg-gray-50">
      <h3 class="text-lg font-bold text-gray-900">Select Tickets</h3>
    </div>

    <!-- Ticket Tiers -->
    <div class="divide-y">
      <div
        v-for="tier in tiers"
        :key="tier.id"
        :class="[
          'p-6 transition-colors',
          tier.is_sold_out ? 'bg-gray-50 opacity-60' : 'hover:bg-gray-50'
        ]"
      >
        <div class="flex items-start justify-between gap-4">
          <!-- Tier Info -->
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-1">
              <h4 class="font-semibold text-gray-900">{{ tier.name }}</h4>
              <span
                v-if="tier.is_sold_out"
                class="px-2 py-0.5 bg-red-100 text-red-700 text-xs font-medium rounded-full"
              >
                Sold Out
              </span>
              <span
                v-else-if="tier.quantity_available <= 10"
                class="px-2 py-0.5 bg-amber-100 text-amber-700 text-xs font-medium rounded-full"
              >
                {{ tier.quantity_available }} left
              </span>
            </div>
            <p v-if="tier.description" class="text-sm text-gray-600 mb-2">
              {{ tier.description }}
            </p>
            <p class="text-lg font-bold text-violet-600">
              {{ tier.price === 0 ? 'Free' : tier.price_display }}
            </p>
          </div>

          <!-- Quantity Selector -->
          <div v-if="!tier.is_sold_out" class="flex items-center gap-3">
            <button
              @click="decrement(tier)"
              :disabled="!quantities[tier.id]"
              :class="[
                'w-10 h-10 rounded-full flex items-center justify-center transition-all',
                quantities[tier.id] > 0
                  ? 'bg-violet-100 text-violet-600 hover:bg-violet-200'
                  : 'bg-gray-100 text-gray-400 cursor-not-allowed'
              ]"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
              </svg>
            </button>

            <span class="w-8 text-center font-semibold text-lg">
              {{ quantities[tier.id] || 0 }}
            </span>

            <button
              @click="increment(tier)"
              :disabled="quantities[tier.id] >= Math.min(tier.max_per_order, tier.quantity_available)"
              :class="[
                'w-10 h-10 rounded-full flex items-center justify-center transition-all',
                quantities[tier.id] < Math.min(tier.max_per_order, tier.quantity_available)
                  ? 'bg-violet-600 text-white hover:bg-violet-700'
                  : 'bg-gray-100 text-gray-400 cursor-not-allowed'
              ]"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Checkout Summary -->
    <div v-if="totalTickets > 0" class="p-6 bg-gradient-to-r from-violet-600 to-purple-600 text-white">
      <div class="flex items-center justify-between mb-4">
        <div>
          <p class="text-white/80 text-sm">{{ totalTickets }} ticket{{ totalTickets !== 1 ? 's' : '' }}</p>
          <p class="text-2xl font-bold">
            {{ totalAmount === 0 ? 'Free' : `$${(totalAmount / 100).toFixed(2)}` }}
          </p>
        </div>
        <button
          @click="handleCheckout"
          class="px-8 py-3 bg-white text-violet-600 font-bold rounded-full hover:bg-gray-100 transition-colors shadow-lg"
        >
          Get Tickets
        </button>
      </div>

      <!-- Selected items breakdown -->
      <div class="text-sm text-white/70 space-y-1">
        <div v-for="item in selectedItems" :key="item.tier_id" class="flex justify-between">
          <span>{{ item.quantity }}x {{ item.name }}</span>
          <span>{{ item.price === 0 ? 'Free' : `$${(item.subtotal / 100).toFixed(2)}` }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
