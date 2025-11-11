<template>
  <div class="bg-white border-t border-gray-200 p-4">
    <div class="flex items-end space-x-2">
      <!-- Voice recording button -->
      <button
        @mousedown="startRecording"
        @mouseup="stopRecording"
        @mouseleave="stopRecording"
        @touchstart="startRecording"
        @touchend="stopRecording"
        :class="[
          'p-3 rounded-full transition-colors',
          isRecording
            ? 'bg-red-500 hover:bg-red-600 text-white'
            : 'bg-gray-200 hover:bg-gray-300 text-gray-700'
        ]"
        title="Удерживайте для записи"
      >
        <svg
          v-if="!isRecording"
          class="w-6 h-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
          />
        </svg>
        <svg
          v-else
          class="w-6 h-6 animate-pulse"
          fill="currentColor"
          viewBox="0 0 24 24"
        >
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z" />
        </svg>
      </button>

      <!-- Text input -->
      <div class="flex-1">
        <textarea
          v-model="message"
          @keydown.enter.exact.prevent="handleSend"
          @keydown.enter.shift.exact="message += '\n'"
          rows="1"
          placeholder="Введите сообщение..."
          class="input-field resize-none"
          style="min-height: 44px; max-height: 120px;"
        />
      </div>

      <!-- Send button -->
      <button
        @click="handleSend"
        :disabled="!message.trim() && !isRecording"
        class="btn-primary disabled:opacity-50 disabled:cursor-not-allowed p-3"
      >
        <svg
          class="w-6 h-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
          />
        </svg>
      </button>
    </div>

    <!-- Recording indicator -->
    <div v-if="isRecording" class="mt-2 flex items-center space-x-2 text-red-600">
      <div class="w-2 h-2 bg-red-600 rounded-full animate-pulse"></div>
      <span class="text-sm">Запись... {{ recordingTime }}с</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['send', 'send-audio'])

const message = ref('')
const isRecording = ref(false)
const mediaRecorder = ref(null)
const audioChunks = ref([])
const recordingTime = ref(0)
let recordingTimer = null

async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    audioChunks.value = []
    mediaRecorder.value = new MediaRecorder(stream)
    
    mediaRecorder.value.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.value.push(event.data)
      }
    }
    
    mediaRecorder.value.onstop = () => {
      const audioBlob = new Blob(audioChunks.value, { type: 'audio/webm' })
      emit('send-audio', audioBlob)
      stream.getTracks().forEach(track => track.stop())
    }
    
    mediaRecorder.value.start()
    isRecording.value = true
    recordingTime.value = 0
    
    recordingTimer = setInterval(() => {
      recordingTime.value++
    }, 1000)
  } catch (error) {
    console.error('Error accessing microphone:', error)
    alert('Не удалось получить доступ к микрофону')
  }
}

function stopRecording() {
  if (isRecording.value && mediaRecorder.value && mediaRecorder.value.state !== 'inactive') {
    mediaRecorder.value.stop()
    isRecording.value = false
    if (recordingTimer) {
      clearInterval(recordingTimer)
      recordingTimer = null
    }
    recordingTime.value = 0
  }
}

function handleSend() {
  if (message.value.trim()) {
    emit('send', message.value.trim())
    message.value = ''
  }
}
</script>

