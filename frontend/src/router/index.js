import { createRouter, createWebHistory } from 'vue-router'
import InfluencerSearch from '../views/InfluencerSearch.vue'
import InfluencerList from '../views/InfluencerList.vue'

const routes = [
  { path: '/', component: InfluencerSearch },
  { path: '/list', component: InfluencerList }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router