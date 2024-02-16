import { resolve } from "path";
// https://nuxt.com/docs/api/configuration/nuxt-config

export default defineNuxtConfig({
  devtools: { enabled: true },
  alias: {
    "@": resolve(__dirname, "/"),
  },
  css: [
    "~/assets/css/theme.css",
    "~/assets/css/main.css"
  ],
  modules: [
    '@nuxtjs/google-fonts'
  ],
  googleFonts: {
    prefetch: true,
    preconnect: true,
    preload: true,
    download: true,
    outputDir: 'assets/fonts',
    display: 'swap',
    families: {
      'Inter': {
        wght: '100..900'
      },
    }
  }
})
