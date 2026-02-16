<template>
  <div
    :class="[
      'relative flex flex-col items-center justify-center rounded-xl border-2 border-dashed p-6 transition-colors cursor-pointer',
      isDragging
        ? 'border-violet-400 bg-violet-50'
        : 'border-gray-200 bg-gray-50 hover:border-gray-300 hover:bg-gray-100'
    ]"
    @dragover.prevent="isDragging = true"
    @dragleave.prevent="isDragging = false"
    @drop.prevent="handleDrop"
    @click="openFileDialog"
  >
    <!-- Preview -->
    <template v-if="previewUrl">
      <img
        :src="previewUrl"
        alt="Preview"
        class="h-40 w-full rounded-lg object-cover"
      />
      <button
        class="mt-3 text-sm font-medium text-red-600 hover:text-red-700"
        @click.stop="clearImage"
      >
        Remove image
      </button>
    </template>

    <!-- Upload prompt -->
    <template v-else>
      <Upload :size="32" class="mb-2 text-gray-400" />
      <p class="text-sm font-medium text-gray-600">
        Drop an image here or <span class="text-violet-600">browse</span>
      </p>
      <p class="mt-1 text-xs text-gray-400">PNG, JPG up to 5MB</p>
    </template>

    <input
      ref="fileInput"
      type="file"
      accept="image/*"
      class="hidden"
      @change="handleFileSelect"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Upload } from 'lucide-vue-next'

const props = defineProps({
  modelValue: { type: [String, File], default: '' }
})

const emit = defineEmits(['update:modelValue'])

const fileInput = ref(null)
const isDragging = ref(false)
const localFile = ref(null)

const previewUrl = computed(() => {
  if (localFile.value) return URL.createObjectURL(localFile.value)
  if (typeof props.modelValue === 'string' && props.modelValue) return props.modelValue
  return ''
})

function openFileDialog() {
  if (!previewUrl.value) fileInput.value?.click()
}

function handleDrop(e) {
  isDragging.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file && file.type.startsWith('image/')) {
    setFile(file)
  }
}

function handleFileSelect(e) {
  const file = e.target.files?.[0]
  if (file) setFile(file)
}

function setFile(file) {
  localFile.value = file
  emit('update:modelValue', file)
}

function clearImage() {
  localFile.value = null
  emit('update:modelValue', '')
  if (fileInput.value) fileInput.value.value = ''
}
</script>
