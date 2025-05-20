import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useInfluencerStore = defineStore('influencer', () => {
  const influencers = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function searchInfluencers({ keyword, min_fans }) {
    loading.value = true
    error.value = null

    try {
        const res = await axios.get('/api/influencers/search', {
          params: { keyword, min_fans }
        })
        // 这里根据后端返回结构调整
        // data {followerCount: 10000}
        this.influencers = res.data
        // 调试成功
        // console.log(res.data)
      } catch (e) {
        this.error = e.message
      } finally {
        loading.value = false
      }
    }
    
  return {
    influencers,
    loading,
    error,
    searchInfluencers
  }
  })