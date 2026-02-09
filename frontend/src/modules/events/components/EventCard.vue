<script setup>
import { computed } from "vue";
import { RouterLink } from "vue-router";
import { useEventsStore } from "@/stores/events";

const props = defineProps({
  event: {
    type: Object,
    required: true,
  },
});

const eventsStore = useEventsStore();

// Format date nicely
const formattedDate = computed(() => {
  if (!props.event.start_date) return "";
  const date = new Date(props.event.start_date);
  const formatted = date.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
  });
  const time = date.toLocaleTimeString("en-US", {
    hour: "numeric",
    minute: "2-digit",
  });
  return `${formatted} • ${time}`;
});

// Get lowest price from ticket tiers
const lowestPrice = computed(() => {
  if (!props.event.ticket_tiers?.length) return null;
  const prices = props.event.ticket_tiers.map((t) => t.price);
  const min = Math.min(...prices);
  return min === 0 ? "Free Entry" : `From $${(min / 100).toFixed(0)}`;
});

// Placeholder image based on category
const eventImage = computed(() => {
  if (props.event.cover_image) return props.event.cover_image;
  // Use picsum with a seed based on event id for consistent images
  const seed = props.event.id || Math.random() * 1000;
  return `https://picsum.photos/seed/${seed}/800/400`;
});

// Generate gradient colors based on category for placeholder
const gradientColors = computed(() => {
  const gradients = {
    music: ["#8338ec", "#ff006e"],
    nightlife: ["#8338ec", "#ff006e"],
    food: ["#ffbe0b", "#fb5607"],
    festival: ["#fb5607", "#ff006e"],
    community: ["#3a86ff", "#8338ec"],
    culture: ["#3a86ff", "#8338ec"],
    art: ["#ff006e", "#8338ec"],
    dance: ["#8338ec", "#3a86ff"],
    sports: ["#10b981", "#3a86ff"],
    default: ["#8338ec", "#3a86ff"],
  };
  return gradients[props.event.category] || gradients.default;
});

// Category badge color
const categoryColor = computed(() => {
  const colors = {
    music: "bg-violet-500",
    nightlife: "bg-violet-500",
    food: "bg-amber-500",
    festival: "bg-orange-500",
    community: "bg-blue-500",
    culture: "bg-blue-500",
    art: "bg-rose-500",
    dance: "bg-purple-500",
    sports: "bg-green-500",
  };
  return colors[props.event.category] || "bg-violet-500";
});
</script>

<template>
  <RouterLink
    :to="{ name: 'event-detail', params: { slug: event.slug } }"
    class="group relative overflow-hidden rounded-3xl border border-gray-200 bg-white shadow-lg shadow-gray-200/50 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg block"
  >
    <!-- Event Image -->
    <div class="relative h-48 overflow-hidden">
      <div
        class="absolute inset-0"
        :style="{
          background: `linear-gradient(135deg, ${gradientColors[0]}, ${gradientColors[1]})`,
        }"
      >
        <img
          v-if="eventImage"
          :src="eventImage"
          :alt="event.title"
          class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
        />
      </div>

      <!-- Category Badge -->
      <span
        class="absolute left-4 top-4 inline-flex items-center gap-1.5 rounded-full bg-white/90 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-gray-700 backdrop-blur-sm"
      >
        <span class="h-2 w-2 rounded-full" :class="categoryColor"></span>
        {{ eventsStore.getCategoryLabel(event.category) }}
      </span>
    </div>

    <!-- Event Details -->
    <div class="p-5">
      <!-- Location -->
      <div class="mb-2 flex items-center gap-1.5 text-sm text-gray-500">
        <svg
          v-if="!event.is_online"
          class="h-4 w-4"
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
          class="h-4 w-4"
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
        {{ event.is_online ? "Online Event" : event.city }}
      </div>

      <!-- Title -->
      <h3 class="mb-2 text-lg font-semibold text-gray-900 line-clamp-2">
        {{ event.title }}
      </h3>

      <!-- Date -->
      <p class="mb-4 text-sm text-gray-600">
        {{ formattedDate }}
      </p>

      <!-- Price (no button) -->
      <div class="flex items-center justify-between">
        <span class="text-sm font-semibold text-gray-900">
          {{ lowestPrice || "See details" }}
        </span>
      </div>
    </div>
  </RouterLink>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
