import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useWebSocket } from '../services/websocket'

export const useChatStore = defineStore('chat', () => {
	const chats = ref([])
	const activeChat = ref(null)
	const messages = ref([])
	const users = ref([])
	const ws = ref(null)

	function initializeWebSocket(token) {
		ws.value = useWebSocket(token)

		ws.value.on('message', (message) => {
			messages.value.push(message)
		})

		ws.value.on('chat_created', (chat) => {
			chats.value.push(chat)
		})

		ws.value.on('user_online', (userId) => {
			const user = users.value.find(u => u.id === userId)
			if (user) user.isOnline = true
		})

		ws.value.on('user_offline', (userId) => {
			const user = users.value.find(u => u.id === userId)
			if (user) user.isOnline = false
		})
	}

	function setActiveChat(chat) {
		activeChat.value = chat
		messages.value = []
		if (ws.value) {
			ws.value.joinChat(chat.id, chat.type)
		}
	}

	function sendMessage(content, type = 'text', audioBlob = null) {
		if (!activeChat.value || !ws.value) return

		const message = {
			chat_id: activeChat.value.id,
			chat_type: activeChat.value.type,
			content,
			type,
			audio: audioBlob,
		}

		ws.value.sendMessage(message)
	}

	function addChat(chat) {
		if (!chats.value.find(c => c.id === chat.id)) {
			chats.value.push(chat)
		}
	}

	function setChats(newChats) {
		chats.value = newChats
	}

	function setMessages(newMessages) {
		messages.value = newMessages
	}

	function setUsers(newUsers) {
		users.value = newUsers
	}

	function disconnect() {
		if (ws.value) {
			ws.value.disconnect()
			ws.value = null
		}
	}

	return {
		chats,
		activeChat,
		messages,
		users,
		initializeWebSocket,
		setActiveChat,
		sendMessage,
		addChat,
		setChats,
		setMessages,
		setUsers,
		disconnect,
	}
})

