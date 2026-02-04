<template>
  <section class="py-16 lg:py-20">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section Header -->
      <div class="text-center mb-12">
        <p class="text-xs uppercase tracking-[0.4em] text-gray-400 mb-3">Community Love</p>
        <h2 class="text-3xl font-semibold text-gray-900">What the Diaspora Says</h2>
      </div>

      <!-- Testimonials Grid -->
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <article
          v-for="testimonial in testimonials"
          :key="testimonial.author"
          class="rounded-3xl border border-gray-200 bg-white p-6 lg:p-8 shadow-md shadow-gray-200/50"
        >
          <!-- Quote Icon -->
          <div class="mb-4">
            <svg class="h-8 w-8 text-violet-200" fill="currentColor" viewBox="0 0 24 24">
              <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z" />
            </svg>
          </div>

          <!-- Quote -->
          <blockquote class="text-gray-700 mb-6 leading-relaxed">
            "{{ testimonial.quote }}"
          </blockquote>

          <!-- Author -->
          <div class="flex items-center gap-4">
            <!-- Avatar Placeholder -->
            <div
              class="h-12 w-12 rounded-full flex items-center justify-center text-white font-semibold"
              :style="{ background: `linear-gradient(135deg, ${testimonial.gradient[0]}, ${testimonial.gradient[1]})` }"
            >
              {{ testimonial.initials }}
            </div>
            <div>
              <p class="font-semibold text-gray-900">{{ testimonial.author }}</p>
              <p class="text-sm text-gray-500">{{ testimonial.role }} • {{ testimonial.location }}</p>
            </div>
          </div>

          <!-- Star Rating -->
          <div class="flex gap-1 mt-4">
            <svg v-for="n in 5" :key="n" class="h-4 w-4 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup>
const testimonials = [
  {
    quote: 'Tikepam made finding authentic Haitian events so easy. No more fake promoters or surprise fees—just real vibes and real culture!',
    author: 'Marie J.',
    initials: 'MJ',
    role: 'Event Attendee',
    location: 'Brooklyn, NY',
    gradient: ['#8338ec', '#ff006e']
  },
  {
    quote: 'As an organizer, I sold out my Kompa night in 3 days. The dashboard is incredible—real-time sales, easy check-ins, and fast payouts.',
    author: 'DJ Flex',
    initials: 'DF',
    role: 'Event Organizer',
    location: 'Miami, FL',
    gradient: ['#fb5607', '#ffbe0b']
  },
  {
    quote: 'Finally a platform that understands our culture! The QR tickets made check-in smooth, and my crew loved how easy it was to buy together.',
    author: 'Jean-Pierre L.',
    initials: 'JL',
    role: 'Regular Attendee',
    location: 'Montreal, CA',
    gradient: ['#3a86ff', '#8338ec']
  }
]
</script>
