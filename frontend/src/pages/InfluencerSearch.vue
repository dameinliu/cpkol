<template>
  <el-main>
    <div v-loading="influencerStore.loading" element-loading-text="Loading..." element-loading-spinner="el-icon-loading">
      <div>
        <el-form
          :inline="true"
          :model="form"
          :rules="rules"
          ref="formRef"
          @submit.prevent="onSearch"
          class="w-full flex justify-center items-center"
        >
          <el-form-item prop="handle" class="w-1/2">
            <el-input
              v-model="form.handle"
              placeholder="请输入TikTok用户名，多个用英文逗号隔开"
              clearable
              class="h-12"
            >
              <template #prepend>@Handle</template>
              <template #append>
                <el-button type="primary" @click="onSearch">
                  Search
                </el-button>
              </template>
            </el-input>
          </el-form-item>
        </el-form>
      </div>

      <el-alert
        v-if="influencerStore.errorMsg"
        :title="influencerStore.errorMsg"
        type="error"
        show-icon
      />

      <div v-if="influencerStore.influencers.length" class="result-card">
        <div class="flex justify-end mb-4">
          <el-button type="primary" @click="copyAll" class="btn">一键复制所有行</el-button>
        </div>
        <el-table :data="influencerStore.influencers" style="width: 100%" border>
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

      <div v-if="influencerStore.influencers && influencerStore.influencers.videos && influencerStore.influencers.videos.length" class="videos-section">
        <h3 class="videos-title">最近30条视频列表</h3>
        <div class="videos-card">
          <el-table :data="influencerStore.influencers.videos" border>
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

      <el-alert
        v-for="err in influencerStore.errorList"
        :key="err.handle"
        :title="`${err.handle}: ${err.error}`"
        type="error"
        show-icon
        class="error-alert"
      />
    </div>
  </el-main>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useInfluencerStore } from '../store/influencer'
import { percent, avg, formatTime } from '../utils/utils'

const influencerStore = useInfluencerStore()
const form = ref({ handle: '' })
const rules = {
  handle: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ]
}
const formRef = ref()

async function onSearch() {
  formRef.value.validate(async (valid) => {
    if (valid) {
      await influencerStore.searchInfluencers({ keyword: form.value.handle })
    }
  })
}

function copyRow(row) {
  const fields = [
    { label: '用户名', value: row.handle },
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

function copyAll() {
  if (!influencerStore.influencers.length) {
    ElMessage.warning('没有可复制的数据')
    return
  }
  // 不需要header，直接拼接数据
  const rows = influencerStore.influencers.map(row => [
    row.handle,
    row.follower_count,
    row.video_count,
    row.total_play_count,
    row.total_digg_count,
    row.total_comment_count,
    avg(row.total_play_count, row.video_count),
    percent(row.total_comment_count + row.total_digg_count, row.total_play_count),
    percent(row.total_comment_count, row.total_digg_count)
  ].join('\t'))
  const text = rows.join('\n')
  navigator.clipboard.writeText(text).then(() => {
    ElMessage.success('已复制所有行！')
  }).catch(() => {
    ElMessage.error('复制失败')
  })
}
</script>