<template>
  <nav
    class="sticky top-0 z-50 backdrop-blur-sm bg-white/95 border-b border-gray-200 shadow-sm"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex h-18 items-center justify-between gap-6 py-3">
        <!-- Logo -->
        <router-link to="/" class="flex items-center gap-3">
          <img src="/logo.svg" alt="Tikepam Haitian events logo" class="h-9" />
          <div class="hidden sm:block">
            <span class="text-lg font-semibold text-gray-900">Tikepam</span>
            <p class="text-[10px] tracking-[0.35em] uppercase text-gray-400">
              LIVE HAITIAN EVENTS
            </p>
          </div>
        </router-link>

        <!-- ============================================================ -->
        <!-- AUTHENTICATED: Icon nav + profile dropdown                    -->
        <!-- ============================================================ -->
        <template v-if="authStore.isAuthenticated && !hideNav">
          <!-- Search Bar -->
          <router-link
            to="/events"
            class="hidden lg:flex items-center gap-3 px-5 py-3 border-2 border-gray-200 hover:bg-gray-200 rounded-full text-gray-500 hover:text-gray-700 transition min-w-[280px]"
          >
            <svg
              class="h-5 w-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
            <span class="text-sm">Search events...</span>
          </router-link>

          <!-- Desktop icon links -->
          <div class="hidden md:flex items-center gap-8">
            <router-link
              to="/create-event"
              class="flex flex-col items-center gap-1 text-gray-500 hover:text-gray-900 transition group"
            >
              <svg
                class="h-5 w-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M12 4v16m8-8H4"
                />
              </svg>
              <span class="text-[11px] font-medium">Create Event</span>
            </router-link>

            <router-link
              to="/favorites"
              class="flex flex-col items-center gap-1 text-gray-500 hover:text-gray-900 transition group"
            >
              <svg
                class="h-5 w-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                />
              </svg>
              <span class="text-[11px] font-medium">Favorites</span>
            </router-link>

            <router-link
              to="/my-tickets"
              class="flex flex-col items-center gap-1 text-gray-500 hover:text-gray-900 transition group"
            >
              <svg
                class="h-5 w-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"
                />
              </svg>
              <span class="text-[11px] font-medium">Tickets</span>
            </router-link>

            <!-- Profile dropdown -->
            <div class="relative" ref="dropdownRef">
              <button
                @click="dropdownOpen = !dropdownOpen"
                type="button"
                class="flex flex-col items-center gap-1 text-gray-500 hover:text-gray-900 transition"
              >
                <div
                  v-if="!authStore.user?.profile_pic"
                  class="h-6 w-6 rounded-full bg-violet-100 flex items-center justify-center text-violet-600 text-xs font-semibold"
                >
                  {{ userInitial }}
                </div>
                <img
                  v-else
                  class="h-6 w-6 rounded-full object-cover border border-gray-200"
                  :src="authStore.user.profile_pic"
                  alt="Profile picture"
                />
                <span class="text-[11px] font-medium max-w-[100px] truncate">{{
                  authStore.user?.email
                }}</span>
              </button>

              <!-- Dropdown Menu -->
              <div
                v-show="dropdownOpen"
                class="absolute right-0 mt-3 w-52 rounded-2xl border border-gray-100 bg-white shadow-lg shadow-gray-200/60"
              >
                <router-link
                  to="/profile"
                  class="flex items-center gap-3 px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 transition"
                >
                  <svg
                    class="h-4 w-4 text-[#8338ec]"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                    />
                  </svg>
                  <span>My Tickets &amp; Events</span>
                </router-link>
                <router-link
                  to="/2fa/settings"
                  class="flex items-center gap-3 px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 transition"
                >
                  <svg
                    class="h-4 w-4 text-[#8338ec]"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                    />
                  </svg>
                  <span>Security &amp; 2FA</span>
                </router-link>
                <div class="border-t border-gray-100"></div>
                <button
                  @click="handleLogout"
                  class="flex items-center gap-3 px-4 py-3 text-sm text-rose-500 hover:bg-rose-50 transition w-full text-left"
                >
                  <svg
                    class="h-4 w-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                    />
                  </svg>
                  <span>Log out</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Mobile menu button (authenticated) -->
          <div class="md:hidden flex items-center">
            <button
              @click="mobileMenuOpen = !mobileMenuOpen"
              type="button"
              class="inline-flex h-10 w-10 items-center justify-center text-gray-700 hover:text-gray-900 focus:outline-hidden"
            >
              <span class="sr-only">Open navigation</span>
              <svg
                class="h-5 w-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>
          </div>
        </template>

        <!-- ============================================================ -->
        <!-- GUEST: Landing page nav + auth buttons                        -->
        <!-- ============================================================ -->
        <template v-else-if="!hideNav">
          <!-- Desktop Navigation -->
          <div
            class="hidden lg:flex items-center gap-6 text-sm font-medium text-gray-600"
          >
            <router-link to="/events" class="hover:text-gray-900 transition"
              >Browse Events</router-link
            >
            <a href="#features" class="hover:text-gray-900 transition"
              >How It Works</a
            >
            <a href="#pricing" class="hover:text-gray-900 transition"
              >Pricing</a
            >
          </div>

          <!-- Desktop Auth -->
          <div class="hidden md:flex items-center gap-3">
            <router-link
              to="/login"
              class="text-sm font-medium text-gray-600 hover:text-gray-900 transition"
            >
              Log In
            </router-link>
            <router-link to="/signup" class="btn-primary">
              Join Tikepam
              <svg
                class="h-4 w-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M14 5l7 7m0 0l-7 7m7-7H3"
                />
              </svg>
            </router-link>
          </div>

          <!-- Mobile Menu Button (guest) -->
          <div class="md:hidden flex items-center">
            <button
              @click="mobileMenuOpen = !mobileMenuOpen"
              type="button"
              class="inline-flex h-10 w-10 items-center justify-center text-gray-700 hover:text-gray-900 focus:outline-hidden"
            >
              <span class="sr-only">Open navigation</span>
              <svg
                class="h-5 w-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>
          </div>
        </template>
      </div>

      <!-- ============================================================ -->
      <!-- MOBILE MENU                                                    -->
      <!-- ============================================================ -->
      <div v-if="!hideNav && mobileMenuOpen" class="md:hidden pb-6">
        <div
          class="space-y-4 rounded-3xl border border-gray-200 bg-white p-6 shadow-lg shadow-gray-200/60"
        >
          <!-- Authenticated mobile menu -->
          <template v-if="authStore.isAuthenticated">
            <nav class="space-y-1 text-sm font-medium text-gray-600">
              <router-link
                to="/events"
                class="flex items-center gap-3 rounded-2xl px-4 py-3 hover:bg-gray-50 transition"
              >
                <svg
                  class="h-5 w-5 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="1.5"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
                Browse Events
              </router-link>
              <router-link
                to="/create-event"
                class="flex items-center gap-3 rounded-2xl px-4 py-3 hover:bg-gray-50 transition"
              >
                <svg
                  class="h-5 w-5 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="1.5"
                    d="M12 4v16m8-8H4"
                  />
                </svg>
                Create Event
              </router-link>
              <router-link
                to="/favorites"
                class="flex items-center gap-3 rounded-2xl px-4 py-3 hover:bg-gray-50 transition"
              >
                <svg
                  class="h-5 w-5 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="1.5"
                    d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                  />
                </svg>
                Favorites
              </router-link>
              <router-link
                to="/my-tickets"
                class="flex items-center gap-3 rounded-2xl px-4 py-3 hover:bg-gray-50 transition"
              >
                <svg
                  class="h-5 w-5 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="1.5"
                    d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"
                  />
                </svg>
                Tickets
              </router-link>
            </nav>
            <div class="border-t border-gray-100 pt-4 space-y-2">
              <router-link
                to="/profile"
                class="block rounded-full bg-gray-100 px-4 py-3 text-sm font-semibold text-gray-700 text-center hover:bg-gray-200 transition"
              >
                My Tickets &amp; Events
              </router-link>
              <button
                @click="handleLogout"
                class="block rounded-full bg-rose-50 px-4 py-3 text-sm font-semibold text-rose-500 text-center hover:bg-rose-100 transition w-full"
              >
                Log out
              </button>
            </div>
          </template>

          <!-- Guest mobile menu -->
          <template v-else>
            <nav class="space-y-2 text-sm font-medium text-gray-600">
              <router-link
                to="/events"
                class="block rounded-2xl px-4 py-3 hover:bg-gray-50 transition"
                >Browse Events</router-link
              >
              <a
                href="#features"
                class="block rounded-2xl px-4 py-3 hover:bg-gray-50 transition"
                >How It Works</a
              >
              <a
                href="#pricing"
                class="block rounded-2xl px-4 py-3 hover:bg-gray-50 transition"
                >Pricing</a
              >
            </nav>
            <div class="border-t border-gray-100 pt-4">
              <div class="flex flex-col gap-2">
                <router-link
                  to="/login"
                  class="rounded-full border border-gray-200 px-4 py-3 text-sm font-semibold text-gray-600 text-center hover:border-[#8338ec]/40 transition"
                >
                  Log In
                </router-link>
                <router-link to="/signup" class="btn-primary text-center">
                  Join Tikepam
                </router-link>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const dropdownOpen = ref(false);
const mobileMenuOpen = ref(false);
const dropdownRef = ref(null);

// Hide navigation on auth pages
const hideNav = computed(() => {
  return ["login", "signup", "twofa-verify", "sso-callback"].includes(
    route.name,
  );
});

// User initial for avatar
const userInitial = computed(() => {
  if (authStore.user?.email) {
    return authStore.user.email[0].toUpperCase();
  }
  return "U";
});

// Click away listener for dropdown
function handleClickOutside(event) {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    dropdownOpen.value = false;
  }
}

async function handleLogout() {
  await authStore.logout();
  dropdownOpen.value = false;
  mobileMenuOpen.value = false;
  router.push("/login");
}

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});
</script>
