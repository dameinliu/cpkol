<template>
  <el-header>
    <el-menu
      :default-active="$route.path"
      mode="horizontal"
      :ellipsis="false"
      router
    >
      <el-menu-item class="text-2xl font-bold">CYPRESS MEDIA</el-menu-item>
      <el-menu-item index="/" @click="handleSelect('/InfluencerList')">Home</el-menu-item>
      <el-sub-menu index="1">
        <template #title>Influencer</template>
        <el-menu-item index="/InfluencerList" @click="handleSelect('/InfluencerList')">Influencer List</el-menu-item>
        <el-menu-item index="/InfluencerSearch" @click="handleSelect('/InfluencerSearch')">Influencer Search</el-menu-item>
      </el-sub-menu>
      <!-- <el-sub-menu index="2">
        <template #title>Videos</template>
        <el-menu-item index="/TrendingVideos" @click="handleSelect('/TrendingVideos')">Trending Videos</el-menu-item>
      </el-sub-menu> -->
      <el-menu-item>
        <ThemeSwitch />
      </el-menu-item>
      <el-menu-item>
        <template v-if="!isLogin">
          <el-button type="primary" @click="showLogin = true">Login</el-button>
        </template>
        <template v-else>
          <el-dropdown>
            <span class="cursor-pointer">
              {{ username }}<i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="logout">Logout</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
      </el-menu-item>
    </el-menu>
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

<style scoped>
.el-menu--horizontal > .el-menu-item:nth-child(1) {
  margin-right: auto;
}
</style> 