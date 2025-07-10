<template>
  <div v-loading="loading" element-loading-text="Loading..." element-loading-spinner="el-icon-loading">
    <div v-if="error">Error: {{ error }}</div>
    <el-table v-else :data="influencers" border stripe>
      <el-table-column prop="handle" label="Handle" />
      <el-table-column prop="follower_count" label="Followers" />
      <el-table-column label="Avg. Plays">
        <template #default="scope">
          {{ avg(scope.row.total_play_count, scope.row.video_count) }}
        </template>
      </el-table-column>
      <el-table-column label="Engagement Rate">
        <template #default="scope">
          {{ percent(scope.row.total_digg_count + scope.row.total_comment_count, scope.row.total_play_count) }}
        </template>
      </el-table-column>
      <el-table-column label="C/L">
        <template #default="scope">
          {{ percent(scope.row.total_comment_count, scope.row.total_digg_count) }}
        </template>
      </el-table-column>
      <el-table-column prop="content_type" label="Content Type" width="200">
        <template #default="scope">
          <el-select
            v-model="scope.row.content_type"
            @change="onContentChange(scope.row)"
            multiple
            clearable
          >
            <el-option label="Beauty" value="beauty" />
            <el-option label="Fashion" value="fashion" />
            <el-option label="Pet" value="pet" />
            <el-option label="Travel" value="travel" />
            <el-option label="Tech" value="tech" />
            <el-option label="Sports" value="sports" />
            <el-option label="Music" value="music" />
            <el-option label="Art" value="art" />
            <el-option label="Gaming" value="gaming" />
            <el-option label="Education" value="education" />
            <el-option label="Other" value="other" />
          </el-select>
        </template>
      </el-table-column>
      <el-table-column prop="note" label="Note" width="200">
        <template #default="scope">
          <el-input
            v-model="noteCache[scope.row.handle]"
            placeholder="Note"
            @keyup.enter="onNoteEnter(scope.row)"
          />
        </template>
      </el-table-column>
      <el-table-column prop="updated_date" label="Updated Date">
        <template #default="scope">
          <span>
            {{ formatTime(scope.row.updated_date) }}
          </span>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      v-if="pages > 1"
      :current-page="page"
      :page-size="perPage"
      :total="total"
      :page-count="pages"
      layout="prev, pager, next, jumper"
      @current-change="onPageChange"
      class="flex justify-center mt-8"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, watch, reactive, ref } from 'vue'
import { useInfluencerStore, Influencer } from '../store/influencer'
import { percent, avg, formatTime } from '../utils/utils'
import { ElMessage } from 'element-plus'

const influencerStore = useInfluencerStore()

// 本地变量存储数据
const influencers = ref<Influencer[]>([])
const loading = ref(false)
const error = ref('')
const page = ref(1)
const perPage = ref(import.meta.env.VITE_PER_PAGE || 12)
const total = ref(0)
const pages = ref(1)

// note 缓存
const noteCache = reactive<Record<string, string>>({})

// 初始化缓存
watch(
  () => influencers.value,
  (list) => {
    list.forEach(i => {
      noteCache[i.handle] = i.note || ''
    })
  },
  { immediate: true, deep: true }
)

// content_type 格式化
watch(
  () => influencers.value,
  (list) => {
    list.forEach(i => {
      if (typeof i.content_type === 'string') {
        i.content_type = i.content_type.split(',').filter(Boolean)
      }
    })
  },
  { immediate: true, deep: true }
)

async function fetchInfluencers({ page: p, perPage: pp }) {
  loading.value = true
  error.value = ''
  try {
    const res = await influencerStore.fetchInfluencers({ page: p, perPage: pp })
    // 后端返回 { items, total, page, per_page, pages }
    if (res && Array.isArray(res.items)) {
      influencers.value = res.items
      page.value = res.page || 1
      perPage.value = res.per_page || 20
      total.value = res.total || 0
      pages.value = res.pages || 1
    } else {
      influencers.value = []
      ElMessage.error('No KOLs found')
    }
  } catch (e: any) {
    error.value = e.message || 'Failed to fetch KOLs'
    influencers.value = []
  } finally {
    loading.value = false
  }
}

function onPageChange(p) {
  fetchInfluencers({ page: p, perPage: perPage.value })
}

function onContentChange(row) {
  influencerStore.updateInfluencer(row.handle, row.content_type, noteCache[row.handle])
}

function onNoteEnter(row) {
  influencerStore.updateInfluencer(row.handle, row.content_type, noteCache[row.handle])
}

onMounted(() => {
  fetchInfluencers({ page: 1, perPage: perPage.value })
})
</script>