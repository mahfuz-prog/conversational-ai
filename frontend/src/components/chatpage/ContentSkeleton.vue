<script setup>
import ProfileIcon from '../icons/ProfileIcon.vue'
</script>
<template>
  <div class="skeleton">
    <div class="box">
      <div class="icon">
        <ProfileIcon />
      </div>
      <div class="info">
        <div class="item"></div>
        <div class="item"></div>
        <div class="item"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.skeleton {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.box {
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

.info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.item {
  width: 250px;
  height: 15px;
  border-radius: 25px;
  animation: pulse-bg 1s infinite;
}

@media (max-width: 430px) {
  .box {
    width: 100%;
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
