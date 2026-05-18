<template>
  <div class="page-container">
    <section class="page-hero">
      <h1>Live Exchange Rates</h1>
      <p>Track 20+ global currencies with real-time updates and instant alerts</p>
      <div class="live-badge" v-if="updateTime">
        <span class="dot"></span>
        <span>Live &mdash; {{ updateTime }}</span>
      </div>
    </section>

    <section aria-label="Currency Converter" class="card">
      <div class="card-header">
        <span class="icon-wrap blue"><el-icon><Coin /></el-icon></span>
        <span class="card-title">Currency Converter</span>
      </div>

      <div class="selector-row">
        <div class="selector-group">
          <span class="selector-label">From</span>
          <el-select v-model="fromCurrency" @change="onCurrencyChange">
            <el-option v-for="c in currencies" :key="c" :label="c" :value="c" />
          </el-select>
        </div>
        <div class="arrow-wrap">
          <el-icon><Right /></el-icon>
        </div>
        <div class="selector-group">
          <span class="selector-label">To</span>
          <el-select v-model="toCurrency" @change="onCurrencyChange">
            <el-option v-for="c in currencies" :key="c" :label="c" :value="c" />
          </el-select>
        </div>
      </div>

      <div class="rate-display">
        <div class="rate-label">Current Rate</div>
        <div class="rate-value" v-if="currentRate !== null">
          <span class="currency-from">1 {{ fromCurrency }} =</span>
          {{ currentRate.toFixed(6) }}
          <span class="currency-to">{{ toCurrency }}</span>
        </div>
        <div class="rate-value" v-else>Loading...</div>
        <div :class="['change-badge', changeClass]">
          <el-icon v-if="changeClass === 'up'"><TopRight /></el-icon>
          <el-icon v-else-if="changeClass === 'down'"><BottomRight /></el-icon>
          <el-icon v-else><Minus /></el-icon>
          {{ changeText }}
        </div>
      </div>
    </section>

    <div class="grid-2">
      <section aria-label="Alert Notifications" class="card">
        <div class="card-header">
          <span class="icon-wrap amber"><el-icon><Bell /></el-icon></span>
          <span class="card-title">Alert Notifications</span>
        </div>
        <div v-if="alerts.length" class="alert-list">
          <div v-for="a in alerts" :key="a.id" :class="['alert-item', a.direction]">
            <span class="alert-icon-wrap">
              <el-icon><TopRight v-if="a.direction === 'up'" /><BottomRight v-else /></el-icon>
            </span>
            <div class="alert-info">
              <div class="alert-pair">{{ a.currency_pair }}</div>
              <div class="alert-change">{{ a.direction === 'up' ? '+' : '-' }}{{ a.change_percent }}%</div>
            </div>
            <span class="alert-time">{{ a.time }}</span>
          </div>
        </div>
        <div v-else class="no-data">
          <el-icon><CircleCheck /></el-icon>
          <div>All stable &mdash; no alerts</div>
        </div>
      </section>

      <section aria-label="Popular Currency Pairs" class="card">
        <div class="card-header">
          <span class="icon-wrap green"><el-icon><Coin /></el-icon></span>
          <span class="card-title">Popular Pairs</span>
        </div>
        <div class="currency-grid">
          <NuxtLink
            v-for="pair in popularPairs"
            :key="pair.from + pair.to"
            :to="`/${pair.from.toLowerCase()}-to-${pair.to.toLowerCase()}`"
            class="currency-link"
          >
            <span class="flag">{{ pair.flag }}</span>
            <div>
              <div class="code">{{ pair.from }}/{{ pair.to }}</div>
              <div class="name">{{ pair.label }}</div>
            </div>
          </NuxtLink>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { Coin, Right, TopRight, BottomRight, Minus, Bell, CircleCheck } from '@element-plus/icons-vue'

const { convertRate, getAlerts } = useApi()
const { CURRENCIES } = useExchangeRateData()

const currencies = ref(CURRENCIES)
const fromCurrency = ref('USD')
const toCurrency = ref('CNY')
const currentRate = ref(null)
const prevRate = ref(null)
const updateTime = ref('')
const alerts = ref([])

