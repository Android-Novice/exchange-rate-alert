<template>
  <div class="page-container">
    <section class="page-hero">
      <h1>{{ from }} to {{ to }} Exchange Rate</h1>
      <p>Real-time {{ currencyNames[from] }} to {{ currencyNames[to] }} conversion rate with historical data</p>
      <div class="live-badge" v-if="updateTime">
        <span class="dot"></span>
        <span>Live &mdash; {{ updateTime }}</span>
      </div>
    </section>

    <article aria-label="Exchange Rate Details" class="card">
      <div class="card-header">
        <span class="icon-wrap blue"><el-icon><Coin /></el-icon></span>
        <span class="card-title">{{ from }} / {{ to }} Rate</span>
      </div>

      <div class="rate-display">
        <div class="rate-label">Current Rate</div>
        <div class="rate-value" v-if="currentRate !== null">
          <span class="currency-from">1 {{ from }} =</span>
          {{ currentRate.toFixed(4) }}
          <span class="currency-to">{{ to }}</span>
        </div>
        <div class="rate-value" v-else>Loading...</div>
        <div :class="['change-badge', changeClass]">
          <el-icon v-if="changeClass === 'up'"><TopRight /></el-icon>
          <el-icon v-else-if="changeClass === 'down'"><BottomRight /></el-icon>
          <el-icon v-else><Minus /></el-icon>
          {{ changeText }}
        </div>
      </div>

      <!-- Conversion Calculator -->
      <div class="converter-section">
        <h2 class="section-subtitle">Currency Converter</h2>
        <div class="converter-row">
          <div class="converter-input">
            <label :for="'amount-' + from">Amount ({{ from }})</label>
            <el-input-number v-model="amount" :min="0" :step="100" :controls="false" />
          </div>
          <div class="arrow-wrap">
            <el-icon><Right /></el-icon>
          </div>
          <div class="converter-input">
            <label>Result ({{ to }})</label>
            <div class="result-value">{{ convertedAmount }}</div>
          </div>
        </div>
      </div>
    </article>

    <!-- History Chart -->
    <article aria-label="Historical Exchange Rate" class="card">
      <div class="card-header">
        <span class="icon-wrap amber"><el-icon><TrendCharts /></el-icon></span>
        <span class="card-title">24h Rate History</span>
      </div>
      <div v-if="history.length" class="history-list">
        <div v-for="(h, i) in history" :key="i" class="history-item">
          <span class="history-time">{{ h.time.split(' ')[1] }}</span>
          <span class="history-rate">{{ h.rate.toFixed(4) }}</span>
        </div>
      </div>
      <div v-else class="no-data">
        <el-icon><CircleCheck /></el-icon>
        <div>Collecting data...</div>
      </div>
    </article>

    <!-- Related Pairs -->
    <article aria-label="Related Currency Pairs" class="card">
      <div class="card-header">
        <span class="icon-wrap green"><el-icon><Coin /></el-icon></span>
        <span class="card-title">Related Currency Pairs</span>
      </div>
      <div class="currency-grid">
        <NuxtLink
          v-for="pair in relatedPairs"
          :key="pair"
          :to="`/${from.toLowerCase()}-to-${pair.toLowerCase()}`"
          class="currency-link"
        >
          <div>
            <div class="code">{{ from }}/{{ pair }}</div>
            <div class="name">{{ currencyNames[pair] || pair }}</div>
          </div>
        </NuxtLink>
      </div>
    </article>
  </div>
</template>

<script setup>
import { Coin, Right, TopRight, BottomRight, Minus, TrendCharts, CircleCheck } from '@element-plus/icons-vue'

const route = useRoute()
const { convertRate, getHistory } = useApi()
const { CURRENCY_NAMES } = useExchangeRateData()

const from = route.params.from.toUpperCase()
const to = route.params.to.toUpperCase()
const currencyNames = CURRENCY_NAMES

const currentRate = ref(null)
const prevRate = ref(null)
const updateTime = ref('')
const amount = ref(1)
const history = ref([])

const relatedPairs = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'AUD', 'CAD', 'CHF']
  .filter(c => c !== from && c !== to).slice(0, 6)

const convertedAmount = computed(() => {
  if (currentRate.value === null) return '—'
  return (amount.value * currentRate.value).toFixed(4)
})

