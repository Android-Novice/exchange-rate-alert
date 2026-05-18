<template>
  <div class="page-container">
    <section class="page-hero">
      <h1>Exchange Rate Insights</h1>
      <p>Expert analysis and educational content on global currency markets</p>
    </section>

    <div class="blog-grid">
      <article v-for="a in articles" :key="a.slug" class="blog-card">
        <NuxtLink :to="`/blog/${a.slug}`" class="blog-link">
          <div class="blog-card-icon">{{ a.image }}</div>
          <div class="blog-card-body">
            <span class="blog-category">{{ a.category }}</span>
            <h2 class="blog-card-title">{{ a.title }}</h2>
            <p class="blog-card-desc">{{ a.description }}</p>
            <div class="blog-meta">
              <span>{{ a.date }}</span>
              <span>&middot;</span>
              <span>{{ a.readTime }}</span>
            </div>
          </div>
        </NuxtLink>
      </article>
    </div>
  </div>
</template>

<script setup>
import { articles } from '~/composables/useBlog'

useHead({
  title: 'Exchange Rate Blog - Insights, Analysis & Guides | Exchange Rate Monitor',
  meta: [
    { name: 'description', content: 'Expert articles on exchange rates, currency markets, economic analysis, and practical guides for international money transfers and forex trading.' },
    { property: 'og:title', content: 'Exchange Rate Insights - Blog' },
    { property: 'og:description', content: 'Educational articles and expert analysis on global currency markets and exchange rate trends.' },
    { property: 'og:type', content: 'website' },
  ],
  link: [
    { rel: 'canonical', href: 'https://yoursite.com/blog' },
  ],
})
</script>

<style scoped>
.blog-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
}

.blog-card {
  background: #fff;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
  border: 1px solid rgba(0,0,0,0.04);
  transition: box-shadow 0.2s, transform 0.2s;
}

.blog-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1), 0 8px 24px rgba(0,0,0,0.06);
  transform: translateY(-2px);
}

.blog-link {
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: inherit;
}

.blog-card-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  height: 120px;
  background: linear-gradient(135deg, #1a2332, #2c3e50);
}

.blog-card-body {
  padding: 20px;
}

.blog-category {
  display: inline-block;
  padding: 2px 10px;
  background: #eef2ff;
  color: #4f6ef7;
  font-size: 11px;
  font-weight: 600;
  border-radius: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.blog-card-title {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.4;
  margin-bottom: 8px;
}

.blog-card-desc {
  font-size: 13px;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 12px;
}

.blog-meta {
  display: flex;
  gap: 8px;
  font-size: 12px;
  color: #94a3b8;
}

@media (max-width: 768px) {
  .blog-grid { grid-template-columns: 1fr; }
}
</style>
