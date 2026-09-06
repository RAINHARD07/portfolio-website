# Rainhard Portfolio API

Express + PostgreSQL + Prisma backend for the portfolio site. The service is intentionally isolated in `backend/` so the static site can still deploy independently.

## Architecture

- `src/app.js` owns HTTP middleware and route mounting.
- `src/routes/` owns resource-specific HTTP behavior.
- `src/validation.js` owns request contracts and bounds.
- Prisma owns migrations and database access.
- Analytics writes go through a small in-memory batch buffer; the API returns `202` quickly and flushes to PostgreSQL in batches. For multi-instance production deployments, replace this buffer with Redis/BullMQ or a managed queue.
- IDs are `BIGSERIAL`/`BigInt`. Responses serialize them as strings to avoid JavaScript precision loss.
- Composite indexes follow the cursor pagination order. Analytics has time/page and hash/time indexes for aggregation and privacy-preserving distinct visitor counts. Blog tags use a PostgreSQL GIN index.

## Setup

Prerequisites: Node.js 20+, npm, PostgreSQL 14+.

```powershell
cd backend
Copy-Item .env.example .env
# Edit .env and set DATABASE_URL and a long random JWT_SECRET
# Optional local database: docker compose up -d postgres
npm install
npm run prisma:generate
npm run prisma:migrate
npm run db:seed
npm run dev
```

Set `SEED_SCALE=true` before `npm run db:seed` to add 5,000 messages and 10,000 visits for pagination and aggregation checks. Never use the sample admin password in production.

## Endpoints

Public: `GET /health`, `GET /api/projects?limit=20&cursor=...`, `GET /api/blog?limit=20&cursor=...`, `GET /api/skills`, `POST /api/messages`, `POST /api/analytics/visit`.

Admin JWT: `POST /api/auth/login`, `GET /api/messages?isRead=false`, project CRUD, blog CRUD, `GET /api/analytics/summary?days=30`.

Example login:

```powershell
$body = @{ email = 'admin@example.com'; password = 'change-me-before-production' } | ConvertTo-Json
Invoke-RestMethod http://localhost:4000/api/auth/login -Method Post -ContentType 'application/json' -Body $body
```

Example contact submission:

```powershell
$body = @{ name = 'A User'; email = 'user@example.com'; subject = 'Opportunity'; message = 'I would like to discuss an IT support opportunity.' } | ConvertTo-Json
Invoke-RestMethod http://localhost:4000/api/messages -Method Post -ContentType 'application/json' -Body $body
```

Admin requests use `Authorization: Bearer <token>`. List responses include `data` and `pagination.nextCursor`; pass that cursor to fetch the next page. Public write endpoints are validated, bounded, sanitized by trimming, and rate-limited where abuse risk is highest. Errors use `{ "error": { "code": "...", "message": "..." } }`.
