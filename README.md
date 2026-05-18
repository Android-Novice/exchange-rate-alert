# Exchange Rate Monitor

Global currency exchange rate tracking and alert system.

## Architecture

- **Frontend:** Nuxt 3 (SSR) → Vercel
- **Backend:** Python FastAPI → Render.com
- **Database:** PostgreSQL (Render) / SQLite (local)

## Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8080

# Frontend
cd frontend-new
npm install
npm run dev
```

## Deployment

### Frontend (Vercel)
1. Push to GitHub
2. Import repo in Vercel
3. Set root directory to `frontend-new`
4. Add env var `NUXT_PUBLIC_API_BASE` = your backend URL

### Backend (Render)
1. Connect GitHub repo in Render
2. Select `render.yaml` blueprint
3. Add env vars: `SMS_ACCESS_KEY_ID`, `SMS_ACCESS_KEY_SECRET`

## Features

- Real-time exchange rates for 20+ currencies
- Free SMS alerts when rates fluctuate > 0.1%
- Blog with 10+ educational articles
- Multi-page SEO optimized structure
