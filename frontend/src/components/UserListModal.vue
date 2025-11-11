<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="$emit('close')">
    <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 max-h-[90vh] overflow-y-auto">
      <div class="p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-2xl font-bold text-gray-800">Выберите пользователя</h2>
          <button
            @click="$emit('close')"
            class="text-gray-500 hover:text-gray-700"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="mb-4">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Поиск пользователей..."
            class="input-field"
          />
        </div>

        <div class="border border-gray-300 rounded-lg p-3 max-h-96 overflow-y-auto">
          <div v-if="loading" class="text-center text-gray-500 py-4">
            Загрузка пользователей...
          </div>
          <div v-else-if="filteredUsers.length === 0" class="text-center text-gray-500 py-4">
            Пользователи не найдены
          </div>
          <div v-else class="space-y-2">
            <div
              v-for="user in filteredUsers"
              :key="user.id"
              @click="handleSelect(user)"
              class="flex items-center space-x-3 p-3 hover:bg-gray-50 rounded cursor-pointer transition-colors"
            >
              <div class="w-10 h-10 rounded-full bg-primary-500 flex items-center justify-center text-white font-semibold">
                {{ getUserInitials(user) }}
              </div>
              <div class="flex-1">
                <div class="font-medium text-gray-800">{{ user.username }}</div>
                <div class="text-sm text-gray-500">{{ user.email }}</div>
              </div>
              <div v-if="user.is_online" class="w-3 h-3 bg-green-500 rounded-full"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'

const emit = defineEmits(['close', 'selected'])

const users = ref([])
const searchQuery = ref('')
const loading = ref(true)

const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value
  const query = searchQuery.value.toLowerCase()
  return users.value.filter(user =>
    user.username.toLowerCase().includes(query) ||
    user.email.toLowerCase().includes(query)
  )
})

function getUserInitials(user) {
  return user.username
    ?.split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2) || 'U'
}

function handleSelect(user) {
  emit('selected', user)
}

async function loadUsers() {
  try {
    loading.value = true
    const response = await api.get('/users')
    users.value = response.data
  } catch (err) {
    console.error('Error loading users:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadUsers()
})
</script>

