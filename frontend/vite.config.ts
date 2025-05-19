import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve, dirname } from 'node:path'
import { fileURLToPath } from 'url'
import VueI18nPlugin from '@intlify/unplugin-vue-i18n/vite'

// https://vitejs.dev/config/
export default defineConfig({
	build: {
		sourcemap: false,
		minify: 'esbuild'
	},
	esbuild: {
		drop: process.env.NODE_ENV === 'production' ? ['console', 'debugger'] : []
	},
	resolve: {
		alias: [
			// '@': resolve(__dirname, 'src'),
			{
				find: '@',
				replacement: fileURLToPath(new URL('./src', import.meta.url)),
			},
			{
				find: '@assets',
				replacement: fileURLToPath(new URL('./src/assets', import.meta.url)),
			},
			{
				find: '@pages',
				replacement: fileURLToPath(new URL('./src/pages', import.meta.url)),
			},
			{
				find: '@stores',
				replacement: fileURLToPath(new URL('./src/stores', import.meta.url)),
			},
		],
		// https://stackoverflow.com/questions/69527016/vue3-vite-alias-not-working-as-expected-with-typescript
	},
	plugins: [
		vue(),
		VueI18nPlugin({
			include: resolve(
				dirname(fileURLToPath(import.meta.url)),
				'./src/i18n/locales/**'
			),
		}),
	],
})
