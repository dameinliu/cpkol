<template>
  <el-header>
    <div class="flex items-center justify-between w-full">
      <el-menu
        :default-active="$route.path"
        mode="horizontal"
        router
        background-color="#fff"
        text-color="#222"
        active-text-color="#27ae60"
        class="flex-1 ml-10"
      >
        <el-menu-item class="text-2xl font-bold">CYPRESS MEDIA</el-menu-item>
        <el-menu-item index="/" @click="handleSelect('/InfluencerList')">首页</el-menu-item>
        <el-menu-item index="/InfluencerList" @click="handleSelect('/InfluencerList')">网红列表</el-menu-item>
        <el-menu-item index="/InfluencerSearch" @click="handleSelect('/InfluencerSearch')">网红搜索</el-menu-item>
        <el-menu-item index="/TrendingVideos" @click="handleSelect('/TrendingVideos')">热门视频</el-menu-item>
      </el-menu>
      <div class="ml-auto mr-10 flex items-center">
        <template v-if="!isLogin">
          <el-button type="primary" class="ml-10" @click="showLogin = true">Login</el-button>
        </template>
        <template v-else>
          <el-dropdown>
            <span class="ml-10 cursor-pointer">
              {{ username }}<i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="logout">Logout</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
      </div>
    </div>
  </el-header>
  <LoginDialog v-model:visible="showLogin" @login-success="onLoginSuccess" />
</template>

<script setup lang="ts">
const router = useRouter()
const showLogin = ref(false)
const isLogin = ref(false)
const username = ref('')

const handleSelect = (path: string) => {
  router.push(path)
}

const onLoginSuccess = (name: string) => {
  isLogin.value = true
  username.value = name
  showLogin.value = false
  ElMessage.success('登录成功')
}

const logout = () => {
  isLogin.value = false
  username.value = ''
  ElMessage.success('已退出登录')
}
</script>

<style scoped lang="scss">
</style> 