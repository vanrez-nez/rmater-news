// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  css: [
    "~/assets/css/theme.css",
    "~/assets/css/main.css"
  ],
  noscript: [{ innerHTML: "This website requires JavaScript." }],
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
