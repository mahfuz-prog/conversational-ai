<script setup>
</script>
<template>
  <div class="skeleton">
    <div class="btn"></div>
    <div class="btn"></div>
    <div class="btn"></div>
  </div>
</template>

<style scoped>
.skeleton {
  width: 500px;
  display: flex;
  flex-direction: row;
  gap: 10px;
  justify-content: center;
}

.btn {
  height: 40px;
  width: 150px;
  border-radius: 5px;
  animation: pulse-bg 1s infinite;
}

@media (max-width: 430px) {
  .skeleton {
    width: 100%;
  }
  .btn {
    height: 30px;
    width: 120px;
  }
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
</style>
