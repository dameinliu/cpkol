<!-- filepath: /Users/damien/Documents/Coding/full_stack/cpkol/frontend/src/views/TrendingVideos.vue -->
<template>
  <div class="trending-videos" v-loading="loading" element-loading-text="加载中..." element-loading-spinner="el-icon-loading">
    <h1 class="title">热门视频</h1>
    <el-card class="form-card">
      <el-form :inline="true" class="form">
        <el-form-item label="选择国家">
          <el-select v-model="country" placeholder="请选择国家" class="country-select">
            <el-option label="美国" value="us"></el-option>
            <el-option label="泰国" value="th"></el-option>
            <el-option label="越南" value="vn"></el-option>
            <el-option label="马来西亚" value="my"></el-option>
            <el-option label="印度尼西亚" value="id"></el-option>
            <el-option label="菲律宾" value="ph"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchVideos">获取视频</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-alert
      v-if="errorMsg"
      :title="errorMsg"
      type="error"
      show-icon
      class="error-alert"
    />
    <el-card v-else class="videos-card">
      <el-table :data="videos" style="width: 100%" border>
        <el-table-column label="视频ID" prop="id" />
        <el-table-column label="标题" prop="desc" />
        <el-table-column label="播放量" prop="stats.playCount" />
        <el-table-column label="点赞数" prop="stats.diggCount" />
        <el-table-column label="评论数" prop="stats.commentCount" />
        <el-table-column label="分享数" prop="stats.shareCount" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const country = ref('th') // 默认选择泰国
const videos = ref([])
const loading = ref(false)
const errorMsg = ref('')
const API_URL = import.meta.env.VITE_API_URL

async function fetchVideos() {
  loading.value = true // 开启加载状态
  errorMsg.value = ''
  videos.value = []
  try {
    const res = await axios.get(`${API_URL}/api/videos`, {
      params: { country: country.value }
    })
    videos.value = res.data
    console.log('获取到的视频数据:', videos.value)
  } catch (e) {
    errorMsg.value = '获取视频失败，请重试'
  } finally {
    loading.value = false // 关闭加载状态
  }
}
</script>

<style scoped>
.trending-videos {
  padding: 20px;
}

.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
}

.form-card {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.form {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.country-select {
  width: 200px;
}

.error-alert {
  margin-top: 20px;
}

.videos-card {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
}
</style>