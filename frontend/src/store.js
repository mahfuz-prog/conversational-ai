// reactive object for state managemnet
// store and retrieve jwt token from localStorage
import axios from 'axios' 
import { reactive, readonly } from 'vue'

import conf from '/etc/chatbot.json'
// import conf from "C:/Users/User/Desktop/task/config.json"

// get jwt from localStorage
const state = reactive({
	token: localStorage.getItem('token')
})


// set jwt token to default header and localStorage
const updateState = (token) => {
	state.token = token
	localStorage.setItem('token', token)
	axios.defaults.headers.common['x-access-token'] = `${conf.AUTHORIZATION_PREFIX} ${token}`
}

// remove the jwt token from localStorage and default header
const resetState = () => {
	state.token = null
	axios.defaults.headers.common['x-access-token'] = ''
	localStorage.removeItem('token')
}


// store a conversation which will be shown in the chat box
const currentConversation = reactive({
	conversation: '',
	isLoading: false,
})

// set a conversation
const setcurrentConversation = (conversation) => {
	currentConversation.conversation = conversation
}

const setLoading = (status) => {
	currentConversation.isLoading = status
}


export default {
	state: readonly(state),
	resetState,
	updateState,

	currentConversation: readonly(currentConversation),
	setcurrentConversation,
	setLoading
}