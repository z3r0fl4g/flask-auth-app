<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <HeroSection />

    <!-- Featured Events Carousel -->
    <FeaturedEvents />

    <!-- How Tikepam Works -->
    <HowItWorks />

    <!-- Event Categories -->
    <EventCategories />

    <!-- Trust Signals / Why Tikepam -->
    <TrustSignals />

    <!-- Testimonials -->
    <Testimonials />

    <!-- Final CTA -->
    <FinalCTA />
  </div>
</template>

<script setup>
import HeroSection from '@/components/home/HeroSection.vue'
import FeaturedEvents from '@/components/home/FeaturedEvents.vue'
import HowItWorks from '@/components/home/HowItWorks.vue'
import EventCategories from '@/components/home/EventCategories.vue'
import TrustSignals from '@/components/home/TrustSignals.vue'
import Testimonials from '@/components/home/Testimonials.vue'
import FinalCTA from '@/components/home/FinalCTA.vue'
</script>
