<template>
  <div
    class="flex"
    :class="isOwn ? 'justify-end' : 'justify-start'"
  >
    <div
      class="max-w-xs lg:max-w-md px-4 py-2 rounded-lg"
      :class="isOwn ? 'bg-primary-600 text-white' : 'bg-white text-gray-800 border border-gray-200'"
    >
      <div v-if="!isOwn" class="text-xs font-semibold mb-1 text-gray-600">
        {{ message.sender?.username || 'Пользователь' }}
      </div>
      
      <!-- Text message -->
      <div v-if="message.type === 'text'" class="break-words">
        {{ message.content }}
      </div>
      
      <!-- Audio message -->
      <div v-else-if="message.type === 'audio'" class="flex items-center space-x-2">
        <audio
          :src="getAudioUrl(message)"
          controls
          class="w-full h-8"
          :class="isOwn ? 'audio-white' : ''"
        />
      </div>
      
      <div class="text-xs mt-1 opacity-75">
        {{ formatTime(message.created_at) }}
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  message: {
    type: Object,
    required: true,
  },
  isOwn: {
    type: Boolean,
    default: false,
  },
})

function formatTime(dateString) {
  const date = new Date(dateString)
  return date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
}

function getAudioUrl(message) {
  if (message.audio_url) {
    return message.audio_url
  }
  if (message.audio) {
    // Если аудио пришло как base64
    return message.audio
  }
  return ''
}
</script>

<style scoped>
.audio-white ::v-deep(audio) {
  filter: invert(1);
}
</style>

