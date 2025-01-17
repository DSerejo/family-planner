import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';
import {loadEnv} from 'vite';
import dotenv from 'dotenv';



export default ({mode}: {mode: string}) => {
	console.log(process.env.API_URL)
	return defineConfig({
		plugins: [sveltekit()],
		server: {
			origin: 'https://family-planner.local'
		},
		test: {
			include: ['src/**/*.{test,spec}.{js,ts}'],
			environment: 'jsdom',
			setupFiles: ["src/setupTests.ts"],
			globals: true,
			alias: [
				{ find: /^svelte$/, replacement: "svelte/internal" }
			  ]
		}
	});
}
