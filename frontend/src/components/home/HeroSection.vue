<template>
  <section class="relative py-16 lg:py-24">
    <!-- Background Decorations -->
    <div
      class="absolute inset-x-0 -top-32 mx-auto h-64 max-w-5xl bg-gradient-to-r from-azure-900/50 via-white to-amber-900/50 blur-3xl -z-10"
    ></div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center space-y-8">
        <!-- Badge -->
        <span
          class="inline-flex items-center gap-2 rounded-full border border-gray-200 bg-white px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.4em] text-gray-500 shadow-sm"
        >
          <svg class="h-4 w-4 text-rose-500" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2L9 9H2l6 4.5L5.5 22 12 17l6.5 5-2.5-8.5L22 9h-7l-3-7z"/>
          </svg>
          Tikepam • Real Haitian Events
        </span>

        <!-- Main Heading -->
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 leading-tight max-w-4xl mx-auto">
          Discover the
          <span class="bg-gradient-to-r from-violet-500 via-rose-500 to-orange-500 bg-clip-text text-transparent">
            Pulse of Haiti
          </span>
        </h1>

        <!-- Subtitle -->
        <p class="text-lg sm:text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
          From Kompa nights in Brooklyn to Rara parades in Miami—find verified events, grab tickets instantly, and keep the culture alive.
        </p>

        <!-- Search Bar -->
        <div class="max-w-4xl mx-auto mt-10">
          <div
            class="rounded-[32px] border border-white/70 bg-white/90 shadow-xl shadow-gray-200/60 backdrop-blur px-6 py-6 sm:px-8 sm:py-8"
          >
            <form class="grid gap-4 md:grid-cols-[1.2fr_1.2fr_0.8fr_auto]">
              <label class="flex flex-col text-left text-sm font-medium text-gray-600 gap-2">
                City or Region
                <input
                  type="text"
                  placeholder="Brooklyn, NY or Miami, FL"
                  class="rounded-2xl border border-gray-200 bg-white px-4 py-3 text-gray-700 placeholder:text-gray-400 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/30 transition-all"
                />
              </label>
              <label class="flex flex-col text-left text-sm font-medium text-gray-600 gap-2">
                Event Type
                <select
                  class="rounded-2xl border border-gray-200 bg-white px-4 py-3 text-gray-700 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/30 transition-all"
                >
                  <option>Any Haitian event</option>
                  <option>Kompa Night</option>
                  <option>Rara / Street Parade</option>
                  <option>Brunch / Day Party</option>
                  <option>Fundraiser / Community</option>
                </select>
              </label>
              <label class="flex flex-col text-left text-sm font-medium text-gray-600 gap-2">
                Date
                <input
                  type="date"
                  class="rounded-2xl border border-gray-200 bg-white px-4 py-3 text-gray-700 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/30 transition-all"
                />
              </label>
              <button
                type="submit"
                class="self-end inline-flex items-center justify-center gap-2 rounded-full bg-gradient-to-br from-violet-500 to-violet-400 px-6 py-3 text-sm font-semibold text-white shadow-lg transition-all hover:-translate-y-0.5 hover:shadow-xl w-full md:w-auto"
              >
                Find Events
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
            </form>
          </div>
        </div>

        <!-- CTA Buttons -->
        <div class="flex flex-wrap gap-4 justify-center pt-4">
          <router-link
            to="/signup"
            class="inline-flex items-center gap-2 rounded-full bg-gradient-to-br from-violet-500 to-violet-400 px-8 py-4 text-sm font-semibold text-white shadow-lg transition-all hover:-translate-y-0.5 hover:shadow-xl"
          >
            Browse Events
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 17l9.2-9.2M17 17V7m0 10H7" />
            </svg>
          </router-link>
          <router-link
            to="/login"
            class="inline-flex items-center gap-2 rounded-full border border-gray-200 bg-white px-8 py-4 text-sm font-semibold text-gray-700 shadow-sm hover:border-violet-500/40 transition-all"
          >
            List Your Event
            <svg class="h-4 w-4 text-violet-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </router-link>
        </div>

        <!-- Stats Ribbon -->
        <div class="flex flex-wrap justify-center gap-8 pt-8 text-sm">
          <div class="flex items-center gap-2">
            <span class="text-2xl font-bold text-gray-900">10,000+</span>
            <span class="text-gray-500">Events</span>
          </div>
          <div class="hidden sm:block w-px h-8 bg-gray-200"></div>
          <div class="flex items-center gap-2">
            <span class="text-2xl font-bold text-gray-900">50+</span>
            <span class="text-gray-500">Cities</span>
          </div>
          <div class="hidden sm:block w-px h-8 bg-gray-200"></div>
          <div class="flex items-center gap-2">
            <span class="text-2xl font-bold text-gray-900">100%</span>
            <span class="text-gray-500">Verified</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// Hero section - no props needed, uses static content with cultural Haitian messaging
</script>
