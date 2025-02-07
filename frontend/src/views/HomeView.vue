<script setup>
import { useRouter } from 'vue-router'
import { onErrorCaptured, ref } from 'vue'
import Header from '../components/templates/Header.vue'
import Footer from '../components/templates/Footer.vue'
import Error from '../components/templates/Error.vue'
import Content from '../components/homepage/Content.vue'
import ContentSkeleton from '../components/homepage/ContentSkeleton.vue'

const router = useRouter()

const error = ref()

onErrorCaptured((err) => {
  error.value = err
})
</script>
<template>
  <Header />
  <main v-if="!error">
    <Suspense>
      <template #default>
        <Content />
      </template>
      <template #fallback>
        <ContentSkeleton />
      </template>
    </Suspense>
  </main>
  <Error :err="String(error)" v-if="error" />
  <Footer />
</template>

<style scoped>
main {
  width: 100vw;
  /*  full height - header height and footer height*/
  height: calc(100vh - 65px - 42px);
  display: grid;
  place-items: center;
}

@media (max-width: 430px) {
  main {
    height: calc(100vh - 90px - 42px);
  }
}
</style>
