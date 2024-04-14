
<script setup lang="ts">
  const sqlite3 = require('sqlite3');
  // open sqlite db from file system at storage/news.db
  const db = new sqlite3.Database('storage/news.db');

  async function getNews() {
    return new Promise((resolve, reject) => {
      db.all('SELECT * FROM entries ORDER BY date DESC', (err:any, rows:any[]) => {
        if (err) {
          reject(err);
        }
        resolve(rows);
      });
    });
  }
  // select all rows from news table
  const data = await getNews();
</script>

<template>
  <article>
    <h1>News</h1>
    <ul>
      <li v-for="entry in data" :key="entry.id">
        <h2>{{ entry.title }}</h2>
        <time datetime="{{entry.date}}">
          <small>{{ entry.date }}</small>
        </time>
        <p>{{ entry.content }}</p>
      </li>
    </ul>
  </article>
</template>