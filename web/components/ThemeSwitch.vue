<script setup>
import { ref } from 'vue'
const themeSwitch = ref(true)
</script>

<template>
  <div>
    <input type="checkbox" v-model="themeSwitch" />
  </div>
</template>