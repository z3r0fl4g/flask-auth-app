<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import StatCard from '@/components/ui/StatCard.vue'
import LineChart from '@/components/ui/LineChart.vue'
import BarChart from '@/components/ui/BarChart.vue'
import { DollarSign, TicketCheck, CalendarDays, TrendingUp } from 'lucide-vue-next'

const events = ref([])
const orders = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  await fetchData()
})

async function fetchData() {
  loading.value = true
  error.value = null
  try {
    const [eventsRes, ordersRes] = await Promise.all([
      api.get('/api/events/my-events'),
      api.get('/api/orders/')
    ])
    events.value = eventsRes.data.data.events || []
    orders.value = ordersRes.data.data?.orders || []
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to load analytics'
    console.error('Failed to fetch analytics:', err)
  } finally {
    loading.value = false
  }
}

// Stats
const totalRevenue = computed(() => {
  return orders.value
    .filter(o => o.status === 'completed')
    .reduce((sum, o) => sum + (o.total || 0), 0)
})

const totalTicketsSold = computed(() => {
  return events.value.reduce((sum, e) => {
    if (!e.ticket_tiers) return sum
    return sum + e.ticket_tiers.reduce((s, t) => s + (t.quantity_sold || 0), 0)
  }, 0)
})

const activeEvents = computed(() => {
  return events.value.filter(e => e.status === 'published').length
})

const formatCurrency = (cents) => {
  return `$${(cents / 100).toLocaleString('en-US', { minimumFractionDigits: 2 })}`
}

// Chart data — sales over last 7 days
const salesChartSeries = computed(() => {
  const days = 7
  const counts = new Array(days).fill(0)
  const now = new Date()

  orders.value
    .filter(o => o.status === 'completed')
    .forEach(order => {
      const orderDate = new Date(order.created_at)
      const daysAgo = Math.floor((now - orderDate) / (1000 * 60 * 60 * 24))
      if (daysAgo >= 0 && daysAgo < days) {
        counts[days - 1 - daysAgo]++
      }
    })

  return [{ name: 'Orders', data: counts }]
})

const salesChartCategories = computed(() => {
  const days = 7
  const categories = []
  for (let i = days - 1; i >= 0; i--) {
    const d = new Date()
    d.setDate(d.getDate() - i)
    categories.push(d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }))
  }
  return categories
})

// Revenue by event bar chart
const revenueByEventSeries = computed(() => {
  const eventRevenue = {}
  orders.value
    .filter(o => o.status === 'completed')
    .forEach(order => {
      const name = order.event_title || `Event #${order.event_id}`
      eventRevenue[name] = (eventRevenue[name] || 0) + (order.total || 0)
    })

  const entries = Object.entries(eventRevenue)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)

  return {
    series: [{ name: 'Revenue', data: entries.map(e => Math.round(e[1] / 100)) }],
    categories: entries.map(e => e[0])
  }
})
</script>

<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900">Analytics</h1>
      <p class="text-sm text-gray-500 mt-1">Track your event performance and revenue</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="space-y-4">
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div v-for="i in 3" :key="i" class="bg-white rounded-xl border border-gray-200 p-5 animate-pulse">
          <div class="h-4 bg-gray-200 rounded w-1/2 mb-3"></div>
          <div class="h-8 bg-gray-200 rounded w-1/3"></div>
        </div>
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
      <button @click="fetchData" class="btn-primary">Try Again</button>
    </div>

    <template v-else>
      <!-- Stat Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <StatCard
          label="Total Revenue"
          :value="formatCurrency(totalRevenue)"
          :icon="DollarSign"
          variant="green"
        />
        <StatCard
          label="Tickets Sold"
          :value="totalTicketsSold"
          :icon="TicketCheck"
          variant="violet"
        />
        <StatCard
          label="Active Events"
          :value="activeEvents"
          :icon="CalendarDays"
          variant="blue"
        />
      </div>

      <!-- Charts Row -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <LineChart
          title="Sales (Last 7 Days)"
          :series="salesChartSeries"
          :categories="salesChartCategories"
          :colors="['#8338ec']"
        />
        <BarChart
          v-if="revenueByEventSeries.categories.length > 0"
          title="Revenue by Event"
          :series="revenueByEventSeries.series"
          :categories="revenueByEventSeries.categories"
          :colors="['#3a86ff']"
        />
        <div v-else class="rounded-xl border border-gray-200 bg-white p-5 flex items-center justify-center">
          <p class="text-gray-400 text-sm">No revenue data yet</p>
        </div>
      </div>

      <!-- Empty state if no data at all -->
      <div v-if="events.length === 0 && orders.length === 0" class="bg-white rounded-xl border border-gray-200 text-center py-16">
        <div class="w-20 h-20 bg-violet-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <TrendingUp :size="40" class="text-violet-600" />
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">No data yet</h2>
        <p class="text-gray-600">Create and publish events to start seeing analytics here.</p>
      </div>
    </template>
  </div>
</template>
