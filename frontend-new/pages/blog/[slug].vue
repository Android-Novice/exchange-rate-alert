<template>
  <div class="page-container">
    <div v-if="article" class="blog-article">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <NuxtLink to="/">Home</NuxtLink>
        <span class="sep">/</span>
        <NuxtLink to="/blog">Blog</NuxtLink>
        <span class="sep">/</span>
        <span class="current">{{ article.category }}</span>
      </nav>

      <article itemscope itemtype="https://schema.org/Article">
        <header class="article-header">
          <span class="blog-category">{{ article.category }}</span>
          <h1 itemprop="headline">{{ article.title }}</h1>
          <p class="article-desc" itemprop="description">{{ article.description }}</p>
          <div class="article-meta">
            <span itemprop="author">{{ article.author }}</span>
            <span>&middot;</span>
            <time itemprop="datePublished" :datetime="article.date">{{ article.date }}</time>
            <span>&middot;</span>
            <span>{{ article.readTime }}</span>
          </div>
        </header>

        <div class="article-body" itemprop="articleBody" v-html="renderedContent"></div>
      </article>

      <aside class="related-section" aria-label="Related Articles">
        <h2>Related Articles</h2>
        <div class="related-grid">
          <NuxtLink
            v-for="r in related"
            :key="r.slug"
            :to="`/blog/${r.slug}`"
            class="related-card"
          >
            <span class="related-icon">{{ r.image }}</span>
            <div>
              <h3>{{ r.title }}</h3>
              <span class="related-meta">{{ r.readTime }}</span>
            </div>
          </NuxtLink>
        </div>
      </aside>
    </div>

    <div v-else class="no-data">
      <h1>Article Not Found</h1>
      <p>The article you're looking for doesn't exist.</p>
      <NuxtLink to="/blog" class="cta-button">Back to Blog</NuxtLink>
    </div>
  </div>
</template>

<script setup>
import { articles, getArticleBySlug, getRelatedArticles } from '~/composables/useBlog'

const route = useRoute()
const slug = route.params.slug
const article = getArticleBySlug(slug)
const related = getRelatedArticles(slug, 3)

const renderedContent = computed(() => {
  if (!article) return ''
  let html = article.content

  // Images: ![alt](url)
  html = html.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<figure class="article-img"><img src="$2" alt="$1" loading="lazy" /><figcaption>$1</figcaption></figure>')

  // Blockquotes: > text
  html = html.replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
  // Merge consecutive blockquotes
  html = html.replace(/<\/blockquote>\n<blockquote>/g, '<br>')

  // Tables: | header | header |
  html = html.replace(/(\|.+\|)\n(\|[-| :]+\|)\n((?:\|.+\|\n?)*)/g, (match, headerRow, sepRow, bodyRows) => {
    const headers = headerRow.split('|').filter(c => c.trim()).map(c => `<th>${c.trim()}</th>`).join('')
    const rows = bodyRows.trim().split('\n').map(row => {
      const cells = row.split('|').filter(c => c.trim()).map(c => `<td>${c.trim()}</td>`).join('')
      return `<tr>${cells}</tr>`
    }).join('')
    return `<table><thead><tr>${headers}</tr></thead><tbody>${rows}</tbody></table>`
  })

  // Headings
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>')
  html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>')

  // Bold
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')

  // Italic
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>')

  // Links: [text](url)
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')

  // List items
  html = html.replace(/^- (.+)$/gm, '<li>$1</li>')
  html = html.replace(/(<li>[\s\S]*?<\/li>)/g, (m) => {
    if (!m.startsWith('<ul>')) return `<ul>${m}</ul>`
    return m
  })
  // Merge consecutive uls
  html = html.replace(/<\/ul>\s*<ul>/g, '')

  // Paragraphs
  html = html.replace(/\n{2,}/g, '</p><p>')
  html = '<p>' + html + '</p>'

  // Clean up empty p tags around block elements
  html = html.replace(/<p>\s*<(h[23]|figure|blockquote|table|ul)/g, '<$1')
  html = html.replace(/<\/(h[23]|figure|blockquote|table|ul)>\s*<\/p>/g, '</$1>')
  html = html.replace(/<p>\s*<\/p>/g, '')

  return html
})

if (article) {
  useHead({
    title: `${article.title} | Exchange Rate Monitor`,
    meta: [
      { name: 'description', content: article.description },
      { name: 'keywords', content: `exchange rate, ${article.category.toLowerCase()}, currency, forex` },
      { property: 'og:title', content: article.title },
      { property: 'og:description', content: article.description },
      { property: 'og:type', content: 'article' },
      { property: 'article:published_time', content: article.date },
      { property: 'article:author', content: article.author },
      { property: 'article:section', content: article.category },
      { name: 'twitter:card', content: 'summary' },
      { name: 'twitter:title', content: article.title },
      { name: 'twitter:description', content: article.description },
    ],
    link: [
      { rel: 'canonical', href: `https://yoursite.com/blog/${slug}` },
    ],
    script: [
      {
        type: 'application/ld+json',
        innerHTML: JSON.stringify({
          '@context': 'https://schema.org',
          '@type': 'Article',
          headline: article.title,
          description: article.description,
          author: { '@type': 'Organization', name: article.author },
          datePublished: article.date,
          publisher: {
            '@type': 'Organization',
            name: 'Exchange Rate Monitor',
          },
          mainEntityOfPage: {
            '@type': 'WebPage',
            '@id': `https://yoursite.com/blog/${slug}`,
          },
        }),
      },
    ],
  })
}
</script>

