<template>
  <el-container>
    <el-header>
      <div class="nav-bar" style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
        <div class="logo" style="font-weight: bold; font-size: 1.4rem; letter-spacing: 2px; margin-left: 100px;">CYPRESS MEDIA</div>
        <el-menu
          :default-active="$route.path"
          mode="horizontal"
          router
          background-color="#fff"
          text-color="#222"
          active-text-color="#27ae60"
          style="flex: 1; margin-left: 40px;"
        >
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/influencer-list">网红列表</el-menu-item>
          <el-menu-item index="/influencer-search">网红搜索</el-menu-item>
          <el-menu-item index="/trending-videos">热门视频</el-menu-item>
        </el-menu>
        <div class="nav-actions" style="margin-left: auto; margin-right: 100px; display: flex; align-items: center;">
          <template v-if="!isLogin">
            <el-button type="primary" class="login-btn" style="margin-left: 16px;" @click="showLogin = true">Login</el-button>
          </template>
          <template v-else>
            <el-dropdown>
              <span class="user-name el-dropdown-link" style="margin-left: 16px; cursor: pointer;">
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
    <el-main>
      <router-view />
    </el-main>
    <LoginDialog v-model:visible="showLogin" @login-success="onLoginSuccess" />
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import LoginDialog from '@/components/LoginDialog.vue'

const showLogin = ref(false)
const isLogin = ref(false)
const username = ref('')

function onLoginSuccess(name) {
  isLogin.value = true
  username.value = name
  showLogin.value = false
  ElMessage.success('登录成功')
}

function logout() {
  isLogin.value = false
  username.value = ''
  ElMessage.success('已退出登录')
}
</script>

<style scoped>
.el-menu--horizontal .el-menu-item:nth-child(1) {
  /* margin-right: auto; */
}
.el-header {
  background: #fff;
  box-shadow: 0 2px 8px #f0f1f2;
  padding: 0;
  min-height: 60px;
  display: flex;
  align-items: center;
}
.el-main {
  padding: 32px 4vw 32px 4vw;
  background: var(--main-bg);
  min-height: calc(100vh - 60px);
  font-family: var(--main-font);
}
body {
  font-family: var(--main-font);
  background: var(--main-bg);
  color: #222;
}
.login-link {
  color: var(--main-green);
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  padding: 0 12px;
  transition: color 0.2s;
}
.login-link:hover {
  color: #219150;
  text-decoration: underline;
}
.user-name {
  color: var(--main-green);
  font-weight: 600;
  margin-right: 12px;
}
.logout-link {
  color: #e74c3c;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  padding: 0 12px;
  transition: color 0.2s;
}
.logout-link:hover {
  color: #b93222;
  text-decoration: underline;
}
</style>