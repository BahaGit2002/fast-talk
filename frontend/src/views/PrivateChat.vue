<template>
  <div class="flex-1 flex flex-col bg-white">
    <ChatHeader
      :chat-name="chatName"
      :user="otherUser"
      :is-online="isOnline"
      chat-type="private"
    />
    <MessageList :messages="chatStore.messages" :current-user-id="authStore.user?.id" />
    <MessageInput @send="handleSendMessage" @send-audio="handleSendAudio" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useChatStore } from '../stores/chat'
import api from '../services/api'
import ChatHeader from '../components/ChatHeader.vue'
import MessageList from '../components/MessageList.vue'
import MessageInput from '../components/MessageInput.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const chatStore = useChatStore()

const userId = computed(() => parseInt(route.params.userId))
const otherUser = ref(null)
const isOnline = ref(false)
const chatId = ref(null)

const chatName = computed(() => otherUser.value?.username || 'Пользователь')

async function loadChat() {
  try {
    // Получаем или создаем приватный чат
    const response = await api.post('/chats/private', { user_id: userId.value })
    const chat = response.data
    chatId.value = chat.id
    
    otherUser.value = chat.members?.find(m => m.id !== userId.value) || chat.other_user
    
    // Загружаем сообщения
    const messagesResponse = await api.get(`/chats/${chat.id}/messages`)
    chatStore.setMessages(messagesResponse.data)
    
    // Устанавливаем активный чат
    chatStore.setActiveChat({
      id: chat.id,
      type: 'private',
    })
  } catch (error) {
    console.error('Error loading chat:', error)
    router.push('/chat')
  }
}

async function loadMessages() {
  if (!chatId.value) return
  try {
    const response = await api.get(`/chats/${chatId.value}/messages`)
    chatStore.setMessages(response.data)
  } catch (error) {
    console.error('Error loading messages:', error)
  }
}

function handleSendMessage(content) {
  chatStore.sendMessage(content, 'text')
}

function handleSendAudio(audioBlob) {
  chatStore.sendMessage('', 'audio', audioBlob)
}

onMounted(() => {
  loadChat()
})

onUnmounted(() => {
  if (chatId.value && chatStore.activeChat) {
    chatStore.activeChat = null
  }
})
</script>

