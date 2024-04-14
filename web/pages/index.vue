
<script setup lang="ts">
  const { data } = await useFetch('/api/today-news')
</script>

<template>
  <article>
    <h1>News</h1>
    <ArticleCard
      v-for="entry in data"
      :key="entry.id"
      :title="entry.title"
      :date="entry.date"
      :content="entry.content"
    />
  </article>
</template>