export default defineNuxtConfig({
  compatibilityDate: '2025-01-01',
  devtools: { enabled: false },

  modules: [
    '@element-plus/nuxt',
    '@nuxtjs/sitemap',
  ],

  elementPlus: {
    importStyle: 'css',
  },

  css: ['~/assets/css/main.css'],

  app: {
    head: {
      htmlAttrs: { lang: 'en' },
      title: 'Exchange Rate Monitor',
      titleTemplate: '%s',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'format-detection', content: 'telephone=no' },
        { name: 'theme-color', content: '#1a2332' },
        { name: 'robots', content: 'index, follow' },
        { property: 'og:site_name', content: 'Exchange Rate Monitor' },
        { name: 'author', content: 'Exchange Rate Monitor' },
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'dns-prefetch', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
      ],
    },
  },

  sitemap: {
    hostname: 'https://yoursite.com',
    gzip: true,
    routes: async () => {
      const pairs = []
      const currencies = ['USD','EUR','JPY','GBP','CNY','AUD','CAD','CHF','HKD','NZD','SEK','KRW','SGD','NOK','MXN','INR','RUB','ZAR','TRY','BRL']
      for (const from of currencies) {
        for (const to of currencies) {
          if (from !== to) {
            pairs.push({
              loc: `/${from.toLowerCase()}-to-${to.toLowerCase()}`,
              changefreq: 'hourly',
              priority: from === 'USD' ? 0.8 : 0.5,
            })
          }
        }
      }
      return pairs
    },
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || 'http://127.0.0.1:8080',
    },
  },

  routeRules: {
    '/api/**': { proxy: { to: 'http://127.0.0.1:8080/api/**' } },
  },

  nitro: {
    compressPublicAssets: true,
  },
})
