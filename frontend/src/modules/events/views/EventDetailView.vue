<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useEventsStore } from "@/stores/events";
import { useAuthStore } from "@/stores/auth";
import TicketSelector from "../components/TicketSelector.vue";
import api from "@/services/api";

const route = useRoute();
const router = useRouter();
const eventsStore = useEventsStore();
const authStore = useAuthStore();

const checkoutLoading = ref(false);
const checkoutError = ref(null);
const showTicketModal = ref(false);

onMounted(() => {
  eventsStore.fetchEvent(route.params.slug);
});

const event = computed(() => eventsStore.currentEvent);

// Format dates
const formattedDate = computed(() => {
  if (!event.value?.start_date) return "";
  const date = new Date(event.value.start_date);
  return date.toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric",
  });
});

const formattedTime = computed(() => {
  if (!event.value?.start_date) return "";
  const start = new Date(event.value.start_date);
  let time = start.toLocaleTimeString("en-US", {
    hour: "numeric",
    minute: "2-digit",
  });

  if (event.value.end_date) {
    const end = new Date(event.value.end_date);
    time +=
      " - " +
      end.toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
      });
  }

  return time;
});

// Event image
const eventImage = computed(() => {
  if (event.value?.cover_image) return event.value.cover_image;
  const seed = event.value?.id || "default";
  return `https://picsum.photos/seed/${seed}/1200/600`;
});

