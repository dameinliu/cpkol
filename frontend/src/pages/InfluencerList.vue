<template>
  <div v-loading="influencerStore.loading" element-loading-text="Loading..." element-loading-spinner="el-icon-loading">
    <div v-if="influencerStore.error">Error: {{ influencerStore.error }}</div>
    <el-table v-else :data="influencerStore.influencers" border stripe>
      <el-table-column prop="handle" label="Handle" />
      <el-table-column prop="follower_count" label="Followers" />
      <!-- <el-table-column prop="video_count" label="Videos" /> -->
      <!-- <el-table-column prop="total_play_count" label="Total Plays" /> -->
      <!-- <el-table-column prop="total_comment_count" label="Total Comments" /> -->
      <!-- <el-table-column prop="total_digg_count" label="Total Diggs" /> -->
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
      <el-table-column prop="updated_date" label="Updated Date">
        <template #default="scope">
          <span>
            {{ formatTime(scope.row.updated_date) }}
          </span>
        </template>
      </el-table-column>
  </el-table>
  <el-pagination
    v-if="influencerStore.pages > 1"
    :current-page="influencerStore.page"
    :page-size="influencerStore.perPage"
    :total="influencerStore.total"
    :page-count="influencerStore.pages"
    layout="prev, pager, next, jumper"
    @current-change="onPageChange"
    class="flex justify-center mt-8"
  />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useInfluencerStore } from '../store/influencer'
import { percent, avg, formatTime } from '../utils/utils'

const influencerStore = useInfluencerStore()

function onPageChange(page) {
  influencerStore.fetchInfluencers({ page, perPage: influencerStore.perPage })
}

function onContentChange(row) {
  influencerStore.updateInfluencer(row.handle, row.content_type, row.note)
}

onMounted(() => {
  influencerStore.fetchInfluencers({ page: 1, perPage: influencerStore.perPage })
})
</script>