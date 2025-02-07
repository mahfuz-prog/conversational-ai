import './assets/main.css'

import axios from 'axios'
import App from './App.vue'
import store from "./store"
import router from './router'
import Notifications from '@kyvg/vue3-notification'

// import conf from '/etc/chatbot.json'
import conf from "C:/Users/User/Desktop/task/config.json"

import { createApp } from 'vue'

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/'
// axios.defaults.baseURL = 'https://webwaymark.com/api/'
axios.defaults.headers.common['x-access-token'] = `${conf.AUTHORIZATION_PREFIX} ${store.state.token}`

async function checkToken() {
	try {
		await axios.get('login-check/')
	} catch (err) {
		if (err.status !== 404) {
			// reset the token
			store.resetState()
		}
	}
}

// if the application found a jwt token at starting then 
// it will send this token to verify this
if (store.state.token) {
	checkToken()
}


const app = createApp(App)

// make accessable reactive store object to the entire app
app.provide("store", store)
app.use(router)
app.use(Notifications)
app.mount('#app')

