<script setup>
import axios from 'axios'
import { ref, inject } from 'vue'
import { redirectNotify } from '../composables/handleAuthorization'

// this will handle all the logic for redirect and notification
const redirect = new redirectNotify()

// simple state management using reactive
const store = inject("store")

const submitValues = ref({
  email: null,
  password: null
})
const submitErrors = ref({})
const submitBtn = ref('Log In')

async function submitForm() {
  submitErrors.value = {}
  submitBtn.value = 'Submitting'

  // email validation
  if (!validateEmail(submitValues.value.email)) {
    submitErrors.value.email = 'Please enter a valid email address.'
  }

  // password validation
  if (!validatePassword(submitValues.value.password)) {
    submitErrors.value.password = 'Minimum 8 characters uppercase, lowercase, digit, special'
  }

  if (Object.keys(submitErrors.value).length === 0) {
    try {
      const data = await (await axios.post('log-in/', submitValues.value)).data
      const error = data.error

      if (error) {
        submitErrors.value.error = error
        submitBtn.value = 'Log In'
      } else {
        // store the jwt token in reactive
        store.updateState(data.token)

        redirect.update('/account', { title: 'Successfuly Loged In.', text: 'Now you have Ultimate access.' })
        redirect.use()
      }
    } catch (err) {
      if (err.status) {
        throw new Error(err.status)
      }
      throw new Error()
    }
  }
}

// email validation
function validateEmail(email) {
  const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  return re.test(String(email).toLowerCase())
}

// password validation
// must one lowercas, one uppercase, one digit, minimum 8 digit and mximum 20
function validatePassword(password) {
  const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+~`|}{[\]:;<>?]).{8,12}$/
  return re.test(password)
}
</script>
<template>
  <div>
    <form @submit.prevent="submitForm" method="POST">
      <h4>Log In</h4>
      <input type="email" id="email" v-model.trim="submitValues.email" placeholder="Your Email" required/>
      <input type="password" id="password" v-model.trim="submitValues.password" placeholder="Password" required/>
      <span v-if="submitErrors.error">● {{ submitErrors.error }}</span>
      <button type="submit" :class="{deactive : submitBtn==='Submitting'}">{{ submitBtn }}</button>
    </form>
  </div>
</template>

<style scoped>
form {
  border-radius: 5px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 15px;
  padding: 30px;
  width: 350px;
  background-color: var(--secondary-black);
}

input {
  color: #fff;
  border: 0;
  border-radius: 3px;
  width: 100%;
  padding: 10px 15px 10px 15px;
  background-color: var(--tertiary-black);
}

input:focus-visible {
  outline: none;
  color: #fff;
}

button,
input[type="submit"] {
  border: 0;
  background-color: var(--accent);
  border-radius: 25px;
  padding: 9px;
  color: #fff;
  cursor: pointer;
}

.deactive {
  animation: btn-bg 1s infinite;
}

span {
  color: red;
  padding-left: 5px;
  margin-top: -10px;
  font-size: 12px;
  font-weight: 400;
}

h4 {
  color: #fff;
  text-align: center;
  font-size: 16px;
  font-weight: 500;
}

@keyframes btn-bg {
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
</style>
