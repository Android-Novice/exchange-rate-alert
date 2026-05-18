import axios from 'axios'

export const CURRENCIES = [
  'USD', 'EUR', 'JPY', 'GBP', 'CNY',
  'AUD', 'CAD', 'CHF', 'HKD', 'NZD',
  'SEK', 'KRW', 'SGD', 'NOK', 'MXN',
  'INR', 'RUB', 'ZAR', 'TRY', 'BRL',
]

export const CURRENCY_NAMES = {
  USD: 'US Dollar', EUR: 'Euro', JPY: 'Japanese Yen', GBP: 'British Pound',
  CNY: 'Chinese Yuan', AUD: 'Australian Dollar', CAD: 'Canadian Dollar',
  CHF: 'Swiss Franc', HKD: 'Hong Kong Dollar', NZD: 'New Zealand Dollar',
  SEK: 'Swedish Krona', KRW: 'South Korean Won', SGD: 'Singapore Dollar',
  NOK: 'Norwegian Krone', MXN: 'Mexican Peso', INR: 'Indian Rupee',
  RUB: 'Russian Ruble', ZAR: 'South African Rand', TRY: 'Turkish Lira',
  BRL: 'Brazilian Real',
}

export function useApi() {
  const config = useRuntimeConfig()
  const api = axios.create({ baseURL: config.public.apiBase, timeout: 10000 })

  return {
    getCurrencies: () => api.get('/api/rates/currencies').then(r => r.data),
    getLatestRates: () => api.get('/api/rates/latest').then(r => r.data),
    convertRate: (from, to) => api.get('/api/rates/convert', { params: { from_currency: from, to_currency: to } }).then(r => r.data),
    getHistory: (from, to, hours = 24) => api.get('/api/rates/history', { params: { from_currency: from, to_currency: to, hours } }).then(r => r.data),
    getAlerts: (hours = 24) => api.get('/api/alerts', { params: { hours } }).then(r => r.data),
    subscribe: (phone, pair) => api.post('/api/subscriptions', { phone, currency_pair: pair }).then(r => r.data),
    unsubscribe: (phone) => api.delete(`/api/subscriptions/${phone}`).then(r => r.data),
  }
}

export function useExchangeRateData() {
  return { CURRENCIES, CURRENCY_NAMES }
}
