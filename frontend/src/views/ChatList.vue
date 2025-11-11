<template>
  <div class="flex h-full">
    <!-- Sidebar with chats -->
    <div class="w-80 bg-white border-r border-gray-200 flex flex-col">
      <div class="p-4 border-b border-gray-200">
        <div class="flex space-x-2 mb-4">
          <button
            @click="showCreateGroup = true"
            class="btn-primary flex-1 text-sm"
          >
            Создать группу
          </button>
          <button
            @click="showUserList = true"
            class="btn-secondary flex-1 text-sm"
          >
            Новый чат
          </button>
        </div>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Поиск чатов..."
          class="input-field text-sm"
        />
      </div>

      <div class="flex-1 overflow-y-auto">
        <div v-if="loading" class="p-4 text-center text-gray-500">
          Загрузка...
        </div>
        <div v-else-if="filteredChats.length === 0" class="p-4 text-center text-gray-500">
          Нет чатов. Создайте новый!
        </div>
        <div v-else>
          <div
            v-for="chat in filteredChats"
            :key="chat.id"
            @click="selectChat(chat)"
            class="p-4 border-b border-gray-100 hover:bg-gray-50 cursor-pointer transition-colors"
            :class="{ 'bg-primary-50': activeChatId === chat.id }"
          >
            <div class="flex items-center space-x-3">
              <div class="w-12 h-12 rounded-full bg-primary-500 flex items-center justify-center text-white font-semibold flex-shrink-0">
                {{ getChatInitials(chat) }}
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between">
                  <h3 class="font-semibold text-gray-800 truncate">
                    {{ getChatName(chat) }}
                  </h3>
                  <span v-if="chat.last_message" class="text-xs text-gray-500">
                    {{ formatTime(chat.last_message.created_at) }}
                  </span>
                </div>
                <p v-if="chat.last_message" class="text-sm text-gray-600 truncate mt-1">
                  {{ chat.last_message.type === 'audio' ? '🎤 Голосовое сообщение' : chat.last_message.content }}
                </p>
                <div v-if="chat.type === 'group'" class="flex items-center mt-1">
                  <span class="text-xs text-gray-500">{{ chat.members_count || 0 }} участников</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main chat area -->
    <div class="flex-1 flex items-center justify-center bg-gray-100">
      <div class="text-center text-gray-500">
        <div class="text-6xl mb-4">💬</div>
        <p class="text-xl">Выберите чат для начала общения</p>
      </div>
    </div>

    <!-- Create Group Modal -->
    <CreateGroupModal
      v-if="showCreateGroup"
      @close="showCreateGroup = false"
      @created="handleGroupCreated"
    />

    <!-- User List Modal -->
    <UserListModal
      v-if="showUserList"
      @close="showUserList = false"
      @selected="handleUserSelected"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useChatStore } from '../stores/chat'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'
import CreateGroupModal from '../components/CreateGroupModal.vue'
import UserListModal from '../components/UserListModal.vue'

const router = useRouter()
const chatStore = useChatStore()
const authStore = useAuthStore()

// Инициализируем WebSocket если еще не инициализирован
onMounted(() => {
  if (authStore.isAuthenticated && authStore.token && !chatStore.ws) {
    chatStore.initializeWebSocket(authStore.token)
  }
  loadChats()
})

const chats = ref([])
const searchQuery = ref('')
const loading = ref(true)
const showCreateGroup = ref(false)
const showUserList = ref(false)
const activeChatId = ref(null)

const filteredChats = computed(() => {
  if (!searchQuery.value) return chats.value
  const query = searchQuery.value.toLowerCase()
  return chats.value.filter(chat => {
    const name = getChatName(chat).toLowerCase()
    return name.includes(query)
  })
})

function getChatName(chat) {
  if (chat.type === 'group') {
    return chat.name
  } else {
    // Для приватного чата показываем имя собеседника
    return chat.other_user?.username || 'Пользователь'
  }
}

function getChatInitials(chat) {
  const name = getChatName(chat)
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

function formatTime(dateString) {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return 'только что'
  if (minutes < 60) return `${minutes}м`
  if (hours < 24) return `${hours}ч`
  if (days < 7) return `${days}д`
  return date.toLocaleDateString('ru-RU')
}

function selectChat(chat) {
  activeChatId.value = chat.id
  if (chat.type === 'group') {
    router.push(`/chat/group/${chat.id}`)
  } else {
    const otherUserId = chat.other_user?.id || chat.members?.find(m => m.id !== authStore.user?.id)?.id
    router.push(`/chat/private/${otherUserId}`)
  }
}

async function loadChats() {
  try {
    loading.value = true
    const response = await api.get('/chats')
    chats.value = response.data
    chatStore.setChats(response.data)
  } catch (error) {
    console.error('Error loading chats:', error)
  } finally {
    loading.value = false
  }
}

function handleGroupCreated(group) {
  chats.value.unshift(group)
  chatStore.addChat(group)
  showCreateGroup.value = false
  selectChat(group)
}

async function handleUserSelected(user) {
  try {
    // Создаем или получаем приватный чат
    const response = await api.post('/chats/private', { user_id: user.id })
    const chat = response.data
    if (!chats.value.find(c => c.id === chat.id)) {
      chats.value.unshift(chat)
      chatStore.addChat(chat)
    }
    showUserList.value = false
    selectChat(chat)
  } catch (error) {
    console.error('Error creating private chat:', error)
  }
}

</script>

