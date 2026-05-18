<template>
  <div class="page-container">
    <section class="page-hero">
      <h1>Rate Alert Notifications</h1>
      <p>Monitor currency fluctuations and get notified when rates move beyond 0.1%</p>
    </section>

    <article aria-label="Active Alerts" class="card">
      <div class="card-header">
        <span class="icon-wrap amber"><el-icon><Bell /></el-icon></span>
        <span class="card-title">Recent Alerts (24h)</span>
      </div>
      <div v-if="alerts.length" class="alert-list">
        <div v-for="a in alerts" :key="a.id" :class="['alert-item', a.direction]">
          <span class="alert-icon-wrap">
            <el-icon><TopRight v-if="a.direction === 'up'" /><BottomRight v-else /></el-icon>
          </span>
          <div class="alert-info">
            <div class="alert-pair">{{ a.currency_pair }}</div>
            <div class="alert-change">
              {{ a.direction === 'up' ? '+' : '-' }}{{ a.change_percent }}%
              &middot; Rate: {{ a.new_rate }}
            </div>
          </div>
          <span class="alert-time">{{ a.time }}</span>
        </div>
      </div>
      <div v-else class="no-data">
        <el-icon><CircleCheck /></el-icon>
        <div>All stable &mdash; no alerts in the past 24 hours</div>
      </div>
    </article>

    <article aria-label="How Alerts Work" class="card">
      <div class="card-header">
        <span class="icon-wrap blue"><el-icon><Warning /></el-icon></span>
        <span class="card-title">How It Works</span>
      </div>
      <div class="info-grid">
        <div class="info-item">
          <h3>Real-time Monitoring</h3>
          <p>Exchange rates are fetched every 60 seconds from ExchangeRate-API for 20+ global currencies.</p>
        </div>
        <div class="info-item">
          <h3>Threshold Detection</h3>
          <p>When a currency pair fluctuates more than 0.1% between consecutive readings, an alert is triggered.</p>
        </div>
        <div class="info-item">
          <h3>SMS Notification</h3>
          <p>Subscribers receive an SMS alert instantly. Duplicate alerts within 1 hour are automatically suppressed.</p>
        </div>
      </div>
      <div class="cta-row">
        <NuxtLink to="/subscribe" class="cta-button">
          <el-icon><Iphone /></el-icon>
          Subscribe to Alerts
        </NuxtLink>
      </div>
    </article>
  </div>
</template>

<script setup>
import { Bell, TopRight, BottomRight, CircleCheck, Warning, Iphone } from '@element-plus/icons-vue'

const { getAlerts } = useApi()
const alerts = ref([])

async function loadAlerts() {
  try {
    const data = await getAlerts(24)
    alerts.value = data.alerts
  } catch (e) {
    console.error('Failed to load alerts', e)
  }
}

let timer = null
onMounted(async () => {
  await loadAlerts()
  timer = setInterval(loadAlerts, 30000)
})
onUnmounted(() => { if (timer) clearInterval(timer) })

useHead({
  title: 'Exchange Rate Alerts - Free SMS Notifications | Exchange Rate Monitor',
  meta: [
    { name: 'description', content: 'Get free SMS alerts when exchange rates fluctuate beyond 0.1%. Monitor USD, EUR, GBP, JPY, CNY and 15+ more currencies in real-time.' },
    { property: 'og:title', content: 'Exchange Rate Alert System' },
    { property: 'og:description', content: 'Free SMS notifications for currency rate fluctuations. Track 20+ global currencies.' },
    { property: 'og:type', content: 'website' },
    { name: 'twitter:card', content: 'summary' },
  ],
  link: [
    { rel: 'canonical', href: 'https://yoursite.com/alerts' },
  ],
})
</script>

<style scoped>
.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.info-item h3 {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 6px;
}

.info-item p {
  font-size: 13px;
  color: #64748b;
  line-height: 1.6;
}

.cta-row {
  text-align: center;
  padding-top: 8px;
  border-top: 1px solid #f1f5f9;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 28px;
  background: linear-gradient(135deg, #1a2332, #2c3e50);
  color: #fff;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: opacity 0.15s;
}

.cta-button:hover { opacity: 0.9; }

@media (max-width: 768px) {
  .info-grid { grid-template-columns: 1fr; }
}
</style>
