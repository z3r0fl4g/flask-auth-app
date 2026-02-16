<template>
  <div class="rounded-xl border border-gray-200 bg-white p-5">
    <h3 v-if="title" class="mb-4 text-sm font-semibold text-gray-900">{{ title }}</h3>
    <apexchart
      type="area"
      :height="height"
      :options="chartOptions"
      :series="series"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: { type: String, default: '' },
  series: { type: Array, required: true },
  categories: { type: Array, default: () => [] },
  height: { type: Number, default: 300 },
  colors: { type: Array, default: () => ['#8338ec', '#3a86ff'] }
})

const chartOptions = computed(() => ({
  chart: {
    fontFamily: 'Inter, system-ui, sans-serif',
    toolbar: { show: false },
    zoom: { enabled: false }
  },
  colors: props.colors,
  dataLabels: { enabled: false },
  stroke: { curve: 'smooth', width: 2 },
  fill: {
    type: 'gradient',
    gradient: { shadeIntensity: 1, opacityFrom: 0.3, opacityTo: 0.05, stops: [0, 90, 100] }
  },
  grid: {
    borderColor: '#f3f4f6',
    strokeDashArray: 4,
    xaxis: { lines: { show: false } }
  },
  xaxis: {
    categories: props.categories,
    labels: { style: { colors: '#9ca3af', fontSize: '12px' } },
    axisBorder: { show: false },
    axisTicks: { show: false }
  },
  yaxis: {
    labels: { style: { colors: '#9ca3af', fontSize: '12px' } }
  },
  tooltip: { theme: 'light' },
  legend: {
    position: 'top',
    horizontalAlign: 'right',
    fontSize: '12px',
    labels: { colors: '#6b7280' }
  }
}))
</script>
