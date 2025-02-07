<script setup>
import Header from '../components/templates/Header.vue'
import Footer from '../components/templates/Footer.vue'
import Content from '../components/accountpage/Content.vue'
import ContentSkeleton from '../components/accountpage/ContentSkeleton.vue'
</script>
<template>
  <Header />
  <main>
    <Suspense>
      <template #default>
        <Content/>
      </template>
      <template #fallback>
        <ContentSkeleton />
      </template>
    </Suspense>
  </main>
  <Footer />
</template>

<style scoped>
main {
  /*  full height - header height and footer height*/
  height: calc(100vh - 65px - 42px);
  display: grid;
  place-items: center;
}

@media (max-width: 430px) {
  main {
    padding: 10px;
    height: calc(100vh - 90px - 42px);
  }
}
</style>