const changeText = computed(() => {
  if (!prevRate.value || prevRate.value === currentRate.value) return '0.00%'
  const pct = ((currentRate.value - prevRate.value) / prevRate.value * 100)
  return `${pct > 0 ? '+' : ''}${pct.toFixed(4)}%`
})

const changeClass = computed(() => {
  if (!prevRate.value || prevRate.value === currentRate.value) return 'neutral'
  return currentRate.value > prevRate.value ? 'up' : 'down'
})

async function loadRate() {
  try {
    const data = await convertRate(from, to)
    if (data.error) return
    prevRate.value = currentRate.value
    currentRate.value = data.rate
    updateTime.value = data.fetched_at || ''
  } catch (e) {
    console.error('Failed to load rate', e)
  }
}

async function loadHistory() {
  try {
    const data = await getHistory(from, to, 24)
    history.value = data.history || []
  } catch (e) {
    console.error('Failed to load history', e)
  }
}

let timer = null

onMounted(async () => {
  await Promise.all([loadRate(), loadHistory()])
  timer = setInterval(loadRate, 30000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

// SEO Meta
const pageTitle = `${from} to ${to} Exchange Rate - ${currentRate.value ? currentRate.value.toFixed(4) : 'Live'} | Exchange Rate Monitor`
const pageDesc = `Live ${from}/${to} exchange rate: convert ${currencyNames[from] || from} to ${currencyNames[to] || to}. Real-time updates, historical data, and free SMS alerts.`

useHead({
  title: `${from} to ${to} Exchange Rate Today | Exchange Rate Monitor`,
  meta: [
    { name: 'description', content: pageDesc },
    { name: 'keywords', content: `${from} to ${to}, ${from} ${to} exchange rate, ${currencyNames[from]}, ${currencyNames[to]}, currency converter` },
    { property: 'og:title', content: `${from} to ${to} Exchange Rate - Live` },
    { property: 'og:description', content: pageDesc },
    { property: 'og:type', content: 'website' },
    { property: 'og:url', content: `https://yoursite.com/${from.toLowerCase()}-to-${to.toLowerCase()}` },
    { name: 'twitter:card', content: 'summary' },
    { name: 'twitter:title', content: `${from}/${to} Exchange Rate` },
    { name: 'twitter:description', content: pageDesc },
  ],
  link: [
    { rel: 'canonical', href: `https://yoursite.com/${from.toLowerCase()}-to-${to.toLowerCase()}` },
  ],
})

// JSON-LD Structured Data
useHead({
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'WebPage',
        name: `${from} to ${to} Exchange Rate`,
        description: pageDesc,
        breadcrumb: {
          '@type': 'BreadcrumbList',
          itemListElement: [
            { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://yoursite.com/' },
            { '@type': 'ListItem', position: 2, name: `${from}/${to}`, item: `https://yoursite.com/${from.toLowerCase()}-to-${to.toLowerCase()}` },
          ],
        },
        mainEntity: {
          '@type': 'FinancialProduct',
          name: `${from}/${to} Exchange Rate`,
          description: `Real-time ${from} to ${to} currency conversion`,
        },
      }),
    },
  ],
})
</script>

<style scoped>
.converter-section {
  border-top: 1px solid #f1f5f9;
  margin-top: 24px;
  padding-top: 20px;
}

.section-subtitle {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 16px;
}

.converter-row {
  display: flex;
  align-items: flex-end;
  gap: 16px;
  justify-content: center;
}

.converter-input {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.converter-input label {
  font-size: 12px;
  font-weight: 500;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.converter-input .el-input-number {
  width: 180px;
}

.converter-input .el-input-number :deep(.el-input__wrapper) {
  border-radius: 10px;
}

.result-value {
  height: 32px;
  line-height: 32px;
  font-size: 20px;
  font-weight: 600;
  color: #1a2332;
  min-width: 180px;
}

.history-list {
  max-height: 300px;
  overflow-y: auto;
}

.history-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  border-bottom: 1px solid #f8fafc;
  font-size: 13px;
}

.history-item:last-child { border-bottom: none; }
.history-time { color: #94a3b8; }
.history-rate { font-weight: 600; color: #1e293b; font-variant-numeric: tabular-nums; }

@media (max-width: 768px) {
  .converter-row { flex-direction: column; align-items: center; }
}
</style>
