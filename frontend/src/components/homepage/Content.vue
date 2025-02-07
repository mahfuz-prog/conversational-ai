<script setup>
import axios from 'axios'


// try {
//   const data = await (await axios.get('/')).data
//   if (data) {

//   }
// } catch (err) {
//   if (err.status) {
//     throw new Error(err.status)
//   }
//   throw new Error()
// }
</script>
<template>
  <div class="container">
    <h1>Hola</h1>
  </div>
</template>

<style scoped>
.container {
  width: 1100px;
  height: calc(100vh - 150px);
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 40px;
  border-radius: 5px;
}
</style>
