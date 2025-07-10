<template>
  <div v-loading="loading" element-loading-text="Loading..." element-loading-spinner="el-icon-loading">
    <div class="w-full flex justify-center items-center">
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
            placeholder="Enter TikTok handle, multiple separated by commas"
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
      v-if="errorMsg"
      :title="errorMsg"
      type="error"
      show-icon
    />
    <div v-if="influencers && influencers.length">
      <div class="flex justify-end mb-4">
        <el-button type="primary" @click="copyAll">Copy All</el-button>
      </div>
      <el-table :data="influencers" style="width: 100%" border stripe>
          <el-table-column prop="handle" label="Handle">
            <template #default="scope">
              <el-link type="primary" @click="showVideos(scope.row)">
                {{ scope.row.handle }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column prop="follower_count" label="Followers" />
          <el-table-column label="Avg. Plays">
            <template #default="scope">
              {{ avg(scope.row.total_play_count, scope.row.video_count) }}
            </template>
          </el-table-column>
          <el-table-column label="ER" :sortable="true" sort-by="(total_digg_count + total_comment_count) / total_play_count">
            <template #default="scope">
              {{ percent(scope.row.total_digg_count + scope.row.total_comment_count, scope.row.total_play_count) }}
            </template>
          </el-table-column>
          <el-table-column label="C/L" :sortable="true" sort-by="(total_comment_count / total_digg_count)">
            <template #default="scope">
              {{ percent(scope.row.total_comment_count, scope.row.total_digg_count) }}
            </template>
          </el-table-column>
          <el-table-column prop="updated_date" label="Updated Date">
            <template #default="scope">
              {{ formatTime(scope.row.updated_date) }}
            </template>
          </el-table-column>
          <el-table-column label="Actions">
            <template #default="scope">
              <el-button type="text" @click="copyRow(scope.row)">Copy</el-button>
            </template>
          </el-table-column>
          <el-table-column prop="content_type" label="Content Type" width="120">
            <template #default="scope">
              <el-select
                v-model="scope.row.content_type"
                placeholder="Please select"
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
              <el-input v-model="scope.row.note" placeholder="Note" size="extra" />
            </template>
          </el-table-column>
          <el-table-column label="Actions">
            <template #default="scope">
              <el-button type="primary" @click="onContentChange(scope.row)">Update</el-button>
            </template>
          </el-table-column>
      </el-table>
    </div>

    <div v-if="selectedVideos.length" class="videos-section">
      <h3>Recent 10 videos</h3>
      <el-table :data="selectedVideos" border>
        <el-table-column label="ID" prop="id" show-overflow-tooltip />
        <el-table-column label="Title" show-overflow-tooltip>
          <template #default="scope">
            {{ scope.row.desc || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="Play Count" prop="stats.playCount" />
        <el-table-column label="Digg Count" prop="stats.diggCount" />
        <el-table-column label="Comment Count" prop="stats.commentCount" />
        <el-table-column label="Share Count" prop="stats.shareCount" />
        <el-table-column label="ER" >
          <template #default="scope">
            {{ percent(scope.row.stats.diggCount + scope.row.stats.commentCount, scope.row.stats.playCount) }}
          </template>
        </el-table-column>
        <el-table-column label="C/L">
          <template #default="scope">
            {{ percent(scope.row.stats.commentCount, scope.row.stats.diggCount) }}
          </template>
        </el-table-column>
        <el-table-column label="Created Time" :sortable="true" sort-by="stats.createTime">
          <template #default="scope">
            {{ formatTime(scope.row.createTime) }}
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useInfluencerStore, Influencer } from '../store/influencer'
import { percent, avg, formatTime } from '../utils/utils'

const influencerStore = useInfluencerStore()
const form = ref({ handle: '' })
const rules = {
  handle: [
    { required: true, message: 'Please enter TikTok handle, multiple separated by commas', trigger: 'blur' }
  ]
}
const formRef = ref()

// 本地变量存储数据
const influencers = ref<Influencer[]>([])
const loading = ref(false)
const errorMsg = ref('')
const errorList = ref([])
const selectedVideos = ref([])

async function onSearch() {
  formRef.value.validate(async (valid) => {
    if (valid) {
      const handleList = form.value.handle.split(',').map(h => h.trim()).filter(Boolean)
      loading.value = true
      errorMsg.value = ''
      errorList.value = []

      try {
        const res = await influencerStore.searchInfluencers(handleList)
        influencers.value = res.items
        console.log(influencers.value)
        errorList.value = res.errors
      } catch (e) {
        errorMsg.value = e.message || 'Failed to search'
        influencers.value = []
      } finally {
        loading.value = false
      }
    }
  })
}

function copyRow(row) {
  const fields = [
    { label: 'Handle', value: row.handle },
    { label: 'Followers', value: row.follower_count },
    { label: 'Videos', value: row.video_count },
    { label: 'Total Play', value: row.total_play_count },
    { label: 'Total Digg', value: row.total_digg_count },
    { label: 'Total Comment', value: row.total_comment_count },
    { label: 'Avg. Play', value: avg(row.total_play_count, row.video_count) },
    { label: 'Engagement Rate', value: percent(row.total_comment_count + row.total_digg_count, row.total_play_count) },
    { label: 'C/L', value: percent(row.total_comment_count, row.total_digg_count) }
  ]
  const text = fields.map(f => f.value).join('\t')
  navigator.clipboard.writeText(text).then(() => {
    ElMessage.success('已复制表格内容！')
  }).catch(() => {
    ElMessage.error('复制失败')
  })
}

function copyAll() {
  if (!searchResults.value.length) {
    ElMessage.warning('No data to copy')
    return
  }
  // 不需要header，直接拼接数据
  const rows = searchResults.value.map(row => [
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

function onContentChange(row) {
  influencerStore.updateInfluencer(row.handle, row.content_type, row.note)
}

function showVideos(row) {
  selectedVideos.value = (row.videos || []).slice(0, 10)
}
</script>