<template>
  <div class="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50">
    <div v-if="messages.length === 0" class="text-center text-gray-500 py-12">
      <p>Пока нет сообщений. Начните общение!</p>
    </div>
    <MessageItem
      v-for="message in messages"
      :key="message.id"
      :message="message"
      :is-own="message.sender_id === currentUserId"
    />
    <div ref="messagesEnd"></div>
  </div>
</template>

<script setup>
import { watch, nextTick, onMounted, ref } from 'vue'
import MessageItem from './MessageItem.vue'

const props = defineProps({
  messages: {
    type: Array,
    required: true,
  },
  currentUserId: {
    type: Number,
    required: true,
  },
})

const messagesEnd = ref(null)

function scrollToBottom() {
  nextTick(() => {
    if (messagesEnd.value) {
      messagesEnd.value.scrollIntoView({ behavior: 'smooth' })
    }
  })
}

watch(() => props.messages.length, () => {
  scrollToBottom()
})

onMounted(() => {
  scrollToBottom()
})
</script>

