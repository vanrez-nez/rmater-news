
<script setup lang="ts">
  const { data } = await useFetch('/api/today-news')
</script>

<template>
  <article>
    <h1>Ultimas noticias</h1>
    <ArticleCard
      v-for="entry in data"
      :key="entry.id"
      :article="entry"
    />
  </article>
</template>