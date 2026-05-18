<template>
  <div>
    <header class="app-header">
      <div class="header-inner">
        <NuxtLink to="/" class="header-brand">
          <span class="header-icon">
            <el-icon><TrendCharts /></el-icon>
          </span>
          <span class="header-text">
            <span class="header-title">Exchange Rate Monitor</span>
            <span class="header-subtitle">Global Currency Tracking & Alert System</span>
          </span>
        </NuxtLink>
        <nav class="header-nav">
          <NuxtLink to="/" class="nav-link">Rates</NuxtLink>
          <NuxtLink to="/alerts" class="nav-link">Alerts</NuxtLink>
          <NuxtLink to="/blog" class="nav-link">Blog</NuxtLink>
          <NuxtLink to="/subscribe" class="nav-link">Subscribe</NuxtLink>
        </nav>
      </div>
    </header>

    <main>
      <slot />
    </main>

    <footer class="app-footer">
      <div class="footer-inner">
        <p>Data from <strong>ExchangeRate-API</strong> &middot; Updated every 60 seconds</p>
        <p class="footer-copy">&copy; {{ new Date().getFullYear() }} Exchange Rate Monitor. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { TrendCharts } from '@element-plus/icons-vue'
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #1a2332 0%, #2c3e50 100%);
  padding: 0 20px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.app-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #d4a843, #f0c75e, #d4a843);
}

.header-inner {
  max-width: 1080px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.header-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: rgba(212, 168, 67, 0.15);
  border-radius: 9px;
  font-size: 20px;
  color: #f0c75e;
}

.header-text {
  display: flex;
  flex-direction: column;
}

.header-title {
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.5px;
}

.header-subtitle {
  font-size: 10px;
  color: rgba(255, 255, 255, 0.4);
  letter-spacing: 0.5px;
}

.header-nav {
  display: flex;
  gap: 4px;
}

.nav-link {
  padding: 6px 16px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  transition: all 0.15s ease;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #fff;
  background: rgba(255, 255, 255, 0.08);
}

.app-footer {
  background: #1a2332;
  padding: 28px 20px;
  text-align: center;
  color: rgba(255, 255, 255, 0.4);
  font-size: 13px;
}

.footer-inner {
  max-width: 1080px;
  margin: 0 auto;
}

.footer-copy {
  margin-top: 6px;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.25);
}

main {
  min-height: calc(100vh - 200px);
}
</style>
