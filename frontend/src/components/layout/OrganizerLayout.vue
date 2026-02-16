<template>
  <div class="flex h-screen overflow-hidden bg-gray-50">
    <!-- Backdrop for mobile sidebar -->
    <Backdrop />

    <!-- Sidebar -->
    <OrganizerSidebar />

    <!-- Main content area -->
    <div class="flex flex-1 flex-col overflow-hidden">
      <!-- Header -->
      <OrganizerHeader />

      <!-- Page content -->
      <main class="flex-1 overflow-y-auto p-4 sm:p-6">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import OrganizerSidebar from './OrganizerSidebar.vue'
import OrganizerHeader from './OrganizerHeader.vue'
import Backdrop from './Backdrop.vue'
</script>
