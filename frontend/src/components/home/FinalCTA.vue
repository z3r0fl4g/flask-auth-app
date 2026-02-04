<template>
  <section class="py-16 lg:py-20">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div
        class="rounded-[38px] bg-gradient-to-r from-rose-500/10 via-white to-azure-500/10 px-8 py-12 lg:px-16 lg:py-16 text-center relative overflow-hidden"
      >
        <!-- Background Pattern (optional decorative) -->
        <div class="absolute inset-0 opacity-30">
          <div class="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-violet-500/20 to-transparent rounded-full blur-3xl"></div>
          <div class="absolute bottom-0 left-0 w-64 h-64 bg-gradient-to-tr from-amber-500/20 to-transparent rounded-full blur-3xl"></div>
        </div>

        <!-- Content -->
        <div class="relative z-10">
          <h2 class="text-3xl lg:text-4xl font-semibold text-gray-900 mb-4">
            Ready for Your Next Haitian Experience?
          </h2>
          <p class="text-base lg:text-lg text-gray-600 max-w-2xl mx-auto mb-8">
            Browse verified events or launch your own Kompa night, rara parade, brunch, or fundraiser. The diaspora is waiting—let's keep the culture loud.
          </p>

          <!-- CTA Buttons -->
          <div class="flex flex-wrap justify-center gap-4">
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
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </router-link>
          </div>

          <!-- Trust Badge -->
          <p class="mt-8 text-sm text-gray-500">
            <span class="inline-flex items-center gap-2">
              <svg class="h-4 w-4 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
              Trusted by 10,000+ Haitians worldwide
            </span>
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// Final CTA section with gradient background
</script>
