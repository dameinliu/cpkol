import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import VueRouter from 'unplugin-vue-router/vite'
import UnoCSS from 'unocss/vite'

export default defineConfig({
  plugins: [
    VueRouter({
      routesFolder: 'src/pages',
      dts: 'src/typed-router.d.ts',
      routeBlockLang: 'yaml',
      extensions: ['.vue'],
      exclude: ['**/components/**', '**/layouts/**'],
    }),
    vue(),
    AutoImport({
      // 自动导入element-plus
      resolvers: [ElementPlusResolver()],
      // 自动导入vue-router和pinia
      imports: ['vue', 'vue-router', 'pinia'],
      // 生成自动导入的类型文件
      dts: 'src/auto-imports.d.ts',
    }),
    Components({
      // 自动导入element-plus
      resolvers: [ElementPlusResolver()],
      // 生成自动导入的类型文件
      dts: 'src/components.d.ts',
    }),
    UnoCSS(),
  ],
  server: {
    host: '0.0.0.0', // 允许从外部访问
    port: 5173,
    proxy: {
      // 将所有 /api 的请求代理到后端容器
      '/api': {
        target: 'http://cp-backend-dev:5001', // 指向后端服务的容器名
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''), // 去掉 /api 前缀
      },
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        // additionalData: `@import "@/assets/element-variables.scss";`
      }
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})