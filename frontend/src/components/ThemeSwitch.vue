<!-- src/components/ThemeSwitch.vue -->
<template>
  <el-switch
    v-model="isDark"
    :active-icon="Moon"
    :inactive-icon="Sunny"
    @change="themeStore.setTheme(isDark ? 'dark' : 'light')"
  />
</template>

<script setup lang="ts">
import { useThemeStore } from '../store/theme'
import { Moon, Sunny } from '@element-plus/icons-vue'
import { computed } from 'vue'

const themeStore = useThemeStore()
const isDark = computed({
  get: () => themeStore.theme === 'dark',
  set: (val: boolean) => themeStore.setTheme(val ? 'dark' : 'light')
})
</script>
