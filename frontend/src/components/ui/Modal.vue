<template>
  <teleport to="body">
    <transition
      enter-active-class="transition duration-200 ease-out"
      leave-active-class="transition duration-150 ease-in"
      enter-from-class="opacity-0"
      leave-to-class="opacity-0"
    >
      <div
        v-if="modelValue"
        class="fixed inset-0 z-[60] flex items-center justify-center p-4"
      >
        <!-- Backdrop -->
        <div
          class="absolute inset-0 bg-gray-900/50"
          @click="$emit('update:modelValue', false)"
        />

        <!-- Modal panel -->
        <transition
          enter-active-class="transition duration-200 ease-out"
          leave-active-class="transition duration-150 ease-in"
          enter-from-class="opacity-0 scale-95"
          leave-to-class="opacity-0 scale-95"
        >
          <div
            v-if="modelValue"
            :class="[
              'relative w-full rounded-2xl bg-white shadow-xl',
              sizeClass
            ]"
          >
            <!-- Header -->
            <div v-if="title || $slots.header" class="flex items-center justify-between border-b border-gray-100 px-6 py-4">
              <slot name="header">
                <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
              </slot>
              <button
                class="flex h-8 w-8 items-center justify-center rounded-full text-gray-400 hover:bg-gray-100 hover:text-gray-600 transition-colors"
                @click="$emit('update:modelValue', false)"
              >
                <X :size="18" />
              </button>
            </div>

            <!-- Body -->
            <div class="px-6 py-4">
              <slot />
            </div>

            <!-- Footer -->
            <div v-if="$slots.footer" class="flex items-center justify-end gap-3 border-t border-gray-100 px-6 py-4">
              <slot name="footer" />
            </div>
          </div>
        </transition>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { computed } from 'vue'
import { X } from 'lucide-vue-next'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  title: { type: String, default: '' },
  size: { type: String, default: 'md' }
})

defineEmits(['update:modelValue'])

const sizeClass = computed(() => {
  const map = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl'
  }
  return map[props.size] || map.md
})
</script>