const popularPairs = [
  { from: 'USD', to: 'CNY', flag: '🇺🇸', label: 'Dollar / Yuan' },
  { from: 'USD', to: 'EUR', flag: '🇪🇺', label: 'Dollar / Euro' },
  { from: 'USD', to: 'GBP', flag: '🇬🇧', label: 'Dollar / Pound' },
  { from: 'USD', to: 'JPY', flag: '🇯🇵', label: 'Dollar / Yen' },
  { from: 'EUR', to: 'GBP', flag: '🇪🇺', label: 'Euro / Pound' },
  { from: 'USD', to: 'CHF', flag: '🇨🇭', label: 'Dollar / Franc' },
  { from: 'USD', to: 'AUD', flag: '🇦🇺', label: 'Dollar / AUD' },
  { from: 'USD', to: 'CAD', flag: '🇨🇦', label: 'Dollar / CAD' },
]

const changeText = computed(() => {
  if (!prevRate.value || prevRate.value === currentRate.value) return '0.00%'
  const pct = ((currentRate.value - prevRate.value) / prevRate.value * 100)
  return `${pct > 0 ? '+' : ''}${pct.toFixed(6)}%`
})

const changeClass = computed(() => {
  if (!prevRate.value || prevRate.value === currentRate.value) return 'neutral'
  return currentRate.value > prevRate.value ? 'up' : 'down'
})

function onCurrencyChange() {
  currentRate.value = null
  prevRate.value = null
  loadRate()
}

async function loadRate() {
  try {
    const data = await convertRate(fromCurrency.value, toCurrency.value)
    if (data.error) return
    prevRate.value = currentRate.value
    currentRate.value = data.rate
    updateTime.value = data.fetched_at || ''
  } catch (e) {
    console.error('Failed to load rate', e)
  }
}

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
  await Promise.all([loadRate(), loadAlerts()])
  timer = setInterval(async () => {
    await Promise.all([loadRate(), loadAlerts()])
  }, 30000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

// SEO
useHead({
  title: 'Live Exchange Rates - Real-time Currency Converter | Exchange Rate Monitor',
  meta: [
    { name: 'description', content: 'Track live exchange rates for 20+ global currencies including USD, EUR, GBP, JPY, CNY. Free SMS alerts when rates fluctuate beyond 0.1%. Updated every 60 seconds.' },
    { name: 'keywords', content: 'exchange rate, currency converter, USD to CNY, forex, live rates, currency exchange, dollar to yuan, euro to dollar' },
    { property: 'og:title', content: 'Exchange Rate Monitor - Live Currency Rates' },
    { property: 'og:description', content: 'Real-time exchange rates for 20+ global currencies with free SMS alert notifications.' },
    { property: 'og:type', content: 'website' },
    { property: 'og:url', content: 'https://yoursite.com/' },
    { property: 'og:site_name', content: 'Exchange Rate Monitor' },
    { name: 'twitter:card', content: 'summary_large_image' },
    { name: 'twitter:title', content: 'Live Exchange Rates - 20+ Currencies' },
    { name: 'twitter:description', content: 'Track live exchange rates for USD, EUR, GBP, JPY, CNY and more with free SMS alerts.' },
  ],
  link: [
    { rel: 'canonical', href: 'https://yoursite.com/' },
  ],
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'WebApplication',
        name: 'Exchange Rate Monitor',
        description: 'Real-time exchange rate tracking and alert system for 20+ global currencies',
        applicationCategory: 'FinanceApplication',
        operatingSystem: 'Web',
        offers: {
          '@type': 'Offer',
          price: '0',
          priceCurrency: 'USD',
        },
        featureList: [
          'Real-time exchange rates for 20+ currencies',
          'Free SMS alert notifications',
          'Rate fluctuation monitoring',
          'Currency conversion calculator',
        ],
      }),
    },
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        itemListElement: [
          { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://yoursite.com/' },
        ],
      }),
    },
  ],
})
</script>
