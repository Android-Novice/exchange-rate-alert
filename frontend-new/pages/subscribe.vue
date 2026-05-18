<template>
  <div class="page-container">
    <section class="page-hero">
      <h1>SMS Alert Subscription</h1>
      <p>Subscribe to receive free SMS notifications when your watched currency pair fluctuates beyond 0.1%</p>
    </section>

    <article aria-label="Subscription Form" class="card">
      <div class="card-header">
        <span class="icon-wrap green"><el-icon><Iphone /></el-icon></span>
        <span class="card-title">Subscribe</span>
      </div>

      <form @submit.prevent="handleSubscribe" class="subscribe-form">
        <div class="form-group">
          <label class="form-label" for="phone">Phone Number</label>
          <el-input
            id="phone"
            v-model="phone"
            placeholder="Enter phone number"
            maxlength="11"
            :prefix-icon="Iphone"
          />
        </div>
        <div class="form-group">
          <label class="form-label" for="pair">Currency Pair</label>
          <el-select id="pair" v-model="subscribePair">
            <el-option
              v-for="c in currencies.filter(x => x !== 'USD')"
              :key="c"
              :label="'USD / ' + c"
              :value="'USD/' + c"
            />
          </el-select>
        </div>
        <el-button type="primary" @click="handleSubscribe" :loading="loading">
          Subscribe
        </el-button>
      </form>

      <div v-if="message" :class="['form-message', messageType]">
        <el-icon><CircleCheck v-if="messageType === 'success'" /><Warning v-else /></el-icon>
        {{ message }}
      </div>
    </article>

    <article aria-label="Subscription Features" class="card">
      <div class="card-header">
        <span class="icon-wrap blue"><el-icon><Warning /></el-icon></span>
        <span class="card-title">How It Works</span>
      </div>
      <div class="steps">
        <div class="step">
          <span class="step-num">1</span>
          <div>
            <h3>Choose a Pair</h3>
            <p>Select the currency pair you want to monitor (e.g. USD/CNY).</p>
          </div>
        </div>
        <div class="step">
          <span class="step-num">2</span>
          <div>
            <h3>Enter Your Phone</h3>
            <p>Provide your mobile number to receive SMS alerts.</p>
          </div>
        </div>
        <div class="step">
          <span class="step-num">3</span>
          <div>
            <h3>Get Notified</h3>
            <p>Receive an SMS whenever the rate moves more than 0.1%. Max 1 alert per hour per pair.</p>
          </div>
        </div>
      </div>
    </article>
  </div>
</template>

<script setup>
import { Iphone, CircleCheck, Warning } from '@element-plus/icons-vue'

const { subscribe: apiSubscribe } = useApi()
const { CURRENCIES } = useExchangeRateData()

const currencies = ref(CURRENCIES)
const phone = ref('')
const subscribePair = ref('USD/CNY')
const loading = ref(false)
const message = ref('')
const messageType = ref('success')

async function handleSubscribe() {
  if (!phone.value || phone.value.length !== 11) {
    message.value = 'Please enter a valid 11-digit phone number'
    messageType.value = 'error'
    return
  }
  loading.value = true
  message.value = ''
  try {
    await apiSubscribe(phone.value, subscribePair.value)
    message.value = 'Subscribed successfully! You will receive SMS alerts when ' + subscribePair.value + ' fluctuates beyond 0.1%.'
    messageType.value = 'success'
    phone.value = ''
  } catch (e) {
    message.value = e.response?.data?.detail || 'Subscription failed. Please try again.'
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}

useHead({
  title: 'Subscribe to Exchange Rate SMS Alerts | Exchange Rate Monitor',
  meta: [
    { name: 'description', content: 'Subscribe to free SMS alerts for exchange rate fluctuations. Get notified when USD/CNY, EUR/USD and other currency pairs move beyond 0.1%.' },
    { property: 'og:title', content: 'Subscribe to Rate Alerts' },
    { property: 'og:description', content: 'Free SMS notifications for exchange rate fluctuations across 20+ currencies.' },
    { property: 'og:type', content: 'website' },
  ],
  link: [
    { rel: 'canonical', href: 'https://yoursite.com/subscribe' },
  ],
})
</script>

<style scoped>
.form-message {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
}

.form-message.success { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
.form-message.error { background: #fef2f2; color: #ef4444; border: 1px solid #fecaca; }

.steps {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.step {
  display: flex;
  gap: 14px;
  align-items: flex-start;
}

.step-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  min-width: 28px;
  border-radius: 50%;
  background: #eef2ff;
  color: #4f6ef7;
  font-size: 13px;
  font-weight: 700;
}

.step h3 {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 2px;
}

.step p {
  font-size: 13px;
  color: #64748b;
  line-height: 1.5;
}
</style>
