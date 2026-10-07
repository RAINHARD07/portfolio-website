# Django Portfolio Backend

This is the authoritative replacement for the previous Express API. Django serves the existing root portfolio frontend at `/`, exposes the JSON API under `/api/`, and provides `/admin/` for managing the profile, CV, social links, projects, skills, posts, contact messages, and high-volume logs.

## Local setup

Prerequisites: Python 3.12+. SQLite is used by default; PostgreSQL support remains optional.

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

Upload a replacement CV from **Site profiles** in Django admin. The CV is served from the Django app so it works in production as well as locally. On Render Free, uploaded files use temporary local storage and can disappear on restart, spin-down, or deploy.

Contact submissions are stored in SQLite and shown in **Contact submissions**. The inbox shows 100 messages per page and supports showing all messages up to 5,000 at once, with search, date filters, and review status. Messages are not capped at 5,000, but on Render Free the SQLite file is temporary and messages can disappear on restart, spin-down, or deploy.

Projects added or edited in **Projects** appear on the portfolio. The initial seed command only adds missing default entries and does not overwrite or delete projects you have edited or added. The public project list is fetched through all bounded API pages, so projects beyond the first 100 are not dropped from the homepage.

The contact inbox supports well over 200,000 records. To load a clearly marked demo dataset for performance testing, run `py manage.py seed_demo_messages --count 200001`. Do not run this for normal use unless you specifically want demo rows in the inbox.

For local development, leave `DATABASE_URL` empty to use SQLite. Render Free also uses SQLite's default local file, but its filesystem is temporary. This mode is for trying the hosted admin and inbox only; use durable storage before relying on messages or uploaded CVs.

## Render deployment

The repository includes `render.yaml` for the Django web service. The Free configuration uses SQLite and local media; it does not create PostgreSQL or attach a disk. Render Free's filesystem is temporary, so messages and uploaded CVs may be lost when the service restarts, spins down, or deploys.

To keep messages and CV uploads permanently, upgrade the Render service to a plan that supports a persistent disk, or move to a host with persistent SQLite storage.

## API

- `GET /health`
- `GET /api/projects?limit=20&cursor=...`
- `GET /api/blog?limit=20&cursor=...`
- `GET /api/skills`
- `POST /api/messages`
- `POST /api/analytics/visit`

All list reads are bounded. Projects and blog posts use keyset cursors based on indexed ordering fields. Contact submissions are atomic, validated, CSRF-protected, and rate limited through Django's cache. Analytics are durable database rows with composite indexes; for very high multi-instance traffic, put a queue in front of the log writer.

## Deployment

Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`, exact `DJANGO_ALLOWED_HOSTS`, exact HTTPS `DJANGO_CSRF_TRUSTED_ORIGINS`, and `DJANGO_SECURE_SSL_REDIRECT=true`. Leave `DATABASE_URL` unset to use SQLite's default local file. Run migrations and collect static files during build, then start:

```powershell
gunicorn portfolio_project.wsgi:application --bind 0.0.0.0:$env:PORT
```

Do not commit `.env`, use a provider-managed secret, and configure the platform HTTPS certificate. Do not rely on Render Free local files for contact-message or CV persistence.
