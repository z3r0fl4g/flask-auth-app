<template>
  <section class="py-16 lg:py-20 bg-gray-50/50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section Header -->
      <div class="text-center mb-14">
        <p class="text-xs uppercase tracking-[0.4em] text-gray-400 mb-3">How Tikepam Works</p>
        <h2 class="text-3xl font-semibold text-gray-900">Book Haitian events in three moves</h2>
      </div>

      <!-- Steps -->
      <div class="grid md:grid-cols-3 gap-8 lg:gap-12 relative">
        <!-- Connecting Line (Desktop only) -->
        <div class="hidden md:block absolute top-16 left-1/4 right-1/4 h-0.5 bg-gradient-to-r from-violet-200 via-rose-200 to-orange-200"></div>

        <!-- Step 1: Discover -->
        <div class="relative text-center">
          <div class="relative z-10 mb-6 mx-auto w-32 h-32 rounded-3xl bg-gradient-to-br from-violet-500/20 via-rose-500/15 to-orange-500/20 flex items-center justify-center shadow-lg">
            <svg class="h-12 w-12 text-violet-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <span class="absolute -top-2 -right-2 w-8 h-8 rounded-full bg-violet-500 text-white text-sm font-bold flex items-center justify-center shadow-lg">1</span>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 mb-3">Discover</h3>
          <p class="text-gray-600 max-w-xs mx-auto">
            Browse verified Haitian events near you or worldwide—Kompa nights, rara parades, brunches, and more.
          </p>
        </div>

        <!-- Step 2: Book -->
        <div class="relative text-center">
          <div class="relative z-10 mb-6 mx-auto w-32 h-32 rounded-3xl bg-gradient-to-br from-rose-500/20 via-violet-500/15 to-amber-500/20 flex items-center justify-center shadow-lg">
            <svg class="h-12 w-12 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" />
            </svg>
            <span class="absolute -top-2 -right-2 w-8 h-8 rounded-full bg-rose-500 text-white text-sm font-bold flex items-center justify-center shadow-lg">2</span>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 mb-3">Book</h3>
          <p class="text-gray-600 max-w-xs mx-auto">
            Secure your tickets instantly with protected checkout—early bird, VIP, or crew bundles, zero surprise fees.
          </p>
        </div>

        <!-- Step 3: Experience -->
        <div class="relative text-center">
          <div class="relative z-10 mb-6 mx-auto w-32 h-32 rounded-3xl bg-gradient-to-br from-amber-500/20 via-orange-500/15 to-rose-500/20 flex items-center justify-center shadow-lg">
            <svg class="h-12 w-12 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span class="absolute -top-2 -right-2 w-8 h-8 rounded-full bg-amber-500 text-white text-sm font-bold flex items-center justify-center shadow-lg">3</span>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 mb-3">Experience</h3>
          <p class="text-gray-600 max-w-xs mx-auto">
            Skip the line with mobile QR tickets—scan at the door and vibe with the diaspora.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// Static content for the 3-step process
</script>
