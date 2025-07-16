// src/store/video.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001'

export const useVideoStore = defineStore('video', () => {
  const videos = ref<any[]>([])
  const loading = ref(false)
  const errorMsg = ref('')

  async function fetchVideos(country: string) {
    loading.value = true
    errorMsg.value = ''
    videos.value = []
    try {
      const res = await axios.get(`${API_URL}/video/trending`, {
        params: { country }
      })
      videos.value = res.data
      console.log('获取到的视频数据:', videos.value)
    } catch (e) {
      errorMsg.value = '获取视频失败，请重试'
    } finally {
      loading.value = false
    }
  }

  return { videos, loading, errorMsg, fetchVideos }
})