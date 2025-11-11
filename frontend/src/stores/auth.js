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
			setToken(response.data.token)
			user.value = response.data.user
			return { success: true }
		} catch (error) {
			return {
				success: false,
				error: error.response?.data?.message || 'Ошибка входа',
			}
		}
	}

	async function register(username, email, password) {
		try {
			const response = await api.post('/auth/register', {
				username,
				email,
				password,
			})
			setToken(response.data.token)
			user.value = response.data.user
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
			const response = await api.get('/auth/me')
			user.value = response.data
			return { success: true }
		} catch (error) {
			setToken(null)
			user.value = null
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

