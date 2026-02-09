<script setup>
import { onMounted, watch } from "vue";
import { useEventsStore } from "@/stores/events";
import EventCard from "../components/EventCard.vue";

const eventsStore = useEventsStore();

onMounted(() => {
  eventsStore.fetchEvents();
});

// Re-fetch when filters change
watch(
  () => eventsStore.filters,
  () => eventsStore.fetchEvents(),
  { deep: true },
);

function selectCategory(category) {
  if (eventsStore.filters.category === category) {
    eventsStore.setFilter("category", null);
  } else {
    eventsStore.setFilter("category", category);
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <div class="bg-gradient-to-r from-violet-500 via-rose-500 to-orange-500">
      <div class="max-w-7xl mx-auto px-4 py-16 sm:py-24">
        <h1 class="text-4xl sm:text-5xl font-bold text-white mb-4">
          Discover Events in Haiti
        </h1>
        <p class="text-xl text-purple-200 max-w-2xl">
          From vibrant music festivals to cultural celebrations, find your next
          unforgettable experience.
        </p>
      </div>
    </div>

    <!-- Category Filters -->
    <div class="sticky top-0 z-10 bg-white border-b shadow-sm">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex gap-2 py-4 overflow-x-auto scrollbar-hide">
          <button
            v-for="cat in eventsStore.categories"
            :key="cat.value"
            @click="selectCategory(cat.value)"
            :class="[
              'px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all border-2',
              eventsStore.filters.category === cat.value
                ? 'bg-white text-violet-600 border-violet-600'
                : 'bg-white text-gray-500 border-gray-200 hover:border-gray-300 hover:text-gray-600',
            ]"
          >
            {{ cat.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- Events Grid -->
    <div class="max-w-7xl mx-auto px-4 py-8">
      <!-- Loading State -->
      <div
        v-if="eventsStore.loading"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        <div
          v-for="i in 6"
          :key="i"
          class="bg-white rounded-2xl overflow-hidden shadow-sm animate-pulse"
        >
          <div class="aspect-[16/9] bg-gray-200"></div>
          <div class="p-4 space-y-3">
            <div class="h-4 bg-gray-200 rounded w-1/3"></div>
            <div class="h-6 bg-gray-200 rounded w-3/4"></div>
            <div class="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="eventsStore.error" class="text-center py-16">
        <div class="text-6xl mb-4">😕</div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">
          Something went wrong
        </h2>
        <p class="text-gray-600 mb-6">{{ eventsStore.error }}</p>
        <button @click="eventsStore.fetchEvents()" class="btn-primary">
          Try Again
        </button>
      </div>

      <!-- Empty State -->
      <div
        v-else-if="eventsStore.events.length === 0"
        class="text-center py-16"
      >
        <div class="text-6xl mb-4">🎭</div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">No events found</h2>
        <p class="text-gray-600 mb-6">
          {{
            eventsStore.filters.category
              ? `No ${eventsStore.getCategoryLabel(eventsStore.filters.category)} events right now.`
              : "Check back soon for upcoming events!"
          }}
        </p>
        <button
          v-if="eventsStore.filters.category"
          @click="eventsStore.clearFilters()"
          class="btn-secondary"
        >
          Clear Filters
        </button>
      </div>

      <!-- Events Grid -->
      <div v-else>
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-semibold text-gray-900">
            {{
              eventsStore.filters.category
                ? eventsStore.getCategoryLabel(eventsStore.filters.category) +
                  " Events"
                : "All Upcoming Events"
            }}
          </h2>
          <span class="text-sm text-gray-500">
            {{ eventsStore.events.length }} event{{
              eventsStore.events.length !== 1 ? "s" : ""
            }}
          </span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <EventCard
            v-for="event in eventsStore.events"
            :key="event.id"
            :event="event"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>
