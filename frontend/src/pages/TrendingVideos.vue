<!-- filepath: /Users/damien/Documents/Coding/full_stack/cpkol/frontend/src/views/TrendingVideos.vue -->
<template>
  <div v-loading="videoStore.loading" element-loading-text="Loading..." element-loading-spinner="el-icon-loading">
    <el-form :model="form" :inline="true" class="flex justify-center items-center">
      <el-form-item label="Trending Videos" class="min-w-[300px]">
        <el-select v-model="form.country" placeholder="Please select a country">
          <el-option label="America" value="us"></el-option>
          <el-option label="Thailand" value="th"></el-option>
          <el-option label="Vietnam" value="vn"></el-option>
          <el-option label="Malaysia" value="my"></el-option>
          <el-option label="Indonesia" value="id"></el-option>
          <el-option label="Philippines" value="ph"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="fetchVideos">Get Videos</el-button>
      </el-form-item>
    </el-form>

    <el-alert
      v-if="videoStore.errorMsg"
      :title="videoStore.errorMsg"
      type="error"
      show-icon
    />
    <el-card v-else>
      <el-table :data="videoStore.videos" stripe border class="max-h-2xl">
        <el-table-column label="视频ID" prop="id" />
        <el-table-column label="标题" show-overflow-tooltip prop="desc" />
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
import { useVideoStore } from '@/store/video'

const form = ref({
  country: 'th'
})

const videoStore = useVideoStore()

async function fetchVideos() {
  await videoStore.fetchVideos(form.value.country)
} 
</script>