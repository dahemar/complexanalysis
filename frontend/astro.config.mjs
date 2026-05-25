// @ts-check
import { defineConfig } from 'astro/config';

const apiTarget = process.env.API_PROXY_TARGET ?? 'http://127.0.0.1:8000';

// https://astro.build/config
export default defineConfig({
	vite: {
		server: {
			proxy: {
				'/api': { target: apiTarget, changeOrigin: true },
				'/health': { target: apiTarget, changeOrigin: true },
			},
		},
	},
});
