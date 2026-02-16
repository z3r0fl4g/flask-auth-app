<template>
  <div class="relative">
    <input
      ref="inputRef"
      :value="modelValue"
      :placeholder="placeholder"
      class="input pr-10"
      readonly
    />
    <Calendar
      :size="18"
      class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import flatpickr from 'flatpickr'
import 'flatpickr/dist/flatpickr.min.css'
import { Calendar } from 'lucide-vue-next'

const props = defineProps({
  modelValue: { type: String, default: '' },
  placeholder: { type: String, default: 'Select date' },
  enableTime: { type: Boolean, default: false },
  minDate: { type: String, default: '' },
  maxDate: { type: String, default: '' }
})

const emit = defineEmits(['update:modelValue'])

const inputRef = ref(null)
let fp = null

onMounted(() => {
  fp = flatpickr(inputRef.value, {
    enableTime: props.enableTime,
    dateFormat: props.enableTime ? 'Y-m-d H:i' : 'Y-m-d',
    minDate: props.minDate || undefined,
    maxDate: props.maxDate || undefined,
    defaultDate: props.modelValue || undefined,
    onChange(selectedDates, dateStr) {
      emit('update:modelValue', dateStr)
    }
  })
})

watch(() => props.minDate, (val) => { if (fp) fp.set('minDate', val || undefined) })
watch(() => props.maxDate, (val) => { if (fp) fp.set('maxDate', val || undefined) })

onUnmounted(() => { if (fp) fp.destroy() })
</script>
