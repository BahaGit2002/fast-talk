import { io } from 'socket.io-client'

let socket = null

export function useWebSocket(token) {
	if (socket && socket.connected) {
		return createWebSocketService(socket)
	}

	socket = io('http://localhost:8000', {
		auth: {
			token,
		},
		transports: ['websocket'],
	})

	socket.on('connect', () => {
		console.log('WebSocket connected')
	})

	socket.on('disconnect', () => {
		console.log('WebSocket disconnected')
	})

	socket.on('error', (error) => {
		console.error('WebSocket error:', error)
	})

	return createWebSocketService(socket)
}

function createWebSocketService(ws) {
	return {
		on(event, callback) {
			ws.on(event, callback)
		},

		off(event, callback) {
			ws.off(event, callback)
		},

		emit(event, data) {
			ws.emit(event, data)
		},

		joinChat(chatId, chatType) {
			ws.emit('join_chat', { chat_id: chatId, chat_type: chatType })
		},

		leaveChat(chatId, chatType) {
			ws.emit('leave_chat', { chat_id: chatId, chat_type: chatType })
		},

		sendMessage(message) {
			if (message.type === 'audio' && message.audio) {
				// Для аудио отправляем через отдельный эндпоинт или как base64
				const reader = new FileReader()
				reader.onloadend = () => {
					ws.emit('send_message', {
						...message,
						audio: reader.result,
					})
				}
				reader.readAsDataURL(message.audio)
			} else {
				ws.emit('send_message', message)
			}
		},

		disconnect() {
			if (socket) {
				socket.disconnect()
				socket = null
			}
		},
	}
}

