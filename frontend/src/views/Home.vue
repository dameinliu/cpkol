<template>
  <div class="home">
    <header class="navbar">
      <div class="logo">CYPRESS MEDIA</div>
      <nav>
        <router-link to="/" exact>Home</router-link>
        <a href="#solutions">Solutions</a>
        <a href="#values">Values</a>
        <a href="#contact">Contact</a>
        <template v-if="isLogin">
          <router-link to="/influencer-search">网红搜索</router-link>
          <router-link to="/trending-videos">热门视频</router-link>
        </template>
      </nav>
      <div class="login-area">
        <template v-if="!isLogin">
          <button class="login-btn" @click="showLogin = true">Login</button>
        </template>
        <template v-else>
          <span class="user">{{ username }}</span>
          <button class="logout-btn" @click="logout">Logout</button>
        </template>
      </div>
    </header>

    <!-- 登录弹窗 -->
    <div v-if="showLogin" class="login-modal">
      <div class="login-dialog">
        <h3>Login</h3>
        <form @submit.prevent="onLogin">
          <div class="form-group">
            <label>Username</label>
            <input v-model="loginForm.username" type="text" placeholder="Please enter your username" />
            <div v-if="loginError.username" class="error">{{ loginError.username }}</div>
          </div>
          <div class="form-group">
            <label>Password</label>
            <input v-model="loginForm.password" type="password" placeholder="Please enter your password" />
            <div v-if="loginError.password" class="error">{{ loginError.password }}</div>
          </div>
          <div class="form-actions">
            <button type="submit" class="login-btn">Login</button>
            <button type="button" class="logout-btn" @click="showLogin = false">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-bg-text">CYPRESS</div>
      <h1>360° Digital<br>Commerce Made Easy.</h1>
      <p class="hero-sub">Simplify. Elevate. Aspire.</p>
    </section>

    <!-- Solutions Section -->
    <section id="solutions" class="solutions">
      <h2>Our Solutions Suite</h2>
      <div class="solution-list">
        <div class="solution-card">
          <div class="icon-circle">S</div>
          <h3>CYPRESS/Social</h3>
          <p>One-stop social commerce powered by our data-driven framework.</p>
        </div>
        <div class="solution-card">
          <div class="icon-circle">St</div>
          <h3>CYPRESS/Studios</h3>
          <p>Full-service, full-funnel creative & production that drives the right metrics.</p>
        </div>
        <div class="solution-card">
          <div class="icon-circle">B</div>
          <h3>CYPRESS/Brands</h3>
          <p>360° Multi-Channel Service for end-to-end e-commerce management.</p>
        </div>
      </div>
    </section>

    <!-- Values Section -->
    <section id="values" class="values">
      <h2>Our Values</h2>
      <div class="values-list">
        <div class="value-card">
          <div class="value-icon">A</div>
          <strong>AUTHENTICITY</strong>
          <span>We stay true to our purpose by constantly elevating the standards of everything that we do.</span>
        </div>
        <div class="value-card">
          <div class="value-icon">I</div>
          <strong>INSPIRATION</strong>
          <span>Our passion for excellence inspires those around us to be better.</span>
        </div>
        <div class="value-card">
          <div class="value-icon">R</div>
          <strong>RESILIENCE</strong>
          <span>This courage empowers us to turn failures into opportunities.</span>
        </div>
        <div class="value-card">
          <div class="value-icon">R</div>
          <strong>RESPECT</strong>
          <span>We treat others how we would like to be treated.</span>
        </div>
      </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="contact">
      <h2>Contact & Locations</h2>
      <ul>
        <li><strong>Thailand:</strong> no. 51/2, Oasis Loft Sukhumvit 64 Project, Soi Phongwet Anusorn School, Phra Khanong Tai Subdistrict, Phra Khanong District, Bangkok 10260</li>
        <li><strong>Email:</strong> damien@cypressmedia.cn</li>
      </ul>
    </section>

    <footer>
      <p>© 2025 CYPRESS MEDIA. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isLogin = ref(false)
const username = ref('用户')
const showLogin = ref(false)
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
  isLogin.value = true
  username.value = loginForm.value.username
  // 存储到localStorage
  localStorage.setItem('user', JSON.stringify({ username: username.value }))
  showLogin.value = false
  // 清空表单
  loginForm.value = { username: '', password: '' }
}

function logout() {
  isLogin.value = false
  username.value = ''
  localStorage.removeItem('user')
}

onMounted(() => {
  const user = localStorage.getItem('user')
  if (user) {
    const userObj = JSON.parse(user)
    isLogin.value = true
    username.value = userObj.username
  }
})
</script>

