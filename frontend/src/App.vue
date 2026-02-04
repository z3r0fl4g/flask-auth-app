<template>
  <div class="min-h-screen bg-background">
    <!-- Ambient glows per Tikepam design -->
    <div class="ambient-bg">
      <div class="glow glow-rose" style="width:42rem;height:42rem;top:-14rem;right:-18rem;"></div>
      <div class="glow glow-amber" style="width:38rem;height:38rem;bottom:-16rem;left:-12rem;"></div>
      <div class="glow glow-orange" style="width:30rem;height:30rem;top:40%;left:48%;transform:translateX(-48%);"></div>
    </div>

    <AppLayout>
      <router-view />
    </AppLayout>
  </div>
</template>

<script setup>
import AppLayout from '@/components/layout/AppLayout.vue'
</script>
