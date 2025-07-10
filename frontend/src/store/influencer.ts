import { defineStore } from 'pinia'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const API_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5001'

export interface Influencer {
  handle: string,
  follower_count: number,
  total_play_count: number,
  total_comment_count: number,
  total_digg_count: number,
  video_count: number,
  videos: any[],
  content_type: string[] | string,
  note: string,
  updated_date: string,
  dirty?: boolean
}

export const useInfluencerStore = defineStore('influencer', () => {
  async function searchInfluencers(keywords: Array<string>) {
    try {
        const res = await axios.get(`${API_URL}/kol/search`, {
          params: { keywords: keywords.join(',') }
        })
        
        return res.data
      } catch (e) {
        return e.message
      }
    }
    
  async function fetchInfluencers({ page: p = 1, perPage: pp = 12} = {}) {
    try {
      const res = await axios.get(`${API_URL}/kol/list`, {
        params: { page: p, per_page: pp }
      })
      return res.data
    } catch (e) {
      return e.message
    }
  }

  // 单行更新数据
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
    }
  }

  return {
    fetchInfluencers,
    searchInfluencers,
    updateInfluencer
  }
})