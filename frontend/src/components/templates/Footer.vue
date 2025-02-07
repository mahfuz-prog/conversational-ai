<script setup>
</script>
<template>
  <footer>
    <p>Copyright © 2025 by Conversational AI. All rights reversed.</p>
  </footer>
</template>

<style scoped>
footer {
  color: var(--text-dark);
  width: 100%;
  height: 42px;
  background-color: var(--secondary-black);
  padding: 20px;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (min-width: 768px) {
  footer {
    width: 100%;
  }
}

@media (min-width: 430px) {
  footer {
    padding: 0;
  }
}
</style>
