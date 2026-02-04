<template>
  <div class="py-12">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Welcome Header -->
      <div class="flex items-center gap-5 mb-10">
        <img
          v-if="user?.profile_pic"
          :src="user.profile_pic"
          alt="Profile picture"
          class="rounded-full w-16 h-16 object-cover border-2 border-violet-200"
        />
        <div
          v-else
          class="w-16 h-16 rounded-full bg-violet-100 flex items-center justify-center text-violet-600 text-2xl font-bold"
        >
          {{ userInitial }}
        </div>
        <div>
          <h1 class="text-2xl font-bold text-headline">Hey {{ displayName }}</h1>
          <p class="text-body mt-1">Here's what's coming up for you.</p>
        </div>
      </div>

      <!-- My Upcoming Tickets -->
      <section class="mb-8">
        <h2 class="text-lg font-semibold text-headline mb-4">My upcoming tickets</h2>
        <div class="card p-10">
          <div class="text-center py-6">
            <div class="w-16 h-16 bg-violet-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-violet-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" />
              </svg>
            </div>
            <h3 class="text-lg font-medium text-headline mb-2">No upcoming events yet</h3>
            <p class="text-muted text-sm mb-6 max-w-sm mx-auto">
              When you reserve a spot at an event, your tickets show up here.
            </p>
            <router-link to="/" class="btn-primary">
              Browse Events
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </router-link>
          </div>
        </div>
      </section>

      <!-- Recent Activity -->
      <section class="mb-8">
        <h2 class="text-lg font-semibold text-headline mb-4">Recent activity</h2>
        <div class="card p-8">
          <div class="text-center py-4">
            <div class="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-sm font-medium text-headline mb-1">No recent activity</h3>
            <p class="text-muted text-xs">Reservations, check-ins, and event history will appear here.</p>
          </div>
        </div>
      </section>

      <!-- Account Strip -->
      <div class="card px-6 py-4">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div class="flex items-center gap-4 text-sm">
            <span class="text-body">{{ user?.email }}</span>
            <span
              v-if="user?.twofa_enabled"
              class="inline-flex items-center gap-1 text-xs font-medium text-green-700 bg-green-50 border border-green-200 rounded-full px-2.5 py-0.5"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4" />
              </svg>
              2FA on
            </span>
            <span
              v-else
              class="inline-flex items-center gap-1 text-xs font-medium text-amber-700 bg-amber-50 border border-amber-200 rounded-full px-2.5 py-0.5"
            >
              2FA off
            </span>
          </div>
          <div class="flex items-center gap-4 text-sm">
            <router-link
              to="/2fa/settings"
              class="text-violet-500 hover:text-violet-600 font-medium"
            >
              Security center
            </router-link>
            <button
              @click="logout"
              class="text-gray-500 hover:text-gray-700"
            >
              Log out
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.user)

const userInitial = computed(() => {
  if (user.value?.email) {
    return user.value.email[0].toUpperCase()
  }
  return 'U'
})

const displayName = computed(() => {
  if (user.value?.fullname) return user.value.fullname
  if (user.value?.username) return user.value.username
  if (user.value?.email) return user.value.email.split('@')[0]
  return 'there'
})

async function logout() {
  await authStore.logout()
  router.push('/login')
}

onMounted(async () => {
  if (!authStore.user) {
    await authStore.checkSession()
  }
})
</script>
