<template>
  <div class="influencer-search" v-loading="loading" element-loading-text="加载中..." element-loading-spinner="el-icon-loading">
    <h1 class="title">网红搜索</h1>
    <div class="form-card">
      <el-form
        :inline="true"
        :model="form"
        :rules="rules"
        ref="formRef"
        @submit.prevent="onSearch"
        class="form"
      >
        <el-form-item label="用户名" prop="handle">
          <el-input
            v-model="form.handle"
            placeholder="请输入TikTok用户名"
            clearable
            class="input"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSearch" class="search-button">
            查询
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-alert
      v-if="errorMsg"
      :title="errorMsg"
      type="error"
      show-icon
      class="error-alert"
    />

    <div v-if="influencer" class="result-card">
      <h2 class="result-title">网红信息</h2>
      <el-table :data="[influencer]" style="width: 100%" border>
        <el-table-column prop="handle" label="用户名" />
        <el-table-column prop="follower_count" label="粉丝数" />
        <el-table-column prop="video_count" label="视频数" />
        <el-table-column prop="total_play_count" label="总播放量" />
        <el-table-column prop="total_digg_count" label="总点赞数" />
        <el-table-column prop="total_comment_count" label="总评论数" />
        <el-table-column label="平均播放量">
          <template #default="scope">
            {{ avg(scope.row.total_play_count, scope.row.video_count) }}
          </template>
        </el-table-column>
        <el-table-column label="互动率">
          <template #default="scope">
            {{ percent(scope.row.total_comment_count + scope.row.total_digg_count, scope.row.total_play_count) }}
          </template>
        </el-table-column>
        <el-table-column label="评赞比">
          <template #default="scope">
            {{ percent(scope.row.total_comment_count, scope.row.total_digg_count) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="80">
          <template #default="scope">
            <el-button size="small" @click="copyRow(scope.row)">复制</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div v-if="influencer && influencer.videos && influencer.videos.length" class="videos-section">
      <h3 class="videos-title">最近30条视频列表</h3>
      <div class="videos-card">
        <el-table :data="influencer.videos" border>
          <el-table-column label="视频ID" prop="id" />
          <el-table-column label="标题">
            <template #default="scope">
              {{ scope.row.desc || '-' }}
            </template>
          </el-table-column>
          <el-table-column label="播放量" prop="stats.playCount" />
          <el-table-column label="点赞数" prop="stats.diggCount" />
          <el-table-column label="评论数" prop="stats.commentCount" />
          <el-table-column label="分享数" prop="stats.shareCount" />
          <el-table-column label="发布时间">
            <template #default="scope">
              {{ formatTime(scope.row.createTime) }}
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const form = ref({ handle: '' })
const rules = {
  handle: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ]
}
const formRef = ref()
const influencer = ref(null)
const loading = ref(false)
const errorMsg = ref('')
const API_URL = import.meta.env.VITE_API_URL

async function onSearch() {
  formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      influencer.value = null
      errorMsg.value = ''
      try {
        const res = await axios.get(`${API_URL}/api/influencers/search`, {
          params: { handle: form.value.handle }
        })
        const data = res.data
        let videos = []
        if (typeof data.videos === 'string') {
          try {
            videos = JSON.parse(data.videos)
          } catch {
            videos = []
          }
        } else if (Array.isArray(data.videos)) {
          videos = data.videos
        }
        influencer.value = {
          ...data,
          videos
        }
      } catch (e) {
        if (e.response && e.response.data && e.response.data.error) {
          errorMsg.value = e.response.data.error
        } else {
          errorMsg.value = '查询失败，请重试'
        }
        influencer.value = null
      } finally {
        loading.value = false
      }
    }
  })
}

function percent(a, b) {
  if (!b || b === 0) return '0%'
  return ((a / b) * 100).toFixed(2) + '%'
}

function avg(total, count) {
  if (!count || count === 0) return '0'
  return (total / count).toFixed(2)
}

function formatTime(ts) {
  if (!ts) return '-'
  const d = new Date(ts * 1000)
  return d.toLocaleString()
}

function copyRow(row) {
  const fields = [
    { label: '粉丝数', value: row.follower_count },
    { label: '视频数', value: row.video_count },
    { label: '总播放量', value: row.total_play_count },
    { label: '总点赞数', value: row.total_digg_count },
    { label: '总评论数', value: row.total_comment_count },
    { label: '平均播放量', value: avg(row.total_play_count, row.video_count) },
    { label: '互动率', value: percent(row.total_comment_count + row.total_digg_count, row.total_play_count) },
    { label: '评赞比', value: percent(row.total_comment_count, row.total_digg_count) }
  ]
  const text = fields.map(f => f.value).join('\t')
  navigator.clipboard.writeText(text).then(() => {
    ElMessage.success('已复制表格内容！')
  }).catch(() => {
    ElMessage.error('复制失败')
  })
}
</script>