<template>
  <el-container>
    <el-header>
      <div class="nav-bar">
        <div class="logo">CYPRESS MEDIA</div>
        <el-menu class="nav-menu" :default-active="$route.path" mode="horizontal" router background-color="#fff" text-color="#222" active-text-color="#27ae60">
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/influencer-list">网红列表</el-menu-item>
          <el-menu-item index="/influencer-search">网红搜索</el-menu-item>
          <el-menu-item index="/trending-videos">热门视频</el-menu-item>
        </el-menu>
        <div class="nav-actions">
          <template v-if="!isLogin">
            <span class="login-link" @click="showLogin = true">登录</span>
          </template>
          <template v-else>
            <span class="user-name">{{ username }}</span>
            <span class="logout-link" @click="logout">退出</span>
          </template>
        </div>
      </div>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
    <el-dialog v-model="showLogin" title="登录" width="340px" :close-on-click-modal="false">
      <el-form :model="loginForm" :rules="loginRules" ref="loginFormRef" label-width="60px" @submit.prevent>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" autocomplete="off" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="password" autocomplete="off" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showLogin = false">取消</el-button>
        <el-button type="primary" @click="onLogin">登录</el-button>
      </template>
    </el-dialog>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const showLogin = ref(false)
const isLogin = ref(false)
const username = ref('')
const loginForm = ref({ username: '', password: '' })
const loginFormRef = ref()
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

function onLogin() {
  loginFormRef.value.validate((valid) => {
    if (valid) {
      // 简单演示：用户名admin，密码123456
      if (loginForm.value.username === 'admin' && loginForm.value.password === '123456') {
        isLogin.value = true
        username.value = loginForm.value.username
        showLogin.value = false
        ElMessage.success('登录成功')
      } else {
        ElMessage.error('用户名或密码错误')
      }
    }
  })
}

function logout() {
  isLogin.value = false
  username.value = ''
  ElMessage.success('已退出登录')
}
</script>

<style scoped>
:root {
  --main-green: #27ae60;
  --main-bg: #f7fff7;
  --main-font: 'Inter', Arial, sans-serif;
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