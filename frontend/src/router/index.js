import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import InfluencerList from '../views/InfluencerList.vue'
import InfluencerSearch from '../views/InfluencerSearch.vue'
import TrendingVideos from '../views/TrendingVideos.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/influencer-list', component: InfluencerList },
  { path: '/influencer-search', component: InfluencerSearch },
  { path: '/trending-videos', component: TrendingVideos }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router