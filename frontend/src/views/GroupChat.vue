<template>
  <div class="flex-1 flex flex-col bg-white">
    <ChatHeader
      :chat-name="groupName"
      :members="members"
      chat-type="group"
      :group-id="groupId"
    />
    <MessageList :messages="chatStore.messages" :current-user-id="authStore.user?.id" />
    <MessageInput @send="handleSendMessage" @send-audio="handleSendAudio" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
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

const groupId = computed(() => parseInt(route.params.groupId))
const groupName = ref('')
const members = ref([])

async function loadGroup() {
  try {
    const response = await api.get(`/chats/${groupId.value}`)
    const chat = response.data
    groupName.value = chat.name
    members.value = chat.members || []
    
    // Загружаем сообщения
    const messagesResponse = await api.get(`/chats/${groupId.value}/messages`)
    chatStore.setMessages(messagesResponse.data)
    
    // Устанавливаем активный чат
    chatStore.setActiveChat({
      id: chat.id,
      type: 'group',
    })
  } catch (error) {
    console.error('Error loading group:', error)
    router.push('/chat')
  }
}

function handleSendMessage(content) {
  chatStore.sendMessage(content, 'text')
}

function handleSendAudio(audioBlob) {
  chatStore.sendMessage('', 'audio', audioBlob)
}

onMounted(() => {
  loadGroup()
})

onUnmounted(() => {
  if (groupId.value && chatStore.activeChat) {
    chatStore.activeChat = null
  }
})
</script>

