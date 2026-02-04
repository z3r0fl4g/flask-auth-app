<template>
  <section class="py-16 lg:py-20 bg-gray-50/50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section Header -->
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6 mb-12">
        <div>
          <p class="text-xs uppercase tracking-[0.4em] text-gray-400 mb-3">Why Haitians Trust Tikepam</p>
          <h2 class="text-3xl font-semibold text-gray-900">Engineered for Real Events</h2>
        </div>
        <span
          class="inline-flex items-center gap-2 rounded-full bg-emerald-50 px-4 py-2 text-xs font-semibold text-emerald-600 w-fit"
        >
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
          Secure Payments · Encrypted Tickets · 24/7 Monitoring
        </span>
      </div>

      <!-- Trust Cards Grid -->
      <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        <article
          v-for="signal in trustSignals"
          :key="signal.title"
          class="rounded-3xl border border-gray-200 bg-white p-6 shadow-md shadow-gray-200/50 hover:-translate-y-1 transition-transform"
        >
          <div
            class="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl"
            :class="signal.iconBg"
          >
            <component :is="signal.icon" class="h-6 w-6" :class="signal.iconColor" />
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ signal.title }}</h3>
          <p class="text-sm text-gray-600">{{ signal.description }}</p>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup>
import { h } from 'vue'

// Icon components using render functions
const CheckCircleIcon = {
  render() {
    return h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' })
    ])
  }
}

const ShieldCheckIcon = {
  render() {
    return h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' })
    ])
  }
}

const GlobeIcon = {
  render() {
    return h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z' })
    ])
  }
}

const BoltIcon = {
  render() {
    return h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13 10V3L4 14h7v7l9-11h-7z' })
    ])
  }
}

const trustSignals = [
  {
    title: 'Verified Events',
    description: 'Every event is vetted by our team to ensure authenticity and quality for the Haitian community.',
    icon: CheckCircleIcon,
    iconBg: 'bg-violet-100',
    iconColor: 'text-violet-500'
  },
  {
    title: 'Secure Checkout',
    description: 'Protected payments with instant confirmations—clear pricing, no hidden fees, peace of mind.',
    icon: ShieldCheckIcon,
    iconBg: 'bg-emerald-100',
    iconColor: 'text-emerald-500'
  },
  {
    title: 'Diaspora Connected',
    description: 'Tap into the global Haitian network—from Brooklyn to Miami to Montreal to Port-au-Prince.',
    icon: GlobeIcon,
    iconBg: 'bg-azure-100',
    iconColor: 'text-azure-500'
  },
  {
    title: 'Fast Check-in',
    description: 'Skip the line with encrypted mobile QR tickets—scan at the door and you\'re inside instantly.',
    icon: BoltIcon,
    iconBg: 'bg-amber-100',
    iconColor: 'text-amber-500'
  }
]
</script>
