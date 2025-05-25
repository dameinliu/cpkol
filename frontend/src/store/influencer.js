import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useInfluencerStore = defineStore('influencer', () => {
  const influencers = ref([])
  const loading = ref(false)
  const error = ref(null)
  const userInfo = ref(null)
  const videoStats = ref(null)

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
    
  return {
    influencers,
    loading,
    error,
    searchInfluencers
  }
  })