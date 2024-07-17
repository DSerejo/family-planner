import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';
import dotenv from 'dotenv';

dotenv.config();
const mode = process.env.APP_ENV // This now exists.
export default defineConfig({
	plugins: [sveltekit()],
	mode,
	server: {
		origin: 'https://family-planner.local'
	},
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}'],
		environment: 'jsdom',
		globals: true
	}
});
