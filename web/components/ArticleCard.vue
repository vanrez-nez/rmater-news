<script lang="ts">
  import dayjs from 'dayjs'
  import relativeTime from 'dayjs/plugin/relativeTime'
  import es from 'dayjs/locale/es'
  dayjs.extend(relativeTime)
  dayjs.locale(es)

  interface Article {
    title: string;
    content: string;
    url: string;
    date: string;
    src: string;
    author: string;
    elapsed: string;
  }

  export default {
    props: {
      article: {
        type: Object as () => Article,
        required: true,
      }
    },
    setup(props: { article: Article }) {
      const elapsed = dayjs(props.article.date).fromNow(true)
      props.article.elapsed = elapsed
      return props
    }
  }
</script>

<style>
  article + article {
    margin: 2rem 0;
  }
</style>

<template>
  <article>
    <h2>{{ article.title }}</h2>
    <time :datetime="article.date">
      <small>Hace {{ article.elapsed }}</small>
    </time>
    <p>{{ article.content }}</p>
  </article>
</template>