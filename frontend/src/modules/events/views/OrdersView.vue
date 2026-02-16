<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import Badge from '@/components/ui/Badge.vue'
import DataTable from '@/components/ui/DataTable.vue'
import { ShoppingCart } from 'lucide-vue-next'

const orders = ref([])
const loading = ref(true)
const error = ref(null)
const search = ref('')

onMounted(async () => {
  await fetchOrders()
})

async function fetchOrders() {
  loading.value = true
  error.value = null
  try {
    const response = await api.get('/api/orders/')
    orders.value = response.data.data?.orders || []
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to load orders'
    console.error('Failed to fetch orders:', err)
  } finally {
    loading.value = false
  }
}

const columns = [
  { key: 'id', label: 'Order #', sortable: true },
  { key: 'event_title', label: 'Event', sortable: true },
  { key: 'buyer', label: 'Buyer', sortable: true },
  { key: 'total', label: 'Amount', sortable: true, align: 'right' },
  { key: 'status', label: 'Status', sortable: true },
  { key: 'created_at', label: 'Date', sortable: true }
]

const filteredOrders = computed(() => {
  if (!search.value.trim()) return orders.value
  const q = search.value.toLowerCase()
  return orders.value.filter(o =>
    (o.event_title || '').toLowerCase().includes(q) ||
    (o.buyer || '').toLowerCase().includes(q) ||
    String(o.id).includes(q)
  )
})

function formatCurrency(cents) {
  if (!cents) return '$0.00'
  return `$${(cents / 100).toFixed(2)}`
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

function getStatusVariant(status) {
  const map = { completed: 'success', pending: 'warning', cancelled: 'error' }
  return map[status] || 'default'
}
</script>

<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900">Orders</h1>
      <p class="text-sm text-gray-500 mt-1">View and manage ticket orders</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="bg-white rounded-xl border border-gray-200 p-8 animate-pulse">
      <div class="space-y-4">
        <div class="h-10 bg-gray-200 rounded w-1/4"></div>
        <div class="h-8 bg-gray-200 rounded"></div>
        <div v-for="i in 5" :key="i" class="h-12 bg-gray-200 rounded"></div>
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-center py-16">
      <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      </div>
      <h2 class="text-xl font-bold text-gray-900 mb-2">Something went wrong</h2>
      <p class="text-gray-600 mb-6">{{ error }}</p>
      <button @click="fetchOrders" class="btn-primary">Try Again</button>
    </div>

    <!-- Empty State -->
    <div v-else-if="orders.length === 0" class="bg-white rounded-xl border border-gray-200 text-center py-16">
      <div class="w-20 h-20 bg-violet-100 rounded-full flex items-center justify-center mx-auto mb-6">
        <ShoppingCart :size="40" class="text-violet-600" />
      </div>
      <h2 class="text-xl font-bold text-gray-900 mb-2">No orders yet</h2>
      <p class="text-gray-600">Orders will appear here once attendees purchase tickets.</p>
    </div>

    <!-- Orders Table -->
    <DataTable v-else :columns="columns" :data="filteredOrders" :per-page="15" empty-text="No orders match your search">
      <template #header>
        <div class="relative w-full sm:w-64">
          <input
            v-model="search"
            type="text"
            placeholder="Search orders..."
            class="w-full pl-9 pr-4 py-2 text-sm border border-gray-200 rounded-lg focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 outline-hidden transition"
          />
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </template>

      <template #cell-id="{ value }">
        <span class="font-mono text-xs text-gray-500">#{{ value }}</span>
      </template>

      <template #cell-event_title="{ value }">
        <span class="font-medium text-gray-900">{{ value || 'Unknown Event' }}</span>
      </template>

      <template #cell-total="{ value }">
        <span class="font-bold text-gray-900">{{ formatCurrency(value) }}</span>
      </template>

      <template #cell-status="{ value }">
        <Badge :variant="getStatusVariant(value)">{{ value }}</Badge>
      </template>

      <template #cell-created_at="{ value }">
        <span class="text-gray-500 text-sm">{{ formatDate(value) }}</span>
      </template>
    </DataTable>
  </div>
</template>
