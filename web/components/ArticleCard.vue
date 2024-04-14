<script>
export default {
  props: {
    title: String,
    date: String,
    content: String
  }
}
</script>

<template>
  <article>
    <h2>{{ title }}</h2>
    <time datetime="{{date}}">
      <small>{{ date }}</small>
    </time>
    <p>{{ content }}</p>
  </article>
</template>