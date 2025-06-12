<template>
  <div class="home">
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
import { ref } from 'vue'

const showLogin = ref(false)
const username = ref('')

function onLoginSuccess(name) {
  username.value = name
  // 这里可以做登录后逻辑，如localStorage存储、全局状态等
}
</script>
