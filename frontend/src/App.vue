<template>
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()

onMounted(() => {
  // Проверяем токен при загрузке приложения
  const token = localStorage.getItem('token')
  if (token) {
    authStore.setToken(token)
    authStore.fetchUser()
  }
})
</script>

