import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useInfluencerStore = defineStore('influencer', () => {
  const influencers = ref([])
  const loading = ref(false)
  const error = ref(null)
  const userInfo = ref(null)
  const videoStats = ref(null)
  const total = ref(0)
  const page = ref(1)
  const perPage = ref(12)
  const pages = ref(1)

  async function searchInfluencers({ keyword }) {
    loading.value = true
    error.value = null

    try {
        const res = await axios.get('/api/influencers/search', {
          params: { keyword }
        })
        // 这里根据后端返回结构调整
        // // "userInfo": {
        //     "handle": influencer.handle,
        //     "sec_uid": influencer.sec_uid,
        //     "followerCount": influencer.follower_count,
        //     "total_play_count": influencer.total_play_count,
        //     "total_comment_count": influencer.total_comment_count,
        //     "total_digg_count": influencer.total_digg_count,
        //     "video_count": influencer.video_count,
        //     "videos": []
        // }
        this.influencers = res.data

        // 调试成功
        // console.log(res.data)
      } catch (e) {
        this.error = e.message
      } finally {
        loading.value = false
      }
    }
    
  async function fetchInfluencers({ page: p = 1, perPage: pp = 10 } = {}) {
    loading.value = true
    error.value = null
    try {
      const res = await axios.get('/api/influencers', {
        params: { page: p, per_page: pp }
      })
      influencers.value = res.data.items
      total.value = res.data.total
      page.value = res.data.page
      perPage.value = res.data.per_page
      pages.value = res.data.pages
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  return {
    influencers,
    loading,
    error,
    total,
    page,
    perPage,
    pages,
    fetchInfluencers,
    searchInfluencers
  }
})