# Rainhard Portfolio

This repository contains the responsive portfolio frontend and its Django application. Django is now the authoritative backend and serves the frontend and API from one origin.

## Project structure

- `index.html` — static portfolio front end
- `styles.css` — site styling and responsive layout
- `script.js` — interactive behavior and form handling
- `django_backend/` — Django application, PostgreSQL models, API, migrations, admin, and deployment entry points
- `backend/` — legacy Express + Prisma API retained for reference and data migration only

## Local development

Prerequisites: Python 3.12+. PostgreSQL 14+ is recommended for production-like volume; an empty `DATABASE_URL` uses SQLite locally.

```powershell
cd django_backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
py manage.py migrate
py manage.py seed_portfolio
py manage.py runserver 8000
```

Open `http://127.0.0.1:8000/`. Django serves the existing HTML, CSS, JavaScript, images, CV, API, and admin console. Contact submissions are stored in `ContactSubmission`; page views are stored in indexed `HighVolumeLogEntry` rows.

## API

- `GET /health`
- `GET /api/projects?limit=20&cursor=...`
- `GET /api/blog?limit=20`
- `GET /api/skills`
- `POST /api/messages`
- `POST /api/analytics/visit`

List responses are bounded. Projects use a keyset cursor ordered by indexed `featured`, `created_at`, and `id` fields. Contact writes are validated, CSRF-protected, rate-limited, and atomic. Analytics are durable database writes; use a queue in front of ingestion if traffic grows beyond synchronous writes.

## Front-end deployment

The portfolio front end is a static site and can be deployed to GitHub Pages, Netlify, Vercel, or any static host.

1. Push the repository to your preferred static host.
2. Set the site root to the project root.
3. Ensure the live site uses the correct backend URL if you wire the API to production.

## Django deployment

Deploy `django_backend/` as a Python web service with managed PostgreSQL. Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`, exact `DJANGO_ALLOWED_HOSTS`, exact HTTPS `DJANGO_CSRF_TRUSTED_ORIGINS`, and `DATABASE_URL` in the provider's secret configuration. Never commit `.env`.

1. Install dependencies and migrate:

```bash
cd django_backend
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

2. Start behind the platform's HTTPS proxy:

```bash
gunicorn portfolio_project.wsgi:application --bind 0.0.0.0:$PORT
```

The service exposes a health check at `GET /health` and admin at `/admin/`.

## Production notes

- Use a strong random `DJANGO_SECRET_KEY` and a managed PostgreSQL service.
- Create an admin with `python manage.py createsuperuser`; never commit credentials.
- Run `python manage.py check --deploy` before release.
- Put a durable queue in front of analytics ingestion if traffic grows beyond synchronous database writes.
