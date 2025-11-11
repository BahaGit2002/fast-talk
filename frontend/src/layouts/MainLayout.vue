<template>
  <div class="h-screen flex flex-col bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="px-6 py-4 flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <h1 class="text-2xl font-bold text-primary-600">Fast Talk</h1>
        </div>
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <div class="w-10 h-10 rounded-full bg-primary-500 flex items-center justify-center text-white font-semibold">
              {{ userInitials }}
            </div>
            <span class="font-medium text-gray-700">{{ authStore.user?.username }}</span>
          </div>
          <button
            @click="handleLogout"
            class="btn-secondary text-sm"
          >
            Выйти
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <div class="flex-1 flex overflow-hidden">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useChatStore } from '../stores/chat'

const router = useRouter()
const authStore = useAuthStore()
const chatStore = useChatStore()

const userInitials = computed(() => {
  if (!authStore.user?.username) return 'U'
  return authStore.user.username
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
})

function handleLogout() {
  chatStore.disconnect()
  authStore.logout()
  router.push('/login')
}

onUnmounted(() => {
  chatStore.disconnect()
})
</script>

