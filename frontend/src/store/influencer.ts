import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001'
const PER_PAGE = import.meta.env.PER_PAGE || 12

export const useInfluencerStore = defineStore('influencer', () => {
  const influencers = ref([])
  const loading = ref(false)
  const error = ref(null)
  // const userInfo = ref(null)
  // const videoStats = ref(null)
  const total = ref(0)
  const page = ref(1)
  const perPage = ref(PER_PAGE)
  const pages = ref(1)

  async function searchInfluencers({ keyword }) {
    loading.value = true
    error.value = null

    try {
        const res = await axios.get(`${API_URL}/kol/search`, {
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

        // 调试成功
        influencers.value = res.data.results
        error.value = res.data.errors

        console.log(influencers.value)
        console.log(error.value)
        console.log("ha")
      } catch (e) {
        this.error = e.message
      } finally {
        loading.value = false
      }
    }
    
  async function fetchInfluencers({ page: p = 1, perPage: pp = PER_PAGE } = {}) {
    loading.value = true
    error.value = null
    try {
      const res = await axios.get(`${API_URL}/kol/list`, {
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

  async function updateInfluencer(handle, content_type:Array<string>, note:string) {
    try {
      const res = await axios.post(`${API_URL}/kol/update`, {
        handle,
        content_type,
        note
      })

      const targetInfluencer = influencers.value.find(influencer => influencer.handle === handle)
      if (targetInfluencer) {
        targetInfluencer.content_type = content_type
        targetInfluencer.note = note
        targetInfluencer.updated_date = res.data.updated_date
        ElMessage.success('Update success')
      }
    } catch (e) {
      ElMessage.error('Update failed')
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
    searchInfluencers,
    updateInfluencer
  }
})