<script setup>
import Header from '../components/templates/Header.vue'
import Footer from '../components/templates/Footer.vue'
import Content from '../components/homepage/Content.vue'
</script>
<template>
  <Header />
  <main>
    <Content />
  </main>
  <Footer />
</template>

<style scoped>
main {
  width: 100vw;
  /*  full height - header height and footer height*/
  height: calc(100vh - 65px - 42px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

@media (max-width: 430px) {
  main {
    height: calc(100vh - 90px - 42px);
    padding: 10px;
  }
}
</style>
