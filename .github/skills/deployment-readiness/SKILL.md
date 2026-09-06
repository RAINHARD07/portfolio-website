---
name: deployment-readiness
description: 'Check whether this website is ready for deployment and guide the user through deployment. Use for static-site hosting, Express/Prisma API deployment, PostgreSQL production setup, environment variables, smoke tests, and production readiness reviews.'
argument-hint: '[optional hosting provider or deployment target]'
user-invocable: true
---

# Deployment Readiness

## Outcome

Inspect the repository, report a clear readiness verdict, and provide an ordered deployment runbook. Treat the static frontend and the optional backend as separate deployable units.

Always distinguish:

- **Static site readiness:** `index.html`, `styles.css`, `script.js`, images, `cv.html`, and `cv.pdf`.
- **Full-stack readiness:** the static site plus `backend/`, Express, Prisma, and PostgreSQL.

Do not claim the whole application is ready when only the static site has passed checks.

## Procedure

1. **Identify the deployment target.**
   - Use the user's provider if supplied.
   - Otherwise recommend a static host for the frontend and a managed Node service plus managed PostgreSQL for the backend.
   - Ask one concise question only if the target materially changes the commands or architecture.

2. **Inspect the repository before judging it.**
   Check:
   - root HTML entry points and referenced assets
   - frontend JavaScript for API URLs, `fetch`, form handling, and build requirements
   - root and backend README instructions
   - `backend/package.json` scripts and lockfile
   - `backend/.env.example`, `.gitignore`, Docker configuration, Prisma schema, and migrations
   - deployment metadata such as host config files, CI workflows, or Dockerfiles

3. **Run cheap, relevant checks.**
   - Verify every local asset referenced by the HTML exists.
   - Check HTML/CSS/JavaScript syntax with available tools.
   - Run the backend's existing check script, using `npm.cmd` on Windows when PowerShell blocks `npm.ps1`.
   - Run tests, if present.
   - Do not run destructive database commands against production.
   - If browser tooling is available, smoke-test the homepage, navigation, theme toggle, project filters, CV download, and contact workflow.

4. **Inspect production blockers.**
   Flag, with file paths, any issue involving:
   - missing assets or broken links
   - hardcoded localhost URLs or wrong canonical/OG URLs
   - missing build/start commands
   - missing production environment variables
   - wildcard `CORS_ORIGIN` in production
   - default seed credentials or weak `JWT_SECRET`
   - running seed data in production without explicit approval
   - database migrations not prepared for deployment
   - reliance on the in-memory analytics buffer with multiple API instances
   - missing HTTPS, health checks, logs, backups, or observability
   - secrets committed to the repository

5. **Give a verdict.**
   Use one of:
   - **Ready for static deployment**
   - **Ready with listed changes**
   - **Not ready for deployment**

   Give separate verdicts for the frontend and backend. Explain what was actually verified and what could not be verified.

6. **Produce the deployment runbook.**
   Include only applicable steps, in this order:
   - commit/push the source without secrets
   - create the static host project with the repository root as its publish directory
   - configure the frontend domain and HTTPS
   - provision PostgreSQL if the backend is needed
   - configure backend environment variables: `NODE_ENV=production`, `PORT`, `DATABASE_URL`, a long random `JWT_SECRET`, `JWT_EXPIRES_IN`, exact frontend `CORS_ORIGIN`, and analytics settings as needed
   - deploy the backend from `backend/` with `npm install`, `npm run prisma:generate`, `npm run prisma:migrate`, and `npm start`
   - do not run `npm run db:seed` in production unless seed data and credentials have been deliberately replaced
   - configure the frontend to use the backend URL only if code actually calls the API
   - verify `GET /health`, public API routes, admin authentication, and error responses
   - configure domain DNS, logs, restart policy, database backups, and monitoring

7. **Report residual risk and next actions.**
   Separate blockers from recommendations. Mention provider-specific values the user must supply, and never invent deployment success, DNS state, credentials, or live URLs.

## Project-Specific Notes

For this repository:

- The root frontend currently uses a `mailto:` contact workflow and does not require the API to render or submit its contact form.
- The backend is an Express + Prisma service requiring PostgreSQL and exposes `/health` plus `/api/*` routes.
- `backend/.env` must remain private; use `.env.example` as the variable checklist.
- The default seed admin password is explicitly unsafe for production.
- The analytics buffer is in-memory and should not be treated as durable across multiple backend instances.

## Completion Criteria

The response is complete only when it includes:

- separate frontend/backend readiness verdicts
- checks run and their results
- every blocking issue with a concrete fix
- an ordered deployment sequence
- production environment-variable guidance
- post-deployment smoke tests
- explicit unknowns or unverified items