async function handleCheckout(items) {
  if (!authStore.isAuthenticated) {
    // Redirect to login
    router.push({ name: "login", query: { redirect: route.fullPath } });
    return;
  }

  checkoutLoading.value = true;
  checkoutError.value = null;

  try {
    const response = await api.post("/api/checkout/create-session", {
      event_id: event.value.id,
      items: items.map((item) => ({
        tier_id: item.tier_id,
        quantity: item.quantity,
      })),
    });

    if (response.data.success) {
      // Redirect to Stripe Checkout
      window.location.href = response.data.data.url;
    } else {
      checkoutError.value = response.data.message;
    }
  } catch (err) {
    checkoutError.value =
      err.response?.data?.message || "Failed to start checkout";
    console.error("Checkout error:", err);
  } finally {
    checkoutLoading.value = false;
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Loading State -->
    <div v-if="eventsStore.loading" class="animate-pulse">
      <div class="h-[400px] bg-gray-200"></div>
      <div class="max-w-7xl mx-auto px-4 py-8">
        <div class="h-8 bg-gray-200 rounded w-2/3 mb-4"></div>
        <div class="h-4 bg-gray-200 rounded w-1/3 mb-8"></div>
        <div class="grid lg:grid-cols-3 gap-8">
          <div class="lg:col-span-2 space-y-4">
            <div class="h-4 bg-gray-200 rounded w-full"></div>
            <div class="h-4 bg-gray-200 rounded w-full"></div>
            <div class="h-4 bg-gray-200 rounded w-3/4"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div
      v-else-if="eventsStore.error"
      class="max-w-7xl mx-auto px-4 py-16 text-center"
    >
      <div class="text-6xl mb-4">😕</div>
      <h2 class="text-xl font-bold text-gray-900 mb-2">Event not found</h2>
      <p class="text-gray-600 mb-6">{{ eventsStore.error }}</p>
      <RouterLink to="/events" class="btn-primary"> Browse Events </RouterLink>
    </div>

    <!-- Event Content -->
    <div v-else-if="event">
      <!-- Hero Image -->
      <div class="relative h-[300px] sm:h-[400px] lg:h-[500px]">
        <img
          :src="eventImage"
          :alt="event.title"
          class="w-full h-full object-cover"
        />
        <div
          class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent"
        ></div>

        <!-- Back Button -->
        <RouterLink
          to="/events"
          class="absolute top-4 left-4 p-2 bg-white/90 backdrop-blur-sm rounded-full hover:bg-white transition-colors"
        >
          <svg
            class="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 19l-7-7 7-7"
            />
          </svg>
        </RouterLink>

        <!-- Category & Featured Badges -->
        <div class="absolute top-4 right-4 flex gap-2">
          <span
            class="px-4 py-2 bg-white/90 backdrop-blur-sm rounded-full text-sm font-medium"
          >
            {{ eventsStore.getCategoryLabel(event.category) }}
          </span>
          <span
            v-if="event.is_featured"
            class="px-4 py-2 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-full text-sm font-bold"
          >
            Featured
          </span>
        </div>

        <!-- Share & Save Buttons (Bottom Right) -->
        <div
          class="absolute bottom-4 right-4 sm:bottom-6 sm:right-6 lg:bottom-8 lg:right-8 flex gap-2"
        >
          <!-- Share Button (UI only for now) -->
          <button
            class="p-2 sm:p-2.5 bg-white/90 backdrop-blur-sm rounded-full hover:bg-white transition-colors shadow-lg"
            title="Share event"
          >
            <svg
              class="w-5 h-5 sm:w-6 sm:h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"
              />
            </svg>
          </button>

          <!-- Save Button (UI only for now) -->
          <button
            class="p-2 sm:p-2.5 bg-white/90 backdrop-blur-sm rounded-full hover:bg-white transition-colors shadow-lg"
            title="Save event"
          >
            <svg
              class="w-5 h-5 sm:w-6 sm:h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Content -->
      <div class="max-w-7xl mx-auto px-4 py-16">
        <div class="grid lg:grid-cols-3 gap-8">
          <!-- Main Content -->
          <div class="lg:col-span-2 space-y-8">
            <!-- Title and Organizer -->
            <div>
              <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-3">
                {{ event.title }}
              </h1>
              <p class="text-gray-600 italic text-base sm:text-lg">
                by {{ event.organizer?.fullname || "Event Organizer" }}
              </p>
            </div>

            <!-- Date & Time and Location -->
            <div
              class="grid sm:grid-cols-2 gap-6 pb-12 border-b border-gray-200"
            >
              <!-- Date & Time -->
              <div class="flex items-start gap-3">
                <svg
                  class="w-6 h-6 text-gray-700 flex-shrink-0 mt-1"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
                <div>
                  <p class="font-semibold text-gray-900">{{ formattedDate }}</p>
                  <p class="text-gray-600">{{ formattedTime }}</p>
                </div>
              </div>

              <!-- Location -->
              <div class="flex items-start gap-3">
                <svg
                  v-if="!event.is_online"
                  class="w-6 h-6 text-gray-700 flex-shrink-0 mt-1"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                </svg>
                <svg
                  v-else
                  class="w-6 h-6 text-gray-700 flex-shrink-0 mt-1"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
                  />
                </svg>
                <div>
                  <p class="font-semibold text-gray-900">
                    {{ event.is_online ? "Online Event" : event.venue_name }}
                  </p>
                  <p class="text-gray-600">
                    {{
                      event.is_online
                        ? "Join from anywhere"
                        : event.venue_address || event.city
                    }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Description -->
            <div class="py-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                About This Event
              </h2>
              <div class="prose prose-gray max-w-none">
                <p
                  v-if="event.description"
                  class="text-gray-700 whitespace-pre-wrap"
                >
                  {{ event.description }}
                </p>
                <p v-else class="text-gray-500 italic">
                  No description provided.
                </p>
              </div>
            </div>

            <!-- Event Information Section -->
            <div class="py-8 border-t border-gray-200">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                Event Information
              </h2>
              <div class="grid sm:grid-cols-2 gap-6">
                <!-- Highlights -->
                <div>
                  <h3 class="font-semibold text-gray-900 mb-3">Highlights</h3>
                  <div class="space-y-2">
                    <div class="flex items-center gap-2 text-gray-600">
                      <svg
                        class="w-4 h-4"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fill-rule="evenodd"
                          d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                          clip-rule="evenodd"
                        />
                      </svg>
                      <span>{{
                        event.is_online ? "Online event" : "In-person event"
                      }}</span>
                    </div>
                    <div
                      v-if="!event.is_online"
                      class="flex items-center gap-2 text-gray-600"
                    >
                      <svg
                        class="w-4 h-4"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fill-rule="evenodd"
                          d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                          clip-rule="evenodd"
                        />
                      </svg>
                      <span>Venue access included</span>
                    </div>
                    <div class="flex items-center gap-2 text-gray-600">
                      <svg
                        class="w-4 h-4"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fill-rule="evenodd"
                          d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                          clip-rule="evenodd"
                        />
                      </svg>
                      <span>Mobile tickets accepted</span>
                    </div>
                  </div>
                </div>

                <!-- Refund Policy -->
                <div>
                  <h3 class="font-semibold text-gray-900 mb-3">
                    Refund Policy
                  </h3>
                  <p class="text-gray-600">No refunds</p>
                  <p class="text-sm text-gray-500 mt-2">
                    Contact the organizer for more details
                  </p>
                </div>
              </div>
            </div>

            <!-- Location Map (for in-person events) -->
            <div v-if="!event.is_online" class="py-8 border-t border-gray-200">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">Location</h2>
              <div class="space-y-4">
                <div>
                  <p class="font-semibold text-gray-900">
                    {{ event.venue_name }}
                  </p>
                  <p class="text-gray-600">{{ event.venue_address }}</p>
                  <p v-if="event.city" class="text-gray-600">
                    {{ event.city }}
                  </p>
                </div>

                <!-- Map Embed -->
                <div class="rounded-lg overflow-hidden border border-gray-200 h-64 sm:h-80 lg:h-96">
                  <iframe
                    :src="`https://maps.google.com/maps?q=${encodeURIComponent(event.venue_name + ', ' + event.venue_address)}&output=embed`"
                    width="100%"
                    height="100%"
                    style="border: 0"
                    loading="lazy"
                  ></iframe>
                </div>
              </div>
            </div>

            <!-- Organizer Section -->
            <div class="py-8 border-t border-gray-200">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">Organizer</h2>
              <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
                <div class="flex items-center gap-4">
                  <div
                    class="w-14 h-14 sm:w-16 sm:h-16 bg-gradient-to-br from-violet-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xl sm:text-2xl flex-shrink-0"
                  >
                    {{ (event.organizer?.fullname || "O")[0].toUpperCase() }}
                  </div>
                  <div>
                    <p class="font-bold text-gray-900 text-base sm:text-lg">
                      {{ event.organizer?.fullname || "Event Organizer" }}
                    </p>
                    <p class="text-gray-600 text-sm sm:text-base">Event Organizer</p>
                  </div>
                </div>
                <button
                  class="w-full sm:w-auto px-4 py-2.5 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors font-medium text-gray-700"
                >
                  Contact
                </button>
              </div>
            </div>

            <!-- Bottom CTA (Mobile) -->
            <div class="lg:hidden pt-8 border-t border-gray-200 text-center">
              <button
                @click="showTicketModal = true"
                class="btn-primary w-full justify-center"
              >
                Get Tickets
              </button>
            </div>
          </div>

          <!-- Sidebar - Ticket Selector (Desktop Only) -->
          <div class="hidden lg:block lg:col-span-1">
            <div class="sticky top-24">
              <!-- Checkout Error -->
              <div
                v-if="checkoutError"
                class="mb-4 p-4 bg-red-50 border border-red-300 rounded-xl text-red-800"
              >
                {{ checkoutError }}
              </div>

              <!-- Loading Overlay -->
              <div v-if="checkoutLoading" class="relative">
                <div
                  class="absolute inset-0 bg-white/80 backdrop-blur-sm rounded-2xl flex items-center justify-center z-10"
                >
                  <div class="flex items-center gap-3">
                    <svg
                      class="animate-spin w-6 h-6 text-violet-600"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        class="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        stroke-width="4"
                      ></circle>
                      <path
                        class="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                      ></path>
                    </svg>
                    <span class="font-medium text-gray-900"
                      >Preparing checkout...</span
                    >
                  </div>
                </div>
              </div>

              <TicketSelector
                v-if="event.ticket_tiers?.length"
                :tiers="event.ticket_tiers"
                @checkout="handleCheckout"
              />

              <!-- No Tickets Available -->
              <div
                v-else
                class="bg-white rounded-2xl shadow-lg p-6 text-center"
              >
                <div class="text-4xl mb-3">🎟️</div>
                <p class="text-gray-600">Tickets coming soon</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Mobile Ticket Modal -->
      <Teleport to="body">
        <Transition
          enter-active-class="transition-opacity duration-200"
          enter-from-class="opacity-0"
          enter-to-class="opacity-100"
          leave-active-class="transition-opacity duration-200"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <div
            v-if="showTicketModal"
            class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 lg:hidden"
            @click="showTicketModal = false"
          >
            <div class="fixed inset-x-0 bottom-0 max-h-[85vh] overflow-y-auto">
              <Transition
                enter-active-class="transition-transform duration-300"
                enter-from-class="translate-y-full"
                enter-to-class="translate-y-0"
                leave-active-class="transition-transform duration-300"
                leave-from-class="translate-y-0"
                leave-to-class="translate-y-full"
              >
                <div
                  v-if="showTicketModal"
                  @click.stop
                  class="bg-white rounded-t-3xl shadow-2xl"
                >
                  <!-- Modal Header -->
                  <div class="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 rounded-t-3xl z-10">
                    <div class="flex items-center justify-between">
                      <h3 class="text-xl font-bold text-gray-900">Select Tickets</h3>
                      <button
                        @click="showTicketModal = false"
                        class="p-2 hover:bg-gray-100 rounded-full transition-colors"
                      >
                        <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                  </div>

                  <!-- Modal Content -->
                  <div class="px-6 py-6">
                    <!-- Checkout Error -->
                    <div
                      v-if="checkoutError"
                      class="mb-4 p-4 bg-red-50 border border-red-300 rounded-xl text-red-800"
                    >
                      {{ checkoutError }}
                    </div>

                    <!-- Loading Overlay -->
                    <div v-if="checkoutLoading" class="relative">
                      <div
                        class="absolute inset-0 bg-white/80 backdrop-blur-sm rounded-2xl flex items-center justify-center z-10"
                      >
                        <div class="flex items-center gap-3">
                          <svg
                            class="animate-spin w-6 h-6 text-violet-600"
                            fill="none"
                            viewBox="0 0 24 24"
                          >
                            <circle
                              class="opacity-25"
                              cx="12"
                              cy="12"
                              r="10"
                              stroke="currentColor"
                              stroke-width="4"
                            ></circle>
                            <path
                              class="opacity-75"
                              fill="currentColor"
                              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                            ></path>
                          </svg>
                          <span class="font-medium text-gray-900">Preparing checkout...</span>
                        </div>
                      </div>
                    </div>

                    <!-- Ticket Selector -->
                    <TicketSelector
                      v-if="event.ticket_tiers?.length"
                      :tiers="event.ticket_tiers"
                      @checkout="handleCheckout"
                    />

                    <!-- No Tickets Available -->
                    <div
                      v-else
                      class="bg-gray-50 rounded-2xl p-8 text-center"
                    >
                      <div class="text-4xl mb-3">🎟️</div>
                      <p class="text-gray-600">Tickets coming soon</p>
                    </div>
                  </div>
                </div>
              </Transition>
            </div>
          </div>
        </Transition>
      </Teleport>
    </div>
  </div>
</template>
