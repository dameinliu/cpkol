// src/store/theme.ts
import { defineStore } from 'pinia'

const theme = (localStorage.getItem('theme') as 'light' | 'dark') || 'light'
document.documentElement.classList.toggle('dark', theme === 'dark')

export const useThemeStore = defineStore('theme', {
  state: () => ({
    theme,
  }),
  actions: {
    setTheme(val: 'light' | 'dark') {
      this.theme = val
      document.documentElement.classList.toggle('dark', val === 'dark')
      localStorage.setItem('theme', val)
    }
  }
})