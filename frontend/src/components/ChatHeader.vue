<template>
  <div class="bg-white border-b border-gray-200 px-6 py-4">
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-12 h-12 rounded-full bg-primary-500 flex items-center justify-center text-white font-semibold">
          {{ getInitials() }}
        </div>
        <div>
          <h2 class="font-semibold text-gray-800">{{ chatName }}</h2>
          <p v-if="chatType === 'private' && isOnline" class="text-sm text-green-600">
            В сети
          </p>
          <p v-else-if="chatType === 'private'" class="text-sm text-gray-500">
            Не в сети
          </p>
          <p v-else-if="chatType === 'group'" class="text-sm text-gray-500">
            {{ members?.length || 0 }} участников
          </p>
        </div>
      </div>
      <div v-if="chatType === 'group'" class="flex items-center space-x-2">
        <button
          @click="showMembers = !showMembers"
          class="btn-secondary text-sm"
        >
          Участники
        </button>
      </div>
    </div>

    <!-- Members dropdown -->
    <div v-if="showMembers && chatType === 'group'" class="mt-4 pt-4 border-t border-gray-200">
      <h3 class="font-medium text-gray-700 mb-2">Участники группы:</h3>
      <div class="flex flex-wrap gap-2">
        <div
          v-for="member in members"
          :key="member.id"
          class="flex items-center space-x-2 bg-gray-100 px-3 py-1 rounded-full"
        >
          <div class="w-6 h-6 rounded-full bg-primary-400 flex items-center justify-center text-white text-xs font-semibold">
            {{ getMemberInitials(member) }}
          </div>
          <span class="text-sm text-gray-700">{{ member.username }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  chatName: {
    type: String,
    required: true,
  },
  chatType: {
    type: String,
    required: true,
  },
  user: {
    type: Object,
    default: null,
  },
  members: {
    type: Array,
    default: () => [],
  },
  isOnline: {
    type: Boolean,
    default: false,
  },
  groupId: {
    type: Number,
    default: null,
  },
})

const showMembers = ref(false)

function getInitials() {
  if (props.chatType === 'group') {
    return props.chatName
      .split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2)
  } else {
    return props.user?.username
      ?.split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2) || 'U'
  }
}

function getMemberInitials(member) {
  return member.username
    ?.split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2) || 'U'
}
</script>

