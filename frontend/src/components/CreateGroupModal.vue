<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="$emit('close')">
    <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 max-h-[90vh] overflow-y-auto">
      <div class="p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-2xl font-bold text-gray-800">Создать группу</h2>
          <button
            @click="$emit('close')"
            class="text-gray-500 hover:text-gray-700"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="handleCreate" class="space-y-4">
          <div>
            <label for="groupName" class="block text-sm font-medium text-gray-700 mb-2">
              Название группы
            </label>
            <input
              id="groupName"
              v-model="groupName"
              type="text"
              required
              class="input-field"
              placeholder="Моя группа"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Выберите участников
            </label>
            <div class="border border-gray-300 rounded-lg p-3 max-h-60 overflow-y-auto">
              <div v-if="loading" class="text-center text-gray-500 py-4">
                Загрузка пользователей...
              </div>
              <div v-else-if="users.length === 0" class="text-center text-gray-500 py-4">
                Нет доступных пользователей
              </div>
              <div v-else class="space-y-2">
                <label
                  v-for="user in users"
                  :key="user.id"
                  class="flex items-center space-x-2 p-2 hover:bg-gray-50 rounded cursor-pointer"
                >
                  <input
                    type="checkbox"
                    :value="user.id"
                    v-model="selectedUsers"
                    class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <div class="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center text-white font-semibold text-sm">
                    {{ getUserInitials(user) }}
                  </div>
                  <span class="text-gray-700">{{ user.username }}</span>
                </label>
              </div>
            </div>
          </div>

          <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {{ error }}
          </div>

          <div class="flex space-x-3">
            <button
              type="button"
              @click="$emit('close')"
              class="btn-secondary flex-1"
            >
              Отмена
            </button>
            <button
              type="submit"
              :disabled="!groupName.trim() || selectedUsers.length === 0 || creating"
              class="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ creating ? 'Создание...' : 'Создать' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const emit = defineEmits(['close', 'created'])

const groupName = ref('')
const users = ref([])
const selectedUsers = ref([])
const loading = ref(true)
const creating = ref(false)
const error = ref('')

function getUserInitials(user) {
  return user.username
    ?.split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2) || 'U'
}

async function loadUsers() {
  try {
    loading.value = true
    const response = await api.get('/users')
    users.value = response.data
  } catch (err) {
    console.error('Error loading users:', err)
    error.value = 'Не удалось загрузить пользователей'
  } finally {
    loading.value = false
  }
}

async function handleCreate() {
  if (!groupName.value.trim() || selectedUsers.value.length === 0) {
    return
  }

  try {
    creating.value = true
    error.value = ''
    const response = await api.post('/chats/group', {
      name: groupName.value.trim(),
      user_ids: selectedUsers.value,
    })
    emit('created', response.data)
  } catch (err) {
    console.error('Error creating group:', err)
    error.value = err.response?.data?.message || 'Не удалось создать группу'
  } finally {
    creating.value = false
  }
}

onMounted(() => {
  loadUsers()
})
</script>

