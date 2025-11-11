import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
	{
		path: '/',
		redirect: '/chat',
	},
	{
		path: '/login',
		name: 'Login',
		component: () => import('../views/Login.vue'),
		meta: { requiresGuest: true },
	},
	{
		path: '/register',
		name: 'Register',
		component: () => import('../views/Register.vue'),
		meta: { requiresGuest: true },
	},
	{
		path: '/chat',
		component: () => import('../layouts/MainLayout.vue'),
		meta: { requiresAuth: true },
		children: [
			{
				path: '',
				name: 'ChatList',
				component: () => import('../views/ChatList.vue'),
			},
			{
				path: 'private/:userId',
				name: 'PrivateChat',
				component: () => import('../views/PrivateChat.vue'),
			},
			{
				path: 'group/:groupId',
				name: 'GroupChat',
				component: () => import('../views/GroupChat.vue'),
			},
		],
	},
]

const router = createRouter({
	history: createWebHistory(),
	routes,
})

router.beforeEach((to, from, next) => {
	const authStore = useAuthStore()

	if (to.meta.requiresAuth && !authStore.isAuthenticated) {
		next({ name: 'Login' })
	} else if (to.meta.requiresGuest && authStore.isAuthenticated) {
		next({ name: 'ChatList' })
	} else {
		next()
	}
})

export default router

