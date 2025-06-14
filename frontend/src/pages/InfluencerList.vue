<template>
  <div v-if="store.loading">加载中...</div>
  <div v-else-if="store.error">错误：{{ store.error }}</div>
  <el-table v-else :data="store.influencers">
    <el-table-column prop="handle" label="Handle" />
    <el-table-column prop="follower_count" label="粉丝数" />
    <el-table-column prop="video_count" label="视频数" />
    <el-table-column prop="total_play_count" label="总播放量" />
    <el-table-column prop="total_comment_count" label="总评论数" />
    <el-table-column prop="total_digg_count" label="总点赞数" />
    <el-table-column prop="content_type" label="内容类型" />
    <el-table-column prop="updated_date" label="更新时间">
      <template #default="scope">
        <span>
          {{ scope.row.updated_date ? new Date(scope.row.updated_date).toLocaleString() : '' }}
        </span>
      </template>
    </el-table-column>
  </el-table>
  <el-pagination
    v-if="store.pages > 1"
    :current-page="store.page"
    :page-size="store.perPage"
    :total="store.total"
    :page-count="store.pages"
    layout="prev, pager, next, jumper"
    @current-change="onPageChange"
    style="margin-top: 20px; text-align: right;"
  />
</template>

<script setup>
import { onMounted } from 'vue'
import { useInfluencerStore } from '../store/influencer'
const store = useInfluencerStore()

function onPageChange(page) {
  store.fetchInfluencers({ page, perPage: store.perPage })
}

onMounted(() => {
  store.fetchInfluencers({ page: 1, perPage: store.perPage })
})
</script>