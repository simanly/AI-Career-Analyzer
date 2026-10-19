import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
// Lokal inkişaf: backend http://localhost:8000-də işləyir (cd backend && uvicorn main:app --port 8000).
// Render backend-ə qoşulmaq üçün: API_PROXY_TARGET=https://ai-career-analyzer-1.onrender.com npm run dev
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: process.env.API_PROXY_TARGET || 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})