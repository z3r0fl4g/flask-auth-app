<template>
  <footer v-if="!isAuthPage" class="relative mt-auto border-t border-gray-200 bg-white/80 backdrop-blur-sm overflow-hidden">
    <div class="absolute inset-x-0 -z-10 mx-auto h-32 max-w-5xl bg-gradient-to-r from-[#ffe59d]/50 via-white to-[#feddce]/50 blur-3xl pointer-events-none"></div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14 relative">
      <div class="grid gap-10 md:grid-cols-2 lg:grid-cols-4 text-sm text-gray-600">
        <!-- Brand Section -->
        <div class="space-y-4">
          <img src="/logo.svg" alt="Tikepam Haitian events logo" class="h-9">
          <p class="text-base font-semibold text-gray-900">Tikepam</p>
          <p class="text-sm text-gray-500 leading-relaxed">
            Tikepam keeps Haitians worldwide plugged into verified Kompa nights, rara parades, brunches, and fundraisers
            with instant, secure tickets.
          </p>
        </div>

        <!-- Explore Tikepam -->
        <div class="space-y-3">
          <h3 class="text-xs uppercase tracking-[0.35em] text-gray-400">Explore Tikepam</h3>
          <ul class="space-y-2">
            <li><router-link to="/" class="hover:text-gray-900 transition">Discover</router-link></li>
            <li><a href="#features" class="hover:text-gray-900 transition">How Tikepam Works</a></li>
            <li><a href="#schedule" class="hover:text-gray-900 transition">Live Events</a></li>
            <li><a href="#pricing" class="hover:text-gray-900 transition">Buy Tickets</a></li>
          </ul>
        </div>

        <!-- Resources & Support -->
        <div class="space-y-3">
          <h3 class="text-xs uppercase tracking-[0.35em] text-gray-400">Resources &amp; Support</h3>
          <ul class="space-y-2">
            <li><a href="/ui-design" class="hover:text-gray-900 transition">Organizer Help Desk</a></li>
            <li><router-link to="/forgot-password" class="hover:text-gray-900 transition">Reset Your Password</router-link></li>
            <li><router-link to="/2fa/settings" class="hover:text-gray-900 transition">Security &amp; 2FA</router-link></li>
            <li><a href="/security" class="hover:text-gray-900 transition">Platform Security</a></li>
          </ul>
        </div>

        <!-- Newsletter Section -->
        <div class="space-y-3">
          <h3 class="text-xs uppercase tracking-[0.35em] text-gray-400">Stay close to the Haitian scene</h3>
          <p>Get Haitian event drops, Kompa lineups, ticket alerts, and diaspora meetups delivered weekly.</p>
          <form @submit.prevent="handleNewsletterSubmit" class="flex flex-col gap-2">
            <div class="flex items-center gap-2 rounded-full border border-gray-200 px-3 py-2 text-sm text-gray-600 focus-within:ring-2 focus-within:ring-[#8338ec]/40">
              <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <input
                v-model="newsletterEmail"
                type="email"
                placeholder="name@email.com"
                class="flex-1 bg-transparent placeholder:text-gray-400 focus:outline-none"
              >
            </div>
            <button
              type="submit"
              class="inline-flex items-center justify-center gap-2 rounded-full bg-gradient-to-r from-[#8338ec] to-[#6414d5] px-4 py-2 text-sm font-semibold text-white shadow-md shadow-[#8338ec]/25 hover:shadow-lg transition-transform transform hover:-translate-y-0.5"
            >
              Get Event Drops · Pa rate l
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </button>
          </form>
          <div class="flex items-center gap-4 text-gray-400 pt-3">
            <a href="#" class="hover:text-gray-700 transition">
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.840 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.430.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
            </a>
            <a href="#" class="hover:text-gray-700 transition">
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
              </svg>
            </a>
            <a href="#" class="hover:text-gray-700 transition">
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.070-4.85.070-3.204 0-3.584-.012-4.849-.070-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
              </svg>
            </a>
            <a href="#" class="hover:text-gray-700 transition">
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
              </svg>
            </a>
          </div>
        </div>
      </div>

      <div class="mt-12 border-t border-gray-200 pt-6 text-xs text-gray-500 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <p>© 2025 Tikepam. Haitian events built for the diaspora.</p>
        <div class="flex items-center gap-4">
          <a href="/privacy" class="hover:text-gray-800 transition">Privacy Notice</a>
          <a href="/terms" class="hover:text-gray-800 transition">Terms of Service</a>
          <a href="/status" class="hover:text-gray-800 transition">System Status</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const newsletterEmail = ref('')

// Hide footer on login and signup pages
const isAuthPage = computed(() => {
  return ['login', 'signup', 'twofa-verify'].includes(route.name)
})

function handleNewsletterSubmit() {
  // TODO: Implement newsletter subscription
  console.log('Newsletter signup:', newsletterEmail.value)
  newsletterEmail.value = ''
}
</script>
