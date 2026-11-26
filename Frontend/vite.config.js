import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
// https://vite.dev/config/server-options
export default defineConfig({
  plugins: [react()],
  server: {
	  proxy: {
		  '/recipes/': {
			  target: 'http://127.0.0.1:8000',
			  changeOrigin: true,
			  rewrite: (path) => path.replace(/^\api/, ''),
		  },
	  },
  },
})
