import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 导入页面组件
const pages = import.meta.glob<{ default: any }>('./pages/**/*.vue', { eager: true })

// 生成路由配置
const routes = Object.entries(pages).map(([path, component]) => {
    const match = path.match(/\.\/pages\/(.*)\.vue$/)
    const name = match ? match[1].toLowerCase() : ''
    return {
        path: name === 'index' ? '/' : `/${name}`,
        component: component.default
    }
})

const app = createApp(App)
const router = createRouter({
    history: createWebHistory(),
    routes
})

app.use(createPinia())
app.use(router)
app.use(ElementPlus)
app.mount('#app')
