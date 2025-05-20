<template>
  <div v-if="store.loading">加载中...</div>
  <div v-else-if="store.error">错误：{{ store.error }}</div>
  <el-table v-else :data="store.influencers">
    <el-table-column prop="user.nickname" label="昵称" />
    <el-table-column prop="user.uniqueId" label="用户名" />
    <el-table-column prop="user.avatarThumb" label="头像">
      <template #default="scope">
        <img :src="scope.row.user.avatarThumb" width="50" />
      </template>
    </el-table-column>
    <el-table-column prop="stats.followerCount" label="粉丝数" />
    <el-table-column prop="stats.heartCount" label="获赞数" />
    <el-table-column prop="stats.videoCount" label="视频数" />
  </el-table>
</template>

<script setup>
import { useInfluencerStore } from '../store/influencer'
const store = useInfluencerStore()
</script>