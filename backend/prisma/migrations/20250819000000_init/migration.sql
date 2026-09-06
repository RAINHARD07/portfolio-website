-- Initial portfolio schema. Composite indexes match the cursor pagination order used by the API.
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE TABLE "messages" (
  "id" BIGSERIAL PRIMARY KEY,
  "name" VARCHAR(120) NOT NULL,
  "email" VARCHAR(320) NOT NULL,
  "subject" VARCHAR(200),
  "message" TEXT NOT NULL,
  "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "is_read" BOOLEAN NOT NULL DEFAULT false
);
CREATE INDEX "messages_created_at_id_idx" ON "messages" ("created_at" DESC, "id" DESC);
CREATE INDEX "messages_is_read_created_at_id_idx" ON "messages" ("is_read", "created_at" DESC, "id" DESC);
CREATE INDEX "messages_email_idx" ON "messages" ("email");
CREATE INDEX "messages_name_trgm_idx" ON "messages" USING GIN ("name" gin_trgm_ops);
CREATE INDEX "messages_subject_trgm_idx" ON "messages" USING GIN ("subject" gin_trgm_ops);

CREATE TABLE "projects" (
  "id" BIGSERIAL PRIMARY KEY,
  "title" VARCHAR(240) NOT NULL,
  "description" TEXT NOT NULL,
  "category" VARCHAR(80) NOT NULL,
  "tech_stack" TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
  "image_url" VARCHAR(500),
  "project_url" VARCHAR(500),
  "github_url" VARCHAR(500),
  "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "featured" BOOLEAN NOT NULL DEFAULT false
);
CREATE INDEX "projects_category_created_at_id_idx" ON "projects" ("category", "created_at" DESC, "id" DESC);
CREATE INDEX "projects_featured_created_at_id_idx" ON "projects" ("featured", "created_at" DESC, "id" DESC);

CREATE TABLE "blog_posts" (
  "id" BIGSERIAL PRIMARY KEY,
  "title" VARCHAR(240) NOT NULL,
  "slug" VARCHAR(260) NOT NULL UNIQUE,
  "content" TEXT NOT NULL,
  "excerpt" VARCHAR(500),
  "tags" TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
  "published_at" TIMESTAMPTZ,
  "views_count" BIGINT NOT NULL DEFAULT 0
);
CREATE INDEX "blog_posts_published_at_id_idx" ON "blog_posts" ("published_at" DESC, "id" DESC);
CREATE INDEX "blog_posts_tags_gin_idx" ON "blog_posts" USING GIN ("tags");

CREATE TABLE "analytics_visits" (
  "id" BIGSERIAL PRIMARY KEY,
  "page_visited" VARCHAR(500) NOT NULL,
  "ip_hash" CHAR(64) NOT NULL,
  "user_agent" VARCHAR(500),
  "referrer" VARCHAR(500),
  "visited_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX "analytics_visits_visited_at_idx" ON "analytics_visits" ("visited_at");
CREATE INDEX "analytics_visits_visited_at_page_idx" ON "analytics_visits" ("visited_at", "page_visited");
CREATE INDEX "analytics_visits_ip_hash_visited_at_idx" ON "analytics_visits" ("ip_hash", "visited_at");

CREATE TABLE "skills" (
  "id" BIGSERIAL PRIMARY KEY,
  "name" VARCHAR(120) NOT NULL,
  "category" VARCHAR(80) NOT NULL,
  "proficiency_level" INTEGER NOT NULL
);
CREATE UNIQUE INDEX "skills_name_category_key" ON "skills" ("name", "category");
CREATE INDEX "skills_category_proficiency_level_idx" ON "skills" ("category", "proficiency_level" DESC);

CREATE TABLE "admin_users" (
  "id" BIGSERIAL PRIMARY KEY,
  "email" VARCHAR(320) NOT NULL UNIQUE,
  "password_hash" VARCHAR(255) NOT NULL,
  "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
