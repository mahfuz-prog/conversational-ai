<script setup>
import axios from 'axios'
import { ref, inject } from 'vue'
import { useRouter } from 'vue-router'
import { useNotification } from "@kyvg/vue3-notification"

const router = useRouter()
const store = inject("store")
const notification = useNotification()

const history = ref()
const activeConversation = ref('')

// handle 401 and 403 error
const handleError = (err) => {
  if (err === 401 || err === 403) {
    // reset reactive state
    store.resetState()
    router.push('/log-in')
  }
}

try {
  const data = await (await axios.get('history/')).data
  if (data) {
    history.value = data

    // store those data in a reactive object
  }
} catch (err) {
  handleError(err.status)
}

// select a conversation
const selectBtn = (item) => {

  // if the conversation request is processing than wait until it complete
  if (!store.currentConversation.isLoading) {
    activeConversation.value = item.conversationId
    store.setcurrentConversation(item)
  }
}

// create a new conversation
const newConversation = async() => {
  try {
    const response = await axios.get('new-conversation/')
    history.value.push(response.data)

    // after creating a new conversation, select this conversation
    // so that the chat will continue in this context
    selectBtn(response.data)
    notification.notify({ title: "New conversation created", text: "Now you can chat in this conversation context." })
  } catch (err) {
    if (err.status === 429) {
      notification.notify({ title: "Too many conversations request!", text: "Only 5 conversation context allowed." })
    }
  }
}
</script>
<template>
  <button @click="newConversation" class="new-converation">New Conversation</button>
  <div class="history" v-if="history[0]">
    <template v-for="item in history">
      <button @click="selectBtn(item)" :class="{ border: activeConversation == item.conversationId }">{{item.title}}...</button>
    </template>
  </div>
</template>

<style scoped>
.history {
  display: flex;
  gap: 10px;
  width: 750px;
  justify-content: center;
  flex-wrap: wrap;
}

button {
  color: #ffffff;
  background-color: var(--secondary-black);
  border: 0;
  padding: 10px 20px;
  border-radius: 5px;
  border: 1px solid transparent;
}

.border {
  border: 1px solid var(--accent);
}

.new-converation {
  background-color: var(--accent);
}

@media (max-width: 430px) {
  .history {
    width: 100%;
  }
  button {
    padding: 8px 15px;
  }
}
</style>
