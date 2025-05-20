<template>
  <el-form :inline="true" @submit.prevent="onSearch">
    <el-form-item label="关键词">
      <el-input v-model="keyword" placeholder="输入TikTok用户名"></el-input>
    </el-form-item>
    <el-form-item label="最小粉丝数">
      <el-input-number v-model="minFans" :min="0"></el-input-number>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSearch">搜索</el-button>
    </el-form-item>
  </el-form>
  <div>
    <h1>粉丝数：{{ store.influencers.followerCount }}</h1>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useInfluencerStore } from '../store/influencer'

const keyword = ref('')
const minFans = ref(0)
const store = useInfluencerStore()

function onSearch() {
  store.searchInfluencers({ keyword: keyword.value, min_fans: minFans.value })
}
</script>