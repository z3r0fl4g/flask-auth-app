<template>
  <div class="overflow-hidden rounded-xl border border-gray-200 bg-white">
    <!-- Header slot (search, filters) -->
    <div v-if="$slots.header" class="border-b border-gray-100 px-5 py-4">
      <slot name="header" />
    </div>

    <!-- Table -->
    <div class="overflow-x-auto">
      <table class="w-full text-left text-sm">
        <thead>
          <tr class="border-b border-gray-100 bg-gray-50/50">
            <th
              v-for="col in columns"
              :key="col.key"
              :class="[
                'px-5 py-3 text-xs font-semibold uppercase tracking-wider text-gray-500',
                col.align === 'right' ? 'text-right' : '',
                col.align === 'center' ? 'text-center' : '',
                col.sortable ? 'cursor-pointer select-none hover:text-gray-700' : ''
              ]"
              @click="col.sortable && handleSort(col.key)"
            >
              {{ col.label }}
              <span v-if="col.sortable && sortKey === col.key" class="ml-1">
                {{ sortOrder === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(row, index) in paginatedData"
            :key="row.id || index"
            class="border-b border-gray-50 last:border-0 hover:bg-gray-50/50 transition-colors"
          >
            <td
              v-for="col in columns"
              :key="col.key"
              :class="[
                'px-5 py-3.5',
                col.align === 'right' ? 'text-right' : '',
                col.align === 'center' ? 'text-center' : ''
              ]"
            >
              <slot :name="'cell-' + col.key" :row="row" :value="row[col.key]">
                {{ row[col.key] }}
              </slot>
            </td>
          </tr>
          <tr v-if="paginatedData.length === 0">
            <td :colspan="columns.length" class="px-5 py-10 text-center text-gray-400">
              {{ emptyText }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex items-center justify-between border-t border-gray-100 px-5 py-3">
      <p class="text-sm text-gray-500">
        Showing {{ startIndex + 1 }}–{{ Math.min(endIndex, sortedData.length) }} of {{ sortedData.length }}
      </p>
      <div class="flex items-center gap-1">
        <button
          :disabled="currentPage === 1"
          class="rounded-lg px-3 py-1.5 text-sm font-medium text-gray-600 hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          @click="currentPage--"
        >
          Prev
        </button>
        <button
          v-for="page in visiblePages"
          :key="page"
          :class="[
            'rounded-lg px-3 py-1.5 text-sm font-medium transition-colors',
            page === currentPage
              ? 'bg-violet-50 text-violet-700'
              : 'text-gray-600 hover:bg-gray-100'
          ]"
          @click="currentPage = page"
        >
          {{ page }}
        </button>
        <button
          :disabled="currentPage === totalPages"
          class="rounded-lg px-3 py-1.5 text-sm font-medium text-gray-600 hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          @click="currentPage++"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  columns: { type: Array, required: true },
  data: { type: Array, default: () => [] },
  perPage: { type: Number, default: 10 },
  emptyText: { type: String, default: 'No data available' }
})

const currentPage = ref(1)
const sortKey = ref('')
const sortOrder = ref('asc')

function handleSort(key) {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
  currentPage.value = 1
}

const sortedData = computed(() => {
  if (!sortKey.value) return props.data
  return [...props.data].sort((a, b) => {
    const aVal = a[sortKey.value]
    const bVal = b[sortKey.value]
    if (aVal < bVal) return sortOrder.value === 'asc' ? -1 : 1
    if (aVal > bVal) return sortOrder.value === 'asc' ? 1 : -1
    return 0
  })
})

const totalPages = computed(() => Math.ceil(sortedData.value.length / props.perPage))
const startIndex = computed(() => (currentPage.value - 1) * props.perPage)
const endIndex = computed(() => startIndex.value + props.perPage)
const paginatedData = computed(() => sortedData.value.slice(startIndex.value, endIndex.value))

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, start + 4)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})
</script>
