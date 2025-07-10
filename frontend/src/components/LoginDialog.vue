<template>
  <el-dialog
    :model-value="visible"
    title="登录"
    width="400px"
    @close="close"
    :close-on-click-modal="false"
    :close-on-press-escape="true"
    center
  >
    <form @submit.prevent="onLogin">
      <div class="form-group">
        <label>Username</label>
        <el-input v-model="loginForm.username" placeholder="请输入用户名" />
        <div v-if="loginError.username" class="error">{{ loginError.username }}</div>
      </div>
      <div class="form-group">
        <label>Password</label>
        <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" />
        <div v-if="loginError.password" class="error">{{ loginError.password }}</div>
      </div>
      <div class="form-actions">
        <el-button type="primary" native-type="submit">Login</el-button>
        <el-button @click="close" style="margin-left: 8px;">Cancel</el-button>
        <el-button type="success" @click="onFeishuLogin" style="margin-left: 8px;">飞书登录</el-button>
      </div>
    </form>
  </el-dialog>
</template>

<script setup lang="ts">
const props = defineProps({
  visible: Boolean
})
const emit = defineEmits(['update:visible', 'login-success'])

const loginForm = ref({ username: '', password: '' })
const loginError = ref({ username: '', password: '' })

function validateLogin() {
  let valid = true
  loginError.value = { username: '', password: '' }
  if (!loginForm.value.username) {
    loginError.value.username = '用户名不能为空'
    valid = false
  } else if (loginForm.value.username !== 'admin') {
    loginError.value.username = '用户名不存在'
    valid = false
  }
  if (!loginForm.value.password) {
    loginError.value.password = '密码不能为空'
    valid = false
  } else if (loginForm.value.password.length < 6) {
    loginError.value.password = '密码长度不能少于6位'
    valid = false
  } else if (loginForm.value.password !== '123456') {
    loginError.value.password = '密码错误'
    valid = false
  }
  return valid
}

function onLogin() {
  if (!validateLogin()) return
  emit('login-success', loginForm.value.username)
  close()
  loginForm.value = { username: '', password: '' }
}

function close() {
  emit('update:visible', false)
}

function onFeishuLogin() {
  window.location.href = '/api/feishu/oauth/login';
}
</script>

<style scoped>
.form-group {
  margin-bottom: 18px;
}
.error {
  color: #e74c3c;
  font-size: 0.95em;
  margin-top: 4px;
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 18px;
}
</style> 