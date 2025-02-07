<script setup>
import axios from 'axios'
import { ref, inject } from 'vue'
import ProfileIcon from '../icons/ProfileIcon.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const store = inject("store")

const info = ref({
  username: '',
  email: ''
})

try {
  const data = await (await axios.get('account/')).data
  info.value.username = data.name
  info.value.email = data.email
} catch (err) {
  if (err.status === 401 || err.status === 403) {
    // reset reactive state
    store.resetState()
    router.push('/log-in')
  }
}
</script>
<template>
  <div class="container">
    <div class="icon">
      <ProfileIcon />
    </div>
    <div class="user-info">
      <h4><span>User Name: </span>{{ info.username.replace(/\b\w/g, char => char.toUpperCase()).replace('-', ' ') }}</h4>
      <h4><span>Email: </span>{{ info.email }}</h4>
    </div>
  </div>
</template>

<style scoped>
.container {
  width: 700px;
  border: 1px solid var(--tertiary-black);
  border-radius: 5px;
  padding: 30px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.icon {
  display: flex;
  border: 2px solid var(--accent);
  border-radius: 50%;
}

.user-info {
  text-align: center;
}

span {
  color: #ffffff !important;
}

h4 {
  color: var(--text-dark);
}

a {
  color: var(--text-dark);
  text-decoration: underline;
  text-decoration-color: var(--accent);
}

@media (max-width: 430px) {
  .container {
    padding: 20px;
    width: 100%;
  }
}
</style>
