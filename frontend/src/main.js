import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { clerkPlugin } from '@clerk/vue'
import VueApexCharts from 'vue3-apexcharts'
import App from './App.vue'
import router from './router'
import './assets/style.css'
import 'vue-sonner/style.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(VueApexCharts)

// Initialize Clerk
app.use(clerkPlugin, {
  publishableKey: import.meta.env.VITE_CLERK_PUBLISHABLE_KEY
})

app.mount('#app')
