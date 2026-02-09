export const eventsRoutes = [
  {
    path: '/events',
    name: 'events',
    component: () => import('../views/EventsListView.vue'),
    meta: { title: 'Events' }
  },
  {
    path: '/events/:slug',
    name: 'event-detail',
    component: () => import('../views/EventDetailView.vue'),
    meta: { title: 'Event Details' }
  },
  {
    path: '/checkout/success',
    name: 'checkout-success',
    component: () => import('../views/CheckoutSuccessView.vue'),
    meta: { title: 'Order Confirmed' }
  },
  {
    path: '/my-tickets',
    name: 'my-tickets',
    component: () => import('../views/MyTicketsView.vue'),
    meta: { requiresAuth: true, title: 'My Tickets' }
  },
  {
    path: '/create-event',
    name: 'create-event',
    component: () => import('../views/CreateEventView.vue'),
    meta: { requiresAuth: true, title: 'Create Event' }
  },
  {
    path: '/my-events',
    name: 'my-events',
    component: () => import('../views/MyEventsView.vue'),
    meta: { requiresAuth: true, title: 'My Events' }
  },
  {
    path: '/check-in',
    name: 'check-in',
    component: () => import('../views/CheckInView.vue'),
    meta: { requiresAuth: true, title: 'Check-In' }
  }
]
