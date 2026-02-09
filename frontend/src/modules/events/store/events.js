import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useEventsStore = defineStore('events', () => {
  // State
  const events = ref([])
  const currentEvent = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const filters = ref({
    category: null,
    city: null,
    featured: false
  })

  // Categories
  const categories = [
    { value: 'music', label: 'Music' },
    { value: 'dance', label: 'Dance' },
    { value: 'food', label: 'Food & Drink' },
    { value: 'culture', label: 'Culture' },
    { value: 'festival', label: 'Festival' },
    { value: 'nightlife', label: 'Nightlife' },
    { value: 'community', label: 'Community' },
    { value: 'sports', label: 'Sports' },
    { value: 'art', label: 'Art & Theater' },
    { value: 'other', label: 'Other' }
  ]

  // Computed
  const featuredEvents = computed(() =>
    events.value.filter(e => e.is_featured)
  )

  const upcomingEvents = computed(() =>
    events.value.slice(0, 6)
  )

  // Actions
  async function fetchEvents() {
    loading.value = true
    error.value = null
    try {
      const params = new URLSearchParams()
      if (filters.value.category) params.append('category', filters.value.category)
      if (filters.value.city) params.append('city', filters.value.city)
      if (filters.value.featured) params.append('featured', 'true')

      const response = await api.get(`/api/events/?${params}`)
      events.value = response.data.data.events
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to load events'
      console.error('Failed to fetch events:', err)
    } finally {
      loading.value = false
    }
  }

  async function fetchEvent(slug) {
    loading.value = true
    error.value = null
    currentEvent.value = null
    try {
      const response = await api.get(`/api/events/${slug}`)
      currentEvent.value = response.data.data.event
      return currentEvent.value
    } catch (err) {
      error.value = err.response?.data?.message || 'Event not found'
      console.error('Failed to fetch event:', err)
      return null
    } finally {
      loading.value = false
    }
  }

  function setFilter(key, value) {
    filters.value[key] = value
  }

  function clearFilters() {
    filters.value = {
      category: null,
      city: null,
      featured: false
    }
  }

  function getCategoryLabel(value) {
    const cat = categories.find(c => c.value === value)
    return cat ? cat.label : value
  }

  function getCategoryIcon(value) {
    return null // Icons removed
  }

  return {
    // State
    events,
    currentEvent,
    loading,
    error,
    filters,
    categories,
    // Computed
    featuredEvents,
    upcomingEvents,
    // Actions
    fetchEvents,
    fetchEvent,
    setFilter,
    clearFilters,
    getCategoryLabel,
    getCategoryIcon
  }
})
