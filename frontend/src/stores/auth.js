import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useAuthStore = defineStore('auth', () => {
    const user = ref(null)
    const token = ref(localStorage.getItem('token') || null)

    const isAuthenticated = computed(() => !!token.value && !!user.value)

    function setToken(newToken) {
        token.value = newToken
        if (newToken) {
            localStorage.setItem('token', newToken)
        } else {
            localStorage.removeItem('token')
        }
    }

    async function login(email, password) {
        try {
            const response = await api.post('/auth/login', { email, password })
            const accessToken = response.data.access_token
            setToken(accessToken)

            await fetchUser()

            return { success: true }
        } catch (error) {
            return {
                success: false,
                error: error.response?.data?.message || 'Ошибка входа',
            }
        }
    }

    async function register(full_name, email, password) {
        try {
            const response = await api.post('/auth/register', {
                full_name,
                email,
                password,
            })
            const accessToken = response.data.access_token
            setToken(accessToken)

            await fetchUser()

            return { success: true }
        } catch (error) {
            return {
                success: false,
                error: error.response?.data?.message || 'Ошибка регистрации',
            }
        }
    }

    async function fetchUser() {
        try {
            const response = await api.get('/users/me')
            user.value = response.data
            return { success: true }
        } catch (error) {
            if (error.response?.status === 401) {
                logout()
            }
            return { success: false }
        }
    }

    function logout() {
        user.value = null
        setToken(null)
    }

    return {
        user,
        token,
        isAuthenticated,
        login,
        register,
        fetchUser,
        logout,
        setToken,
    }
})