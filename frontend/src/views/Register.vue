<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 to-primary-700 px-4">
    <div class="card max-w-md w-full">
      <h1 class="text-3xl font-bold text-center mb-8 text-gray-800">Регистрация в Fast Talk</h1>
      
      <form @submit.prevent="handleRegister" class="space-y-6">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
            Имя пользователя
          </label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
            class="input-field"
            placeholder="Иван Иванов"
          />
        </div>

        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
            Email
          </label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            class="input-field"
            placeholder="your@email.com"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
            Пароль
          </label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            minlength="6"
            class="input-field"
            placeholder="••••••••"
          />
        </div>

        <div>
          <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2">
            Подтвердите пароль
          </label>
          <input
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            required
            class="input-field"
            placeholder="••••••••"
          />
        </div>

        <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {{ error }}
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
        </button>
      </form>

      <p class="mt-6 text-center text-gray-600">
        Уже есть аккаунт?
        <router-link to="/login" class="text-primary-600 hover:text-primary-700 font-medium">
          Войти
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useChatStore } from '../stores/chat'

const router = useRouter()
const authStore = useAuthStore()
const chatStore = useChatStore()

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  error.value = ''

  if (password.value !== confirmPassword.value) {
    error.value = 'Пароли не совпадают'
    return
  }

  if (password.value.length < 6) {
    error.value = 'Пароль должен содержать минимум 6 символов'
    return
  }

  loading.value = true

  const result = await authStore.register(username.value, email.value, password.value)

  if (result.success) {
    // Инициализируем WebSocket после успешной регистрации
    chatStore.initializeWebSocket(authStore.token)
    router.push('/chat')
  } else {
    error.value = result.error
  }

  loading.value = false
}
</script>

