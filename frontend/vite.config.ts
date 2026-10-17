import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // API の URL は Aspire の AppHost が API_HTTP として渡す（apphost.mts の withReference(api)）
      '/api': {
        target: process.env.API_HTTP,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
