<template>
  <div class="flex flex-col min-h-screen">
    <Navbar />
    <main class="flex-grow">
      <slot />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Navbar from './Navbar.vue'
import Footer from './Footer.vue'
</script>
