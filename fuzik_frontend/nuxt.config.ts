// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  runtimeConfig: {
    public: {
      // เวลาจะสลับ ให้แก้แค่ค่าตรงนี้ค่าเดียวครับ
      apiBase: process.env.NODE_ENV === 'development'
        ? 'http://127.0.0.1:8000'
        : 'https://downloadlovedy.pythonanywhere.com'
    }
  }
})