<style scoped>
.blog-article {
  max-width: 780px;
  margin: 0 auto;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  margin-bottom: 24px;
}

.breadcrumb a {
  color: #4f6ef7;
  text-decoration: none;
}

.breadcrumb a:hover { text-decoration: underline; }
.breadcrumb .sep { color: #cbd5e1; }
.breadcrumb .current { color: #64748b; font-weight: 500; }

.article-header {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e2e8f0;
}

.article-header .blog-category {
  display: inline-block;
  padding: 2px 10px;
  background: #eef2ff;
  color: #4f6ef7;
  font-size: 11px;
  font-weight: 600;
  border-radius: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
}

.article-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1a2332;
  line-height: 1.3;
  margin-bottom: 12px;
}

.article-desc {
  font-size: 16px;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 12px;
}

.article-meta {
  display: flex;
  gap: 8px;
  font-size: 13px;
  color: #94a3b8;
}

.article-body {
  font-size: 15px;
  line-height: 1.8;
  color: #334155;
}

.article-body :deep(h2) {
  font-size: 20px;
  font-weight: 700;
  color: #1a2332;
  margin: 32px 0 12px;
}

.article-body :deep(h3) {
  font-size: 17px;
  font-weight: 600;
  color: #1e293b;
  margin: 24px 0 8px;
}

.article-body :deep(p) {
  margin-bottom: 16px;
}

.article-body :deep(ul) {
  margin: 12px 0 16px 20px;
}

.article-body :deep(li) {
  margin-bottom: 6px;
}

.article-body :deep(strong) {
  color: #1a2332;
}

.article-body :deep(.article-img) {
  margin: 24px 0;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

.article-body :deep(.article-img img) {
  width: 100%;
  height: auto;
  display: block;
}

.article-body :deep(.article-img figcaption) {
  padding: 10px 16px;
  font-size: 12px;
  color: #94a3b8;
  background: #f8fafc;
  text-align: center;
}

.article-body :deep(blockquote) {
  margin: 20px 0;
  padding: 16px 20px;
  background: #fffbeb;
  border-left: 4px solid #f0c75e;
  border-radius: 0 8px 8px 0;
  font-size: 14px;
  color: #6b5a1e;
  line-height: 1.7;
}

.article-body :deep(blockquote strong) {
  color: #92700c;
}

.article-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.article-body :deep(thead) {
  background: #1a2332;
}

.article-body :deep(thead th) {
  padding: 10px 14px;
  font-size: 12px;
  font-weight: 600;
  color: #fff;
  text-align: left;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.article-body :deep(tbody td) {
  padding: 10px 14px;
  font-size: 13px;
  color: #334155;
  border-bottom: 1px solid #f1f5f9;
}

.article-body :deep(tbody tr:nth-child(even)) {
  background: #f8fafc;
}

.article-body :deep(tbody tr:hover) {
  background: #eef2ff;
}

.article-body :deep(em) {
  color: #64748b;
  font-size: 13px;
}

.article-body :deep(a) {
  color: #4f6ef7;
  text-decoration: underline;
  text-underline-offset: 2px;
}

.article-body :deep(a:hover) {
  color: #3730a3;
}

.related-section {
  margin-top: 48px;
  padding-top: 32px;
  border-top: 1px solid #e2e8f0;
}

.related-section h2 {
  font-size: 18px;
  font-weight: 700;
  color: #1a2332;
  margin-bottom: 16px;
}

.related-grid {
  display: grid;
  gap: 12px;
}

.related-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  text-decoration: none;
  color: inherit;
  transition: all 0.15s;
}

.related-card:hover {
  background: #eef2ff;
  border-color: #c7d2fe;
}

.related-icon {
  font-size: 28px;
}

.related-card h3 {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 2px;
}

.related-meta {
  font-size: 12px;
  color: #94a3b8;
}

.no-data {
  text-align: center;
  padding: 60px 20px;
}

.no-data h1 {
  font-size: 24px;
  color: #1a2332;
  margin-bottom: 8px;
}

.no-data p {
  color: #64748b;
  margin-bottom: 20px;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  padding: 10px 24px;
  background: linear-gradient(135deg, #1a2332, #2c3e50);
  color: #fff;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
}

.cta-button:hover { opacity: 0.9; }
</style>
