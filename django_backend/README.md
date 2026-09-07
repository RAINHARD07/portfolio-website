# Django Portfolio Backend

This is the authoritative replacement for the previous Express API. Django serves the existing root portfolio frontend at `/`, exposes the JSON API under `/api/`, and provides `/admin/` for managing the profile, CV, social links, projects, skills, posts, contact messages, and high-volume logs.

## Local setup

Prerequisites: Python 3.12+, PostgreSQL 14+ for production-style use.

```powershell
cd django_backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
py manage.py migrate
py manage.py createsuperuser
py manage.py seed_portfolio
py manage.py runserver 127.0.0.1:8000
```

Open `http://127.0.0.1:8000/` (HTTP, not HTTPS). The Django view serves the existing `index.html`, `styles.css`, `script.js`, `Images/`, `cv.html`, and `cv.pdf`. The frontend fetches projects and skills from this same-origin API and submits contact messages with Django CSRF protection.

## Simple editing dashboard

1. Start the server with `py manage.py runserver 127.0.0.1:8000`.
2. Open `http://127.0.0.1:8000/admin/`.
3. Sign in with the account created by `py manage.py createsuperuser`.
4. Open **Site profiles** to upload a new CV and change Instagram, GitHub, LinkedIn, X, or Facebook links.
5. Open **Contact submissions** to read messages sent from the website. Use the `is reviewed` checkbox after handling a message.
6. Use **Projects**, **Skills**, and **Blog posts** to change the portfolio content without editing GitHub files.

Uploaded CV files and future admin uploads are stored in `django_backend/media/`, separate from the source code. The root `.gitignore` excludes this folder, so `git add -A` will not push your CV or uploaded files to GitHub. Keep `media/` backed up locally, and configure persistent media storage before deploying because uploaded files are not included in a normal code deployment.

The contact inbox supports well over 200,000 records. To load a clearly marked demo dataset for performance testing, run `py manage.py seed_demo_messages --count 200001`. Do not run this for normal use unless you specifically want demo rows in the inbox.

For a quick SQLite-only local run, leave `DATABASE_URL` empty. Use PostgreSQL for production and large-volume workloads. Run `py manage.py collectstatic --noinput` before deployment and serve with Gunicorn behind HTTPS.

## Render deployment

The repository includes `render.yaml` for the full Django deployment. In Render, choose **New > Blueprint**, connect `RAINHARD07/portfolio-website`, and apply the blueprint. It creates the `asanterainhardboah` web service and a PostgreSQL database, then runs migrations and collects static files during each build.

Render's free web service filesystem is temporary. The CV upload works during a running instance, but uploaded files should use persistent object storage or a paid persistent disk before production use.

## API

- `GET /health`
- `GET /api/projects?limit=20&cursor=...`
- `GET /api/blog?limit=20&cursor=...`
- `GET /api/skills`
- `POST /api/messages`
- `POST /api/analytics/visit`

All list reads are bounded. Projects and blog posts use keyset cursors based on indexed ordering fields. Contact submissions are atomic, validated, CSRF-protected, and rate limited through Django's cache. Analytics are durable database rows with composite indexes; for very high multi-instance traffic, put a queue in front of the log writer.

## Deployment

Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`, exact `DJANGO_ALLOWED_HOSTS`, exact HTTPS `DJANGO_CSRF_TRUSTED_ORIGINS`, `DJANGO_SECURE_SSL_REDIRECT=true`, and a managed PostgreSQL `DATABASE_URL`. Run migrations and collect static files during release, then start:

```powershell
gunicorn portfolio_project.wsgi:application --bind 0.0.0.0:$env:PORT
```

Do not commit `.env`, use a provider-managed secret, enable PostgreSQL backups, and configure a reverse proxy/platform HTTPS certificate.
