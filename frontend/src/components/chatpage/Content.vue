<script setup>
import axios from 'axios'
import History from './History.vue'
import { useRouter } from 'vue-router'
import UserIcon from '../icons/UserIcon.vue'
import { ref, inject, nextTick, watch } from 'vue'
import HistorySkeleton from './HistorySkeleton.vue'
import { useNotification } from "@kyvg/vue3-notification"

const router = useRouter()
const store = inject("store")
const notification = useNotification()

const history = ref()
const messageInput = ref('')
const isWaiting = ref(false)

// handle 401 and 403 error
const handleError = (err) => {
  if (err === 401 || err === 403) {
    // reset reactive state
    store.resetState()
    router.push('/log-in')
  }
}

// scroll to last message
const executeScroll = () => {
  const element = document.getElementById("checkpoint")
  if (element) {
    element.scrollIntoView({ behavior: "smooth" })
  }
}

const sendMessage = async() => {
  try {
    // load the id from store if there
    const id = store.currentConversation.conversation.conversationId

    // if there is no input
    if (!messageInput.value) {
      notification.notify({ title: "Invalid Message!", text: "Please ask Something." })
    }

    // check if there any request is processing
    if (isWaiting.value) {
      notification.notify({ title: "Request is processing.", text: "You can't send a new request until processing the current one." })
    }

    // if there is no id found in store then 
    // notify the user to select a conversation context of create a new one.
    if (!id) {
      notification.notify({ title: "Select or Start a new conversation", text: "You have to select a context" })
    }


    // if all of the conditon satisfy send a message
    if (messageInput.value && !isWaiting.value && id) {

      // send a message again after  one req complete
      isWaiting.value = true

      // push the input message
      history.value.push({ 'role': 'user', "text": messageInput.value })

      const payload = { conversationId: id, message: messageInput.value.trim() }
      messageInput.value = ''

      const response = await axios.post('chat/', payload)
      history.value.push({ 'role': 'model', "text": response.data.botReply })
    }

  } catch (err) {
    messageInput.value = history.value[history.value.length - 1].text
    history.value.push({ role: "model", "text": "Error occurred" })
    handleError(err.status)
  } finally {
    // wait for dom render
    await nextTick()

    // scroll to last bot reply after complete the request
    executeScroll()
    isWaiting.value = false
  }
}

// if a new conversation select from History component
// we will send a request and load this conversation history
watch(
  () => store.currentConversation.conversation,
  async(_) => {
    try {
      // set loading state true so we can't sent a new request
      // befor completing the current one
      store.setLoading(true)
      const id = store.currentConversation.conversation.conversationId
      const response = await axios.get(`single-conversation/${id}`)
      history.value = response.data
    } catch (err) {
      notification.notify({ title: "Something went wrong!", text: "Please try to load the conversation again." })
      handleError(err.status)
    } finally {
      store.setLoading(false)
    }
  }
)
</script>
<template>
  <!-- skeleton loading -->
  <Suspense>
    <template #default>
      <History />
    </template>
    <template #fallback>
      <HistorySkeleton />
    </template>
  </Suspense>
  <div class="chatbox-container">
    <!-- show the chat -->
    <div class="chat-messages">
      <template v-for="(msg, index) in history" :key="index">
        <div v-if="msg.role === 'model'" class="bot-message">
          <div class="avatar"></div>
          <div class="message">
            <span>{{msg.text}}</span>
          </div>
        </div>
        <div v-if="msg.role === 'user'" class="user-message">
          <div class="message">
            <span>{{msg.text}}</span>
          </div>
          <div class="avatar">
            <UserIcon />
          </div>
        </div>
      </template>
      <div id="checkpoint"></div>
    </div>
    <!-- Input Box -->
    <div class="input-box">
      <input type="text" v-model="messageInput" id="chat-input" placeholder="Type your message..." @keyup.enter="sendMessage">
      <button id="send-btn" @click="sendMessage" v-if="!isWaiting">Send</button>
      <button class="pending-btn" v-if="isWaiting">Loading...</button>
    </div>
  </div>
</template>

<style scoped>
.chatbox-container {
  width: 700px;
  height: auto;
  max-height: 80%;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid var(--tertiary-black);
  padding: 20px 15px;
}

.chat-messages {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow-y: auto;
  scrollbar-color: var(--accent) transparent;
  scrollbar-width: none;
  font-size: 15px;
}


/*profile icon*/

.avatar {
  height: 30px;
  width: 30px;
  border-radius: 50%;
  background-color: var(--accent);
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 3px;
}


/* Message Styles */

.message {
  background-color: var(--secondary-black);
  color: #ffffff;
  display: flex;
  gap: 10px;
  align-items: center;
  padding: 5px 10px;
  border-radius: 7px;
  max-width: 90%;
}

.bot-message {
  align-self: flex-start;
  display: flex;
  gap: 10px;
  align-items: end;
  max-width: 70%;
}

.bot-message .message {
  border-bottom-left-radius: 0;
}


/* User Message */

.user-message {
  max-width: 70%;
  align-self: flex-end;
  display: flex;
  justify-content: end;
  gap: 10px;
  align-items: end;
}

.user-message .message {
  border-bottom-right-radius: 0;
}


/*input*/

.input-box {
  display: flex;
  padding: 10px;
  background-color: var(--secondary-black);
  border-radius: 5px;
}

.input-box input {
  flex: 1;
  padding: 10px;
  border: 1px solid var(--tertiary-black);
  border-radius: 25px;
  outline: none;
  background-color: transparent;
  color: #ffffff;
}

.input-box button {
  padding: 10px 30px;
  margin-left: 10px;
  background-color: var(--accent);
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
}

.input-box button:hover {
  opacity: .9;
}

.pending-btn {
  animation: pulse-bg 1s infinite;
}

@keyframes pulse-bg {
  0% {
    background-color: rgb(12 187 197 / 15%);
  }
  50% {
    background-color: var(--tertiary-black);
  }
  100% {
    background-color: rgb(12 187 197 / 15%);
  }
}

@media (max-width: 430px) {
  .chatbox-container {
    width: 100%;
    max-height: 100%;
    padding: 15px 10px;
  }
  .message {
    max-width: 85%;
  }
  .bot-message,
  .user-message {
    max-width: 80%;
  }
  .chat-messages {
    font-size: 13px;
  }
}
</style>
