<template>
  <div class="flex justify-between">
    <input
      v-for="index in length"
      :key="index"
      :ref="el => inputRefs[index - 1] = el"
      v-model="digits[index - 1]"
      type="text"
      inputmode="numeric"
      maxlength="1"
      pattern="[0-9]"
      class="flex-1 max-w-[3.25rem] h-14 text-center text-2xl font-semibold rounded-xl border-2 border-gray-200 bg-white focus:border-violet-500 focus:ring-4 focus:ring-violet-500/20 outline-none transition-all"
      :class="{ 'border-red-500': error }"
      @input="handleInput(index - 1, $event)"
      @keydown="handleKeydown(index - 1, $event)"
      @paste="handlePaste"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  length: {
    type: Number,
    default: 6
  },
  error: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['complete', 'update:modelValue'])

const digits = ref(Array(props.length).fill(''))
const inputRefs = ref([])

function handleInput(index, event) {
  const value = event.target.value

  // Only allow digits
  if (!/^\d*$/.test(value)) {
    digits.value[index] = ''
    return
  }

  digits.value[index] = value

  // Auto-focus next input
  if (value && index < props.length - 1) {
    inputRefs.value[index + 1]?.focus()
  }

  // Check if complete
  const code = digits.value.join('')
  if (digits.value.every(d => d !== '')) {
    emit('complete', code)
    emit('update:modelValue', code)
  }
}

function handleKeydown(index, event) {
  // Handle backspace - focus previous input if current is empty
  if (event.key === 'Backspace' && !digits.value[index] && index > 0) {
    inputRefs.value[index - 1]?.focus()
  }
}

function handlePaste(event) {
  event.preventDefault()
  const pastedData = event.clipboardData.getData('text').replace(/\D/g, '').slice(0, props.length)

  pastedData.split('').forEach((digit, index) => {
    if (index < props.length) {
      digits.value[index] = digit
    }
  })

  // Focus last filled input
  const lastIndex = Math.min(pastedData.length - 1, props.length - 1)
  if (lastIndex >= 0) {
    inputRefs.value[lastIndex]?.focus()
  }

  // Check if complete
  if (digits.value.every(d => d !== '')) {
    const code = digits.value.join('')
    emit('complete', code)
    emit('update:modelValue', code)
  }
}

// Reset on error
watch(() => props.error, (newError) => {
  if (newError) {
    digits.value = Array(props.length).fill('')
    inputRefs.value[0]?.focus()
  }
})

// Expose method to reset digits
defineExpose({
  reset() {
    digits.value = Array(props.length).fill('')
    inputRefs.value[0]?.focus()
  }
})
</script>
