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
  }

  export default {
    props: {
      article: {
        type: Object as () => Article,
        required: true,
      }
    },
    computed: {
      elapsed(): string {
        return dayjs(this.article.date).fromNow(true);
      },
      friendlySrc(): string {
        return new URL(this.article.src).hostname.replace('www.', '');
      }
    }
  }
</script>

<style>
  article + article {
    margin: 2rem 0;
  }
  .meta {
    opacity: 0.75;
  }

  .meta + h2 {
    margin-top: 0;
  }
</style>

<template>
  <article>
    <small class="meta">
      <a :href="article.src" target="__blank">{{ friendlySrc }}</a>
      <time :datetime="article.date">
        hace {{ elapsed }}
      </time>
    </small>
    <h2>{{ article.title }}</h2>
    <p>{{ article.content }}</p>
  </article>
</template>