<style scoped>
.home {
  font-family: 'Inter', Arial, sans-serif;
  color: #222;
  background: #fff;
}
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 4vw;
  background: #fff;
  border-bottom: 1px solid #eee;
}
.logo {
  font-size: 2rem;
  font-weight: bold;
  letter-spacing: 2px;
}
.navbar nav {
  display: flex;
  align-items: center;
}
.navbar nav a,
.navbar nav .router-link-active {
  margin-left: 2rem;
  color: #222;
  text-decoration: none;
  font-weight: 500;
}
.router-link-exact-active {
  color: #27ae60;
  font-weight: bold;
}
.login-area {
  display: flex;
  align-items: center;
  margin-left: 2rem;
}
.login-btn {
  background: none;
  color: #222;
  border: none;
  border-radius: 0;
  padding: 0.5rem 1.2rem 0.5rem 1.2rem;
  margin-left: 1rem;
  cursor: pointer;
  font-size: 1.08rem;
  font-weight: 600;
  box-shadow: none;
  text-decoration: underline;
  transition: color 0.2s;
}
.login-btn:hover, .login-btn:focus {
  color: #27ae60;
  background: none;
  text-decoration: underline;
  transform: none;
  box-shadow: none;
}
.logout-btn {
  background: none;
  color: #222;
  border: none;
  border-radius: 24px;
  padding: 0.5rem 1.5rem;
  margin-left: 1rem;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: color 0.2s;
}
.logout-btn:hover, .logout-btn:focus {
  background: none;
  color: #27ae60;
}
.user {
  color: #27ae60;
  font-weight: bold;
}
/* 登录弹窗样式 */
.login-modal {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.login-dialog {
  background: #fff;
  border-radius: 8px;
  padding: 2rem 2.5rem 1.5rem 2.5rem;
  min-width: 320px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.12);
}
.form-group {
  margin-bottom: 1.2rem;
}
.form-group label {
  display: block;
  margin-bottom: 0.3rem;
  font-weight: 500;
}
.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}
.error {
  color: #e74c3c;
  font-size: 0.95rem;
  margin-top: 0.2rem;
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.2rem;
}
/* Hero Section */
.hero {
  position: relative;
  text-align: center;
  padding: 7rem 2vw 4rem 2vw;
  background: #111;
  color: #fff;
  overflow: hidden;
}
.hero-bg-text {
  position: absolute;
  top: 30px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 8rem;
  color: rgba(39,174,96,0.07);
  font-weight: 900;
  letter-spacing: 10px;
  pointer-events: none;
  user-select: none;
  z-index: 0;
}
.hero h1 {
  font-size: 3.2rem;
  margin-bottom: 1.2rem;
  letter-spacing: 2px;
  position: relative;
  z-index: 1;
}
.hero-sub {
  font-size: 1.6rem;
  color: #b2ffb2;
  position: relative;
  z-index: 1;
}
/* Solutions Section */
.solutions {
  padding: 5rem 2vw 5rem 2vw;
  text-align: center;
  background: #fff;
}
.solutions h2 {
  color: #222;
  margin-bottom: 2.5rem;
  font-size: 2.2rem;
  letter-spacing: 1px;
}
.solution-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2.5rem;
  margin-top: 2rem;
}
.solution-card {
  background: #fff;
  border-radius: 20px;
  padding: 2.5rem 2rem 2rem 2rem;
  width: 320px;
  box-shadow: 0 4px 32px rgba(39,174,96,0.10);
  color: #222;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.solution-card:hover {
  transform: translateY(-8px) scale(1.04);
  box-shadow: 0 12px 48px rgba(39,174,96,0.18);
}
.icon-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #27ae60 60%, #00c48c 100%);
  color: #fff;
  font-size: 2rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.2rem;
  box-shadow: 0 2px 8px rgba(39,174,96,0.10);
}
/* Values Section */
.values {
  background: linear-gradient(90deg, #f7fff7 0%, #eaffea 100%);
  padding: 5rem 2vw;
  text-align: center;
}
.values h2 {
  color: #27ae60;
  margin-bottom: 2.5rem;
  font-size: 2.2rem;
  letter-spacing: 1px;
}
.values-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
  margin-top: 2rem;
}
.value-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 16px rgba(39,174,96,0.07);
  padding: 2rem 1.5rem;
  width: 260px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.value-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #27ae60;
  color: #fff;
  font-size: 1.3rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.8rem;
  box-shadow: 0 1px 4px rgba(39,174,96,0.10);
}
.value-card strong {
  color: #27ae60;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}
.value-card span {
  color: #444;
  font-size: 1rem;
}
/* Contact Section */
.contact {
  padding: 4rem 2vw;
  text-align: center;
  background: #111;
  color: #fff;
}
.contact h2 {
  color: #b2ffb2;
}
.contact ul {
  list-style: none;
  padding: 0;
  margin: 2rem auto 0 auto;
  max-width: 700px;
}
.contact li {
  margin-bottom: 1rem;
}
/* Footer */
footer {
  text-align: center;
  padding: 2rem 0;
  background: #111;
  color: #b2ffb2;
  margin-top: 0;
  letter-spacing: 1px;
}
@media (max-width: 900px) {
  .solution-list, .values-list {
    flex-direction: column;
    align-items: center;
  }
  .hero-bg-text {
    font-size: 3rem;
    top: 10px;
  }
}
</style>
