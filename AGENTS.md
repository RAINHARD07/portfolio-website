# Agent Instructions

## Project Shape

- The root site is a static portfolio: `index.html`, `styles.css`, `script.js`, `Images/`, `cv.html`, and `cv.pdf`.
- `django_backend/` is the authoritative Django 5.2+ application. It serves the root frontend, owns the API, migrations, and admin console.
- `backend/` is the legacy Express 5 + Prisma API retained for reference and data migration only; do not add new frontend integrations to it.
- Read the root [README.md](README.md) and [django_backend/README.md](django_backend/README.md) for setup and deployment details. Read [deployment-readiness](.github/skills/deployment-readiness/SKILL.md) for production checks; do not duplicate its runbook here.

## Frontend and Backend Integration

- Preserve the existing visual frontend while serving it through Django in the connected deployment.
- The contact form submits JSON to Django `POST /api/messages` with same-origin CSRF protection; retain a useful direct-email fallback message when the API is unavailable.
- Public Django endpoints include `/health`, `/api/projects`, `/api/blog`, `/api/skills`, `/api/messages`, and `/api/analytics/visit`. Preserve the `{data, pagination}` response shape and bounded pagination.
- Keep Django and the frontend on one origin in production. If a separate frontend host is introduced, configure CSRF trusted origins and CORS deliberately before changing `apiBase`.
- Never expose database credentials, JWT secrets, or `.env` contents in frontend code or committed documentation.

## Responsive UI Requirements

- Keep the existing visual language: Manrope and DM Mono from Google Fonts, Georgia for display headings, paper/navy/copper tokens, semantic HTML, and the established class names unless a change requires otherwise.
- Check mobile, tablet, and wide desktop layouts after frontend changes. Preserve the existing breakpoint behavior around `800px`, including the menu toggle, one-column content grids, project filters, contact form, and field-note visual.
- Use the existing responsive CSS patterns and stable grid/flex dimensions. Avoid horizontal overflow, clipped labels, overlapping controls, and fixed-width content that cannot shrink.
- Preserve keyboard focus states, meaningful labels, `aria-*` state updates, reduced-motion behavior, and usable touch targets.
- Keep local asset paths valid and verify every changed HTML reference under `Images/`, plus `cv.pdf` and `cv.html`.

## Backend Development

- Run Django commands from `django_backend/`. Python 3.12+ and PostgreSQL 14+ are expected for production.
- Use `py manage.py check`, `py manage.py makemigrations`, and `py manage.py migrate` for Django changes. Never edit an applied migration; review generated migrations.
- Keep pagination bounded and keyset-based where high-volume ordering requires it. Use `only()`/`select_related()`/`prefetch_related()` deliberately.
- Maintain CSRF, validation, atomic contact writes, rate limiting, security middleware, and indexed log writes when changing API views.
- Analytics are durable Django database rows but still need a queue or ingestion service for extreme multi-instance traffic; do not promise unlimited throughput from synchronous request writes.

## Verification

- For frontend changes, perform an HTML asset check and manually or browser-test navigation, theme toggle, project filters, CV download, and contact behavior when affected.
- For Django changes, run `py manage.py check`, migration checks, and focused API tests when available. Do not run destructive production database commands.
- For legacy Express changes, run `npm.cmd run check` from `backend/`.
- Report checks that could not run, especially when Python, PostgreSQL, or browser tooling is unavailable.
