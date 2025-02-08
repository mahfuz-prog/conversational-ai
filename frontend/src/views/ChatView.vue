<script setup>
import Header from '../components/templates/Header.vue'
import Footer from '../components/templates/Footer.vue'
import Content from '../components/chatpage/Content.vue'
</script>
<template>
  <Header />
  <main>
    <Content/>
  </main>
  <Footer />
</template>

<style scoped>
main {
  /*  full height - header height and footer height*/
  height: calc(100vh - 65px - 42px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

@media (max-width: 430px) {
  main {
    padding: 10px;
    height: calc(100vh - 90px - 42px);
  }
}
</style